import pygame
from ui.sprites import (
    COLORS, MODULE_COLORS, draw_module_sprite, draw_floor_tile,
    draw_empty_tile, draw_cursor, generate_star_field, draw_mini_planet,
    draw_resource_icon,
)
from data.modules import MODULES, REFINE_RECIPES
from data.config import EMPTY, FLOOR, SCREENS, HULL_COST

TILE_SIZE = 32
SCREEN_W = 1024
SCREEN_H = 768
HEADER_H = 40
FOOTER_H = 70


class Renderer:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("DEAD SUN")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("monospace", 24, bold=True)
        self.font_med = pygame.font.SysFont("monospace", 16)
        self.font_small = pygame.font.SysFont("monospace", 12)
        self.star_field = generate_star_field(SCREEN_W, SCREEN_H)
        self.fps = 30

    def render(self, game):
        self._draw_bg()
        self._draw_header(game)
        renderers = {
            "ship": self._render_ship_screen,
            "map": self._render_map_screen,
            "crew": self._render_crew_screen,
            "cargo": self._render_cargo_screen,
            "systems": self._render_systems_screen,
        }
        renderer = renderers.get(game.screen, self._render_ship_screen)
        renderer(game)
        self._draw_footer(game)
        pygame.display.flip()
        self.clock.tick(self.fps)

    def _draw_bg(self):
        self.screen.blit(self.star_field, (0, 0))
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 60))
        self.screen.blit(overlay, (0, 0))

    def _draw_header(self, game):
        title_surf = self.font_large.render("DEAD SUN", True, COLORS["title"])
        self.screen.blit(title_surf, (10, 8))

        day_surf = self.font_med.render(f"Day {game.day}", True, COLORS["title"])
        self.screen.blit(day_surf, (160, 12))

        loc_name = game.current_location.name
        loc_surf = self.font_med.render(f"Location: {loc_name}", True, COLORS["text"])
        self.screen.blit(loc_surf, (320, 12))

        credits_surf = self.font_med.render(f"Credits: {game.credits}cr", True, COLORS["title"])
        self.screen.blit(credits_surf, (580, 12))

        resources = ["metal", "electronics", "fuel", "food", "water", "iron_ore"]
        rx = SCREEN_W - 10
        for res in reversed(resources):
            val = game.cargo.get(res, 0)
            draw_resource_icon(self.screen, res, rx - 80, 12, 16)
            val_surf = self.font_small.render(f"{val}", True, COLORS["text"])
            self.screen.blit(val_surf, (rx - 60, 14))
            rx -= 95

        pygame.draw.line(self.screen, COLORS["border"], (0, HEADER_H - 2), (SCREEN_W, HEADER_H - 2), 1)

    def _draw_footer(self, game):
        fy = SCREEN_H - FOOTER_H
        pygame.draw.line(self.screen, COLORS["border"], (0, fy), (SCREEN_W, fy), 1)

        screen_idx = SCREENS.index(game.screen) if game.screen in SCREENS else 0
        tx = 10
        for i, s in enumerate(SCREENS):
            if i == screen_idx:
                label = f"[{s.upper()}]"
                color = COLORS["cursor"]
            else:
                label = f" {s} "
                color = COLORS["text_dim"]
            tab_surf = self.font_med.render(label, True, color)
            self.screen.blit(tab_surf, (tx, fy + 8))
            tx += tab_surf.get_width() + 10

        commands = {
            "ship": "WASD:Move  B:Build  X:Remove  Q:Quit",
            "map": "Up/Down:Select  N:Navigate  M:Mine  R:Refine  Q:Quit",
            "crew": "Up/Down:Select  A:Assign  U:Unassign  Q:Quit",
            "cargo": "Up/Down:Select recipe  R:Refine  Q:Quit",
            "systems": "TAB:Switch screen  Q:Quit",
        }
        cmd = commands.get(game.screen, "Q:Quit")
        cmd_surf = self.font_small.render(cmd, True, COLORS["text_dim"])
        self.screen.blit(cmd_surf, (10, fy + 35))

        if game.message_timer > 0 and game.message:
            msg_surf = self.font_med.render(game.message, True, COLORS["warn"])
            mx = SCREEN_W - msg_surf.get_width() - 15
            self.screen.blit(msg_surf, (mx, fy + 35))

        tab_hint = self.font_small.render("TAB: Switch screen", True, COLORS["text_dim"])
        self.screen.blit(tab_hint, (10, fy + 52))

    def _render_ship_screen(self, game):
        ship = game.ship
        grid_w = ship.width * TILE_SIZE
        grid_h = ship.height * TILE_SIZE
        info_w = 240
        total_w = grid_w + info_w + 20
        total_h = grid_h

        avail_h = SCREEN_H - HEADER_H - FOOTER_H
        avail_w = SCREEN_W

        origin_x = (avail_w - total_w) // 2
        origin_y = HEADER_H + (avail_h - total_h) // 2

        border_rect = pygame.Rect(origin_x - 4, origin_y - 4, grid_w + 8, grid_h + 8)
        pygame.draw.rect(self.screen, COLORS["border"], border_rect, 2, border_radius=3)

        for r in range(ship.height):
            for c in range(ship.width):
                tx = origin_x + c * TILE_SIZE
                ty = origin_y + r * TILE_SIZE
                tile = ship.grid[r][c]
                module = ship.get_module_at(r, c)

                if module:
                    draw_module_sprite(self.screen, module, tx, ty, TILE_SIZE)
                elif tile == FLOOR:
                    draw_floor_tile(self.screen, tx, ty, TILE_SIZE)
                else:
                    draw_empty_tile(self.screen, tx, ty, TILE_SIZE)

        cursor_x = origin_x + game.cursor_c * TILE_SIZE
        cursor_y = origin_y + game.cursor_r * TILE_SIZE
        draw_cursor(self.screen, cursor_x, cursor_y, TILE_SIZE)

        info_x = origin_x + grid_w + 20
        info_y = origin_y

        self._draw_panel(info_x, info_y, info_w, grid_h, "Info")

        pos_label = self.font_small.render(f"Cursor: ({game.cursor_r}, {game.cursor_c})", True, COLORS["text"])
        self.screen.blit(pos_label, (info_x + 8, info_y + 24))

        tile = ship.get_tile(game.cursor_r, game.cursor_c)
        module = ship.get_module_at(game.cursor_r, game.cursor_c)

        iy = info_y + 44
        if module:
            m = MODULES[module]
            mc = MODULE_COLORS.get(module, {})
            name_color = mc.get("primary", COLORS["text"])
            name_surf = self.font_med.render(m["name"], True, name_color)
            self.screen.blit(name_surf, (info_x + 8, iy))
            iy += 22

            pwr_val = m["pwr"]
            pwr_color = COLORS["good"] if pwr_val <= 0 else COLORS["warn"]
            pwr_sign = "+" if pwr_val > 0 else ""
            pwr_surf = self.font_small.render(f"Power: {pwr_sign}{pwr_val}", True, pwr_color)
            self.screen.blit(pwr_surf, (info_x + 8, iy))
            iy += 16

            o2_val = m["o2"]
            o2_color = COLORS["good"] if o2_val <= 0 else COLORS["warn"]
            o2_sign = "+" if o2_val > 0 else ""
            o2_surf = self.font_small.render(f"O2:    {o2_sign}{o2_val}", True, o2_color)
            self.screen.blit(o2_surf, (info_x + 8, iy))
            iy += 16

            crew_m = game.roster.get_assigned_to((game.cursor_r, game.cursor_c))
            if crew_m:
                crew_surf = self.font_small.render(f"Crew: {crew_m.name}", True, COLORS["good"])
            elif m["crew"] > 0:
                crew_surf = self.font_small.render("Crew: (unmanned)", True, COLORS["warn"])
            else:
                crew_surf = self.font_small.render("Crew: ---", True, COLORS["text_dim"])
            self.screen.blit(crew_surf, (info_x + 8, iy))
        elif tile == FLOOR:
            fl_surf = self.font_small.render("Empty floor", True, COLORS["text_dim"])
            self.screen.blit(fl_surf, (info_x + 8, iy))
        elif tile == EMPTY:
            can_build = ship.is_buildable(game.cursor_r, game.cursor_c)
            if can_build:
                sp_surf = self.font_small.render("Space (buildable)", True, COLORS["good"])
            else:
                sp_surf = self.font_small.render("Space", True, COLORS["text_dim"])
            self.screen.blit(sp_surf, (info_x + 8, iy))

        stat_y = info_y + grid_h // 2 + 20
        sep_surf = self.font_small.render("-- Ship Status --", True, COLORS["border"])
        self.screen.blit(sep_surf, (info_x + 8, stat_y))
        stat_y += 20

        pwr_gen, pwr_use = ship.get_power_balance()
        pwr_ok = pwr_gen >= pwr_use
        pwr_color = COLORS["good"] if pwr_ok else COLORS["bad"]
        pwr_text = f"Power: {pwr_gen}/{pwr_use}"
        self.screen.blit(self.font_small.render(pwr_text, True, pwr_color), (info_x + 8, stat_y))
        self._draw_bar(info_x + 8, stat_y + 16, info_w - 16, 8, pwr_gen, max(pwr_gen, pwr_use), COLORS["good"], COLORS["bad"])
        stat_y += 30

        o2_gen, o2_use = ship.get_oxygen_balance()
        o2_ok = o2_gen >= o2_use
        o2_color = COLORS["good"] if o2_ok else COLORS["bad"]
        o2_text = f"O2:    {o2_gen}/{o2_use}"
        self.screen.blit(self.font_small.render(o2_text, True, o2_color), (info_x + 8, stat_y))
        self._draw_bar(info_x + 8, stat_y + 16, info_w - 16, 8, o2_gen, max(o2_gen, o2_use), COLORS["good"], COLORS["bad"])
        stat_y += 30

        cargo_total = ship.get_total_cargo(game.cargo)
        cargo_max = ship.get_cargo_capacity()
        cclr = COLORS["good"] if cargo_total < cargo_max else COLORS["warn"]
        cargo_text = f"Cargo: {cargo_total}/{cargo_max}"
        self.screen.blit(self.font_small.render(cargo_text, True, cclr), (info_x + 8, stat_y))
        self._draw_bar(info_x + 8, stat_y + 16, info_w - 16, 8, cargo_total, cargo_max, COLORS["good"], COLORS["warn"])
        stat_y += 30

        crew_text = f"Crew:  {len(game.roster.members)}/{ship.get_max_crew()}"
        self.screen.blit(self.font_small.render(crew_text, True, COLORS["text"]), (info_x + 8, stat_y))

        if game.build_menu_open:
            self._render_build_menu(game)

    def _render_build_menu(self, game):
        ship = game.ship
        r, c = game.cursor_r, game.cursor_c
        tile = ship.get_tile(r, c)

        options = []
        if tile == EMPTY and ship.is_buildable(r, c):
            options.append(("hull", "Hull Extension", HULL_COST))
        elif tile == FLOOR and ship.can_place_module(r, c):
            for key, m in MODULES.items():
                if key == "cockpit":
                    continue
                options.append((key, m["name"], m["cost"]))

        if not options:
            game.build_menu_open = False
            return

        menu_w = 420
        line_h = 24
        menu_h = len(options) * line_h + 60

        mx = (SCREEN_W - menu_w) // 2
        my = (SCREEN_H - menu_h) // 2

        panel = pygame.Surface((menu_w, menu_h), pygame.SRCALPHA)
        panel.fill((10, 10, 30, 220))
        self.screen.blit(panel, (mx, my))

        pygame.draw.rect(self.screen, COLORS["border"], (mx, my, menu_w, menu_h), 2, border_radius=4)

        title_surf = self.font_med.render("-- BUILD --", True, COLORS["border"])
        self.screen.blit(title_surf, (mx + (menu_w - title_surf.get_width()) // 2, my + 8))

        for i, (key, name, cost) in enumerate(options):
            oy = my + 36 + i * line_h
            cost_parts = []
            for res, amt in cost.items():
                cost_parts.append(f"{amt} {res[:4]}")
            cost_str = " ".join(cost_parts) if cost_parts else "free"
            can_afford = game.can_afford(cost)

            if i == game.build_choice:
                sel_rect = pygame.Rect(mx + 4, oy - 2, menu_w - 8, line_h)
                sel_surf = pygame.Surface((sel_rect.width, sel_rect.height), pygame.SRCALPHA)
                sel_surf.fill((255, 220, 80, 40))
                self.screen.blit(sel_surf, (sel_rect.x, sel_rect.y))
                pygame.draw.rect(self.screen, COLORS["cursor"], sel_rect, 1)
                prefix = "> "
                name_color = COLORS["cursor"]
            else:
                prefix = "  "
                name_color = COLORS["text"] if can_afford else COLORS["bad"]

            cost_color = COLORS["good"] if can_afford else COLORS["bad"]
            opt_surf = self.font_small.render(f"{prefix}{name}", True, name_color)
            self.screen.blit(opt_surf, (mx + 10, oy + 2))
            cost_surf = self.font_small.render(cost_str, True, cost_color)
            self.screen.blit(cost_surf, (mx + menu_w - cost_surf.get_width() - 10, oy + 2))

        hint_y = my + 36 + len(options) * line_h + 4
        hint_surf = self.font_small.render("Enter: Build   Esc: Cancel", True, COLORS["text_dim"])
        self.screen.blit(hint_surf, (mx + (menu_w - hint_surf.get_width()) // 2, hint_y))

    def _render_map_screen(self, game):
        avail_h = SCREEN_H - HEADER_H - FOOTER_H
        avail_w = SCREEN_W

        panel_w = 700
        panel_h = avail_h - 20
        px = (avail_w - panel_w) // 2
        py = HEADER_H + 10

        self._draw_panel(px, py, panel_w, panel_h, "System Map")

        loc = game.current_location
        cur_surf = self.font_med.render(f"Current: {loc.name}", True, COLORS["title"])
        self.screen.blit(cur_surf, (px + 12, py + 28))

        desc_surf = self.font_small.render(loc.description, True, COLORS["text_dim"])
        self.screen.blit(desc_surf, (px + 12, py + 48))

        list_y = py + 72
        for i, l in enumerate(game.system.locations):
            if l.loc_type == "star":
                continue

            row_y = list_y + (i - 1) * 30
            if row_y + 28 > py + panel_h - 30:
                break

            is_selected = i == game.selected_location
            is_here = l.name == game.current_location.name
            fuel_cost = game.system.travel_cost(game.current_location, l)
            can_travel = game.cargo.get("fuel", 0) >= fuel_cost

            if is_selected:
                sel_rect = pygame.Rect(px + 8, row_y - 2, panel_w - 16, 26)
                sel_bg = pygame.Surface((sel_rect.width, sel_rect.height), pygame.SRCALPHA)
                sel_bg.fill((40, 80, 140, 60))
                self.screen.blit(sel_bg, (sel_rect.x, sel_rect.y))
                pygame.draw.rect(self.screen, COLORS["border"], sel_rect, 1)

            planet_type = l.loc_type if l.explored else "asteroid_field"
            draw_mini_planet(self.screen, px + 24, row_y + 10, planet_type, 6)

            if is_here:
                name_color = COLORS["title"]
                here_tag = " (YOU)"
            elif is_selected:
                name_color = COLORS["white"]
                here_tag = ""
            elif l.explored and can_travel:
                name_color = COLORS["good"]
                here_tag = ""
            elif l.explored:
                name_color = COLORS["warn"]
                here_tag = ""
            else:
                name_color = COLORS["text_dim"]
                here_tag = ""

            display_name = l.name if l.explored else "???"
            name_surf = self.font_med.render(f"{display_name}{here_tag}", True, name_color)
            self.screen.blit(name_surf, (px + 40, row_y + 2))

            dist = game.current_location.distance_to(l)
            info_text = f"dist:{dist}  fuel:{fuel_cost}"
            info_color = COLORS["good"] if can_travel else COLORS["bad"]
            info_surf = self.font_small.render(info_text, True, info_color)
            self.screen.blit(info_surf, (px + panel_w - info_surf.get_width() - 16, row_y + 4))

        action_y = py + panel_h - 60
        pygame.draw.line(self.screen, COLORS["border"], (px + 8, action_y), (px + panel_w - 8, action_y), 1)

        sel_loc = game.system.locations[game.selected_location] if game.selected_location < len(game.system.locations) else None
        action_y += 10
        if sel_loc and sel_loc.name != game.current_location.name:
            fuel_cost = game.system.travel_cost(game.current_location, sel_loc)
            nav_surf = self.font_small.render(f"[N] Navigate to {sel_loc.name} ({fuel_cost} fuel)", True, COLORS["good"])
            self.screen.blit(nav_surf, (px + 12, action_y))
            action_y += 18

        if game.current_location.resources:
            mine_surf = self.font_small.render("[M] Mine here", True, COLORS["good"])
            self.screen.blit(mine_surf, (px + 12, action_y))
            action_y += 18

        if game.ship.count_module("refinery") > 0:
            ref_surf = self.font_small.render("[R] Refine resources", True, COLORS["good"])
            self.screen.blit(ref_surf, (px + 12, action_y))

    def _render_crew_screen(self, game):
        avail_h = SCREEN_H - HEADER_H - FOOTER_H
        avail_w = SCREEN_W

        panel_w = avail_w - 40
        panel_h = avail_h - 20
        px = 20
        py = HEADER_H + 10

        self._draw_panel(px, py, panel_w, panel_h, "Crew Roster")

        food_val = game.cargo.get("food", 0)
        crew_count = len(game.roster.members)
        max_crew = game.ship.get_max_crew()
        summary = f"Food: {food_val}  |  Crew: {crew_count}/{max_crew}"
        sum_surf = self.font_small.render(summary, True, COLORS["text"])
        self.screen.blit(sum_surf, (px + panel_w - 280, py + 10))

        y = py + 30
        for i, m in enumerate(game.roster.members):
            row_h = 80
            if y + row_h > py + panel_h - 10:
                more_surf = self.font_small.render("... more crew below ...", True, COLORS["text_dim"])
                self.screen.blit(more_surf, (px + 12, y))
                break

            selected = i == game.selected_crew
            if selected:
                sel_rect = pygame.Rect(px + 6, y - 2, panel_w - 12, row_h)
                sel_bg = pygame.Surface((sel_rect.width, sel_rect.height), pygame.SRCALPHA)
                sel_bg.fill((40, 80, 140, 50))
                self.screen.blit(sel_bg, (sel_rect.x, sel_rect.y))
                pygame.draw.rect(self.screen, COLORS["border"], sel_rect, 1)
                prefix = "> "
            else:
                prefix = "  "

            status = m.status_text()
            status_colors = {
                "ok": COLORS["good"], "hungry": COLORS["warn"],
                "unhappy": COLORS["warn"], "injured": COLORS["bad"],
                "critical": COLORS["bad"],
            }
            status_color = status_colors.get(status, COLORS["text"])

            line1 = f"{prefix}{m.name} ({m.role})   [{status}]"
            self.screen.blit(self.font_med.render(line1, True, status_color if selected else COLORS["text"]), (px + 12, y + 2))

            if m.assigned_to:
                mt = game.ship.get_module_at(*m.assigned_to)
                assign_text = f"Assigned: {MODULES[mt]['name']}" if mt else "Assigned: ???"
                assign_color = COLORS["good"]
            else:
                assign_text = "Unassigned"
                assign_color = COLORS["text_dim"]
            self.screen.blit(self.font_small.render(assign_text, True, assign_color), (px + 28, y + 24))

            bar_w = 120
            bar_h = 8
            morale_label = self.font_small.render(f"Morale {m.morale}%", True, COLORS["good"] if m.morale > 50 else COLORS["warn"])
            self.screen.blit(morale_label, (px + 28, y + 40))
            self._draw_bar(px + 120, y + 42, bar_w, bar_h, m.morale, 100, COLORS["good"], COLORS["bad"])

            health_label = self.font_small.render(f"Health {m.health}%", True, COLORS["good"] if m.health > 50 else COLORS["bad"])
            self.screen.blit(health_label, (px + 28, y + 54))
            self._draw_bar(px + 120, y + 56, bar_w, bar_h, m.health, 100, COLORS["good"], COLORS["bad"])

            top_skills = sorted(m.skills.items(), key=lambda x: x[1], reverse=True)[:3]
            skills_parts = []
            for sk, sv in top_skills:
                stars = "*" * sv
                skills_parts.append(f"{sk[:3]}:{stars}")
            skills_str = "  ".join(skills_parts)
            self.screen.blit(self.font_small.render(skills_str, True, COLORS["text_dim"]), (px + 260, y + 48))

            y += row_h

    def _render_cargo_screen(self, game):
        avail_h = SCREEN_H - HEADER_H - FOOTER_H
        avail_w = SCREEN_W

        panel_w = avail_w - 40
        panel_h = avail_h - 20
        px = 20
        py = HEADER_H + 10

        self._draw_panel(px, py, panel_w, panel_h, "Cargo Hold")

        cargo_total = game.ship.get_total_cargo(game.cargo)
        cargo_max = game.ship.get_cargo_capacity()
        cap_text = f"{cargo_total}/{cargo_max}"
        cap_color = COLORS["good"] if cargo_total < cargo_max else COLORS["warn"]
        cap_surf = self.font_med.render(cap_text, True, cap_color)
        self.screen.blit(cap_surf, (px + panel_w - cap_surf.get_width() - 20, py + 10))

        y = py + 36
        col = 0
        col_w = 200
        col_count = max(1, (panel_w - 20) // col_w)
        for key in sorted(game.cargo.keys()):
            val = game.cargo[key]
            cx = px + 14 + col * col_w
            draw_resource_icon(self.screen, key, cx, y + 2, 16)
            name_color = COLORS["text"] if val > 0 else COLORS["text_dim"]
            name_surf = self.font_small.render(f"{key}", True, name_color)
            self.screen.blit(name_surf, (cx + 20, y + 2))
            val_surf = self.font_small.render(f"{val}", True, name_color)
            self.screen.blit(val_surf, (cx + col_w - 50, y + 2))
            col += 1
            if col >= col_count:
                col = 0
                y += 22

        if game.ship.count_module("refinery") > 0:
            ref_y = y + 20
            pygame.draw.line(self.screen, COLORS["border"], (px + 8, ref_y), (px + panel_w - 8, ref_y), 1)
            ref_y += 8
            ref_title = self.font_med.render("Refinery", True, COLORS["border"])
            self.screen.blit(ref_title, (px + 12, ref_y))
            ref_y += 26

            for i, (name, recipe) in enumerate(REFINE_RECIPES.items()):
                inputs_parts = []
                for rk, rv in recipe["inputs"].items():
                    inputs_parts.append(f"{rv} {rk}")
                inputs_str = " + ".join(inputs_parts)
                selected = i == game.selected_recipe
                can = game.can_afford(recipe["inputs"])

                if selected:
                    sel_rect = pygame.Rect(px + 8, ref_y - 2, panel_w - 16, 22)
                    sel_bg = pygame.Surface((sel_rect.width, sel_rect.height), pygame.SRCALPHA)
                    sel_bg.fill((255, 220, 80, 30))
                    self.screen.blit(sel_bg, (sel_rect.x, sel_rect.y))
                    pygame.draw.rect(self.screen, COLORS["cursor"], sel_rect, 1)

                prefix = "> " if selected else "  "
                color = COLORS["good"] if can else COLORS["bad"]
                recipe_text = f"{prefix}{inputs_str} -> {recipe['output']} {name}"
                self.screen.blit(self.font_small.render(recipe_text, True, color), (px + 12, ref_y + 2))
                ref_y += 24

            hint_surf = self.font_small.render("[R] Refine   Up/Down: Select recipe", True, COLORS["text_dim"])
            self.screen.blit(hint_surf, (px + 12, ref_y + 8))

    def _render_systems_screen(self, game):
        avail_h = SCREEN_H - HEADER_H - FOOTER_H
        avail_w = SCREEN_W

        panel_w = avail_w - 40
        panel_h = avail_h - 20
        px = 20
        py = HEADER_H + 10

        self._draw_panel(px, py, panel_w, panel_h, "Ship Systems")

        ship = game.ship
        pwr_gen, pwr_use = ship.get_power_balance()
        o2_gen, o2_use = ship.get_oxygen_balance()

        y = py + 30
        bar_w = 300

        pwr_ok = pwr_gen >= pwr_use
        pwr_color = COLORS["good"] if pwr_ok else COLORS["bad"]
        pwr_status = "OK" if pwr_ok else "DEFICIT!"
        pwr_label = self.font_med.render(f"POWER  {pwr_gen}/{pwr_use}  {pwr_status}", True, pwr_color)
        self.screen.blit(pwr_label, (px + 12, y))
        self._draw_bar(px + 12, y + 24, bar_w, 12, pwr_gen, max(pwr_gen, pwr_use, 1), COLORS["good"], COLORS["bad"])
        y += 44

        o2_ok = o2_gen >= o2_use
        o2_color = COLORS["good"] if o2_ok else COLORS["bad"]
        o2_status = "OK" if o2_ok else "DEFICIT!"
        o2_label = self.font_med.render(f"OXYGEN {o2_gen}/{o2_use}  {o2_status}", True, o2_color)
        self.screen.blit(o2_label, (px + 12, y))
        self._draw_bar(px + 12, y + 24, bar_w, 12, o2_gen, max(o2_gen, o2_use, 1), COLORS["good"], COLORS["bad"])
        y += 50

        pygame.draw.line(self.screen, COLORS["border"], (px + 8, y), (px + panel_w - 8, y), 1)
        y += 8
        mod_title = self.font_med.render("Modules", True, COLORS["border"])
        self.screen.blit(mod_title, (px + 12, y))
        y += 24

        for pos, mt in sorted(ship.modules.items()):
            if y + 18 > py + panel_h - 80:
                more_surf = self.font_small.render("... more modules ...", True, COLORS["text_dim"])
                self.screen.blit(more_surf, (px + 12, y))
                break

            m = MODULES[mt]
            mc = MODULE_COLORS.get(mt, {})
            name_color = mc.get("primary", COLORS["text"])
            crew_m = game.roster.get_assigned_to(pos)
            if crew_m:
                crew_txt = crew_m.name
            elif m["crew"] > 0:
                crew_txt = "(need crew)"
            else:
                crew_txt = "---"

            pwr_sign = "+" if m["pwr"] < 0 else ""
            line = f"{m['name']:<16} Pwr:{pwr_sign}{abs(m['pwr']):>2}  O2:{m['o2']:>+2}  Crew: {crew_txt}"
            self.screen.blit(self.font_small.render(line, True, name_color), (px + 16, y))
            y += 18

        crew_y = py + panel_h - 60
        pygame.draw.line(self.screen, COLORS["border"], (px + 8, crew_y), (px + panel_w - 8, crew_y), 1)
        crew_y += 8
        crew_title = self.font_med.render("Crew Status", True, COLORS["border"])
        self.screen.blit(crew_title, (px + 12, crew_y))
        crew_y += 22

        for m in game.roster.members[:4]:
            status = m.status_text()
            status_colors = {
                "ok": COLORS["good"], "hungry": COLORS["warn"],
                "unhappy": COLORS["warn"], "injured": COLORS["bad"],
                "critical": COLORS["bad"],
            }
            sc = status_colors.get(status, COLORS["text"])
            line = f"{m.name:<20} HP:{m.health}%  Morale:{m.morale}%  {status}"
            self.screen.blit(self.font_small.render(line, True, sc), (px + 16, crew_y))
            crew_y += 16

    def _draw_bar(self, x, y, w, h, value, max_val, color_good, color_bad):
        if max_val <= 0:
            max_val = 1
        ratio = min(1.0, max(0.0, value / max_val))
        pygame.draw.rect(self.screen, (30, 30, 50), (x, y, w, h))
        fill_w = int(w * ratio)
        color = color_good if ratio >= 0.5 else color_bad
        if fill_w > 0:
            pygame.draw.rect(self.screen, color, (x, y, fill_w, h))
        pygame.draw.rect(self.screen, COLORS["border"], (x, y, w, h), 1)

    def _draw_panel(self, x, y, w, h, title=""):
        panel_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        panel_surf.fill((15, 15, 35, 180))
        self.screen.blit(panel_surf, (x, y))
        pygame.draw.rect(self.screen, COLORS["border"], (x, y, w, h), 2, border_radius=3)
        if title:
            title_surf = self.font_med.render(title, True, COLORS["border"])
            self.screen.blit(title_surf, (x + (w - title_surf.get_width()) // 2, y + 4))
