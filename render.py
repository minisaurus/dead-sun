"""Dead Sun - Curses-based terminal rendering."""

import curses
from data.config import CLR_TITLE, CLR_GOOD, CLR_WARN, CLR_BAD, CLR_HIGHLIGHT, CLR_DIM, CLR_MODULE, CLR_CURSOR, CLR_BORDER, EMPTY, FLOOR, SCREENS, HULL_COST
from data.modules import MODULES, REFINE_RECIPES

HEADER_H = 2
FOOTER_H = 4
SIDE_PAD = 4


def _content_offset(max_w, max_h, content_w, content_h):
    """Calculate (row, col) to center a content block between header and footer."""
    avail_w = max_w - SIDE_PAD * 2
    avail_h = max_h - HEADER_H - FOOTER_H
    r = HEADER_H + max(1, (avail_h - content_h) // 2)
    c = SIDE_PAD + max(0, (avail_w - content_w) // 2)
    return r, c


def init_colors():
    curses.start_color()
    curses.init_pair(CLR_TITLE, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(CLR_GOOD, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(CLR_WARN, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(CLR_BAD, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(CLR_HIGHLIGHT, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(CLR_DIM, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(CLR_MODULE, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(CLR_CURSOR, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(CLR_BORDER, curses.COLOR_BLUE, curses.COLOR_BLACK)


def safe_addstr(win, r, c, text, color=0):
    try:
        win.addstr(r, c, text, color)
    except curses.error:
        pass


def render_header(win, game, max_w):
    safe_addstr(win, 0, 0, " ☀️  DEAD SUN ", curses.color_pair(CLR_TITLE) | curses.A_BOLD)
    safe_addstr(win, 0, 16, f"Day {game.day}", curses.color_pair(CLR_TITLE))
    loc = game.current_location
    safe_addstr(win, 0, 26, f"📍 {loc.name}", curses.color_pair(CLR_TITLE))
    safe_addstr(win, 0, 50, f"💳 {game.credits}cr", curses.color_pair(CLR_TITLE))

    resources = [
        ("metal", "🔩"),
        ("electronics", "💎"),
        ("fuel", "⛽"),
        ("food", "🍖"),
        ("water", "💧"),
        ("iron_ore", "🪨"),
    ]
    x = max_w - 2
    for key, sym in reversed(resources):
        val = game.cargo.get(key, 0)
        text = f"{sym}{val}"
        x -= len(text) + 1
        safe_addstr(win, 0, x, text, curses.color_pair(CLR_TITLE))

    safe_addstr(win, 1, 0, "─" * max_w, curses.color_pair(CLR_BORDER))


def render_footer(win, game, max_w, max_h):
    y = max_h - 3
    safe_addstr(win, y, 0, "─" * max_w, curses.color_pair(CLR_BORDER))

    screen_idx = SCREENS.index(game.screen) if game.screen in SCREENS else 0
    tabs = "  ".join(f"[{s.upper()}]" if i == screen_idx else s for i, s in enumerate(SCREENS))

    commands = {
        "ship": "[WASD] Move  [B] Build  [X] Remove module  [Q] Quit",
        "map":  "[↑↓] Select  [N] Navigate  [M] Mine  [R] Refine  [Q] Quit",
        "crew": "[↑↓] Select  [A] Assign to module  [U] Unassign  [Q] Quit",
        "cargo": "[↑↓] Select recipe  [R] Refine  [Q] Quit",
        "systems": "[TAB] Switch screen  [Q] Quit",
    }
    cmd_text = commands.get(game.screen, "[Q] Quit")

    safe_addstr(win, y + 1, 0, f" TAB:switch ", curses.color_pair(CLR_DIM))
    safe_addstr(win, y + 1, 12, tabs, curses.color_pair(CLR_BORDER))

    safe_addstr(win, y + 2, 0, f" {cmd_text}", curses.color_pair(CLR_DIM))

    if game.message_timer > 0 and game.message:
        safe_addstr(win, y + 2, max_w - len(game.message) - 2, game.message, curses.color_pair(CLR_WARN) | curses.A_BOLD)


def render_ship_view(win, game, max_w, max_h):
    render_header(win, game, max_w)

    ship = game.ship
    grid_pixel_w = ship.width * 2 + 2
    info_w = 28
    total_w = grid_pixel_w + info_w + 3
    total_h = ship.height + 2

    header_h = 2
    footer_h = 4
    avail_h = max_h - header_h - footer_h
    avail_w = max_w

    offset_r = header_h + max(1, (avail_h - total_h) // 2)
    offset_c = max(1, (avail_w - total_w) // 2)

    safe_addstr(win, offset_r, offset_c, "╔" + "═" * (ship.width * 2) + "╗", curses.color_pair(CLR_BORDER))
    for r in range(ship.height):
        row_y = offset_r + 1 + r
        safe_addstr(win, row_y, offset_c, "║", curses.color_pair(CLR_BORDER))
        for c in range(ship.width):
            cx = offset_c + 1 + c * 2
            tile = ship.grid[r][c]
            module = ship.get_module_at(r, c)
            is_cursor = (r == game.cursor_r and c == game.cursor_c)

            if is_cursor:
                attr = curses.color_pair(CLR_CURSOR) | curses.A_BOLD
            elif module:
                attr = curses.color_pair(CLR_MODULE)
            elif tile == FLOOR:
                attr = curses.color_pair(CLR_DIM)
            else:
                attr = 0

            if module:
                sym = MODULES[module]["sym"]
                safe_addstr(win, row_y, cx, sym[0], attr)
            elif tile == FLOOR:
                safe_addstr(win, row_y, cx, "·", attr)
            else:
                safe_addstr(win, row_y, cx, " ", attr)
            safe_addstr(win, row_y, cx + 1, " ", 0)

        safe_addstr(win, row_y, offset_c + 1 + ship.width * 2, "║", curses.color_pair(CLR_BORDER))

    bottom = offset_r + 1 + ship.height
    safe_addstr(win, bottom, offset_c, "╚" + "═" * (ship.width * 2) + "╝", curses.color_pair(CLR_BORDER))

    info_x = offset_c + grid_pixel_w + 3
    info_y = offset_r

    tile = ship.get_tile(game.cursor_r, game.cursor_c)
    module = ship.get_module_at(game.cursor_r, game.cursor_c)

    safe_addstr(win, info_y, info_x, "── Cursor ──", curses.color_pair(CLR_BORDER))
    cr_text = f"Position: ({game.cursor_r}, {game.cursor_c})"
    safe_addstr(win, info_y + 1, info_x, cr_text)

    if module:
        m = MODULES[module]
        safe_addstr(win, info_y + 3, info_x, f"{m['sym']} {m['name']}", curses.color_pair(CLR_MODULE) | curses.A_BOLD)
        pwr_color = CLR_GOOD if m["pwr"] <= 0 else CLR_WARN
        safe_addstr(win, info_y + 4, info_x, f"Power: {'+' if m['pwr']<0 else ''}{abs(m['pwr'])}", curses.color_pair(pwr_color))
        o2_color = CLR_GOOD if m["o2"] <= 0 else CLR_WARN
        safe_addstr(win, info_y + 5, info_x, f"O2:    {'+' if m['o2']<0 else ''}{abs(m['o2'])}", curses.color_pair(o2_color))
        crew_member = game.roster.get_assigned_to((game.cursor_r, game.cursor_c))
        if crew_member:
            safe_addstr(win, info_y + 6, info_x, f"Crew:  {crew_member.name}", curses.color_pair(CLR_GOOD))
        elif m["crew"] > 0:
            safe_addstr(win, info_y + 6, info_x, f"Crew:  (unmanned)", curses.color_pair(CLR_WARN))
    elif tile == FLOOR:
        safe_addstr(win, info_y + 3, info_x, "Empty floor", curses.color_pair(CLR_DIM))
    elif tile == EMPTY:
        can_build = ship.is_buildable(game.cursor_r, game.cursor_c)
        if can_build:
            safe_addstr(win, info_y + 3, info_x, "Space (buildable)", curses.color_pair(CLR_GOOD))
        else:
            safe_addstr(win, info_y + 3, info_x, "Space", curses.color_pair(CLR_DIM))

    stat_y = info_y + 8
    pwr_gen, pwr_use = ship.get_power_balance()
    o2_gen, o2_use = ship.get_oxygen_balance()
    safe_addstr(win, stat_y, info_x, "── Ship Status ──", curses.color_pair(CLR_BORDER))
    pwr_status = f"Power: {pwr_gen}/{pwr_use}"
    pclr = CLR_GOOD if pwr_gen >= pwr_use else CLR_BAD
    safe_addstr(win, stat_y + 1, info_x, pwr_status, curses.color_pair(pclr))
    o2_status = f"O2:    {o2_gen}/{o2_use}"
    oclr = CLR_GOOD if o2_gen >= o2_use else CLR_BAD
    safe_addstr(win, stat_y + 2, info_x, o2_status, curses.color_pair(oclr))
    cargo_total = ship.get_total_cargo(game.cargo)
    cargo_max = ship.get_cargo_capacity()
    cclr = CLR_GOOD if cargo_total < cargo_max else CLR_WARN
    safe_addstr(win, stat_y + 3, info_x, f"Cargo: {cargo_total}/{cargo_max}", curses.color_pair(cclr))
    safe_addstr(win, stat_y + 4, info_x, f"Crew:  {len(game.roster.members)}/{ship.get_max_crew()}")

    if game.build_menu_open:
        _render_build_menu(win, game, max_w, max_h)

    render_footer(win, game, max_w, max_h)


def _render_build_menu(win, game, max_w, max_h):
    r = game.cursor_r
    c = game.cursor_c
    ship = game.ship
    tile = ship.get_tile(r, c)

    menu_y = 5
    menu_x = 4
    menu_w = 40
    options = []

    if tile == EMPTY and ship.is_buildable(r, c):
        options.append(("hull", "Hull Extension", HULL_COST))
    elif tile == FLOOR and ship.can_place_module(r, c):
        for key, m in MODULES.items():
            if key == "cockpit":
                continue
            options.append((key, f"{m['sym']} {m['name']}", m["cost"]))

    if not options:
        game.build_menu_open = False
        return

    menu_h = len(options) + 3
    for i in range(menu_h):
        safe_addstr(win, menu_y + i, menu_x, " " * menu_w, curses.color_pair(CLR_HIGHLIGHT))
    safe_addstr(win, menu_y, menu_x, "┌─ BUILD ─" + "─" * (menu_w - 10) + "┐", curses.color_pair(CLR_BORDER))

    for i, (key, name, cost) in enumerate(options):
        cost_str = " ".join(f"{v}{k[:3]}" for k, v in cost.items()) if cost else "free"
        can = game.can_afford(cost)
        prefix = "▶ " if i == game.build_choice else "  "
        clr = curses.color_pair(CLR_GOOD if can else CLR_BAD)
        row_text = f"│{prefix}{name:<20} {cost_str:<14}│"
        safe_addstr(win, menu_y + 1 + i, menu_x, row_text, clr)

    safe_addstr(win, menu_y + len(options) + 1, menu_x, "│ [Enter] Build  [Esc] Cancel" + " " * (menu_w - 30) + "│", curses.color_pair(CLR_DIM))
    safe_addstr(win, menu_y + len(options) + 2, menu_x, "└" + "─" * (menu_w - 2) + "┘", curses.color_pair(CLR_BORDER))


def render_map_view(win, game, max_w, max_h):
    render_header(win, game, max_w)

    y, x = _content_offset(max_w, max_h, 50, len(game.system.locations) + 12)

    loc = game.current_location
    safe_addstr(win, y, x, f"📍 Current: {loc.name}", curses.color_pair(CLR_TITLE) | curses.A_BOLD)
    safe_addstr(win, y + 1, x, f"   {loc.description}", curses.color_pair(CLR_DIM))

    safe_addstr(win, y + 3, x, "─── System Map ───", curses.color_pair(CLR_BORDER))

    nav_y = y + 5
    for i, l in enumerate(game.system.locations):
        if l.loc_type == "star":
            continue
        prefix = " ▶ " if i == game.selected_location else "   "
        here = " (YOU)" if l.name == game.current_location.name else ""

        fuel_cost = game.system.travel_cost(game.current_location, l)
        can_travel = game.cargo.get("fuel", 0) >= fuel_cost
        explored = l.explored

        if here:
            clr = curses.color_pair(CLR_TITLE) | curses.A_BOLD
        elif i == game.selected_location:
            clr = curses.color_pair(CLR_HIGHLIGHT)
        elif explored:
            clr = curses.color_pair(CLR_GOOD) if can_travel else curses.color_pair(CLR_WARN)
        else:
            clr = curses.color_pair(CLR_DIM)

        sym = l.symbol if explored else "?"
        dist = game.current_location.distance_to(l)
        text = f"{prefix}{sym} {l.name:<18} dist:{dist} fuel:{fuel_cost}{here}"
        safe_addstr(win, nav_y + i - 1, x, text, clr)

    cmd_y = nav_y + len(game.system.locations)
    safe_addstr(win, cmd_y + 1, x, "─── Actions ───", curses.color_pair(CLR_BORDER))

    sel_loc = game.system.locations[game.selected_location] if game.selected_location < len(game.system.locations) else None
    if sel_loc and sel_loc.name != game.current_location.name:
        fuel_cost = game.system.travel_cost(game.current_location, sel_loc)
        safe_addstr(win, cmd_y + 2, x, f"[N] Navigate to {sel_loc.name} ({fuel_cost} fuel)", curses.color_pair(CLR_GOOD))

    if game.current_location.resources:
        safe_addstr(win, cmd_y + 3, x, "[M] Mine here", curses.color_pair(CLR_GOOD))

    if game.ship.count_module("refinery") > 0:
        safe_addstr(win, cmd_y + 4, x, "[R] Refine resources", curses.color_pair(CLR_GOOD))

    render_footer(win, game, max_w, max_h)


def render_crew_view(win, game, max_w, max_h):
    render_header(win, game, max_w)

    safe_addstr(win, 3, 2, "─── Crew Roster ───", curses.color_pair(CLR_BORDER))
    safe_addstr(win, 3, 30, f"Food: {game.cargo.get('food', 0)}  |  Crew: {len(game.roster.members)}/{game.ship.get_max_crew()}")

    y = 5
    for i, m in enumerate(game.roster.members):
        selected = i == game.selected_crew
        clr = curses.color_pair(CLR_HIGHLIGHT) if selected else 0

        sym = "👤"
        status = m.status_text()
        status_clr = {
            "ok": CLR_GOOD, "hungry": CLR_WARN, "unhappy": CLR_WARN,
            "injured": CLR_BAD, "critical": CLR_BAD,
        }.get(status, 0)

        prefix = "▶ " if selected else "  "
        line1 = f"{prefix}{sym} {m.name} ({m.role})"
        safe_addstr(win, y, 2, line1, clr)

        assigned_text = "Unassigned"
        if m.assigned_to:
            mt = game.ship.get_module_at(*m.assigned_to)
            if mt:
                assigned_text = f"{MODULES[mt]['sym']} {MODULES[mt]['name']}"
        safe_addstr(win, y + 1, 6, f"Assignment: {assigned_text}", curses.color_pair(CLR_DIM))
        safe_addstr(win, y + 1, 35, f"Status: {status}", curses.color_pair(status_clr))

        bar_w = 15
        morale_bar = "█" * int(m.morale / 100 * bar_w) + "░" * (bar_w - int(m.morale / 100 * bar_w))
        health_bar = "█" * int(m.health / 100 * bar_w) + "░" * (bar_w - int(m.health / 100 * bar_w))
        safe_addstr(win, y + 2, 6, f"Morale {morale_bar} {m.morale}%", curses.color_pair(CLR_GOOD if m.morale > 50 else CLR_WARN))
        safe_addstr(win, y + 3, 6, f"Health {health_bar} {m.health}%", curses.color_pair(CLR_GOOD if m.health > 50 else CLR_BAD))

        top_skills = sorted(m.skills.items(), key=lambda x: x[1], reverse=True)[:3]
        skills_str = "  ".join(f"{k[:3]}:{'★'*v}" for k, v in top_skills)
        safe_addstr(win, y + 4, 6, skills_str, curses.color_pair(CLR_DIM))

        y += 6
        if y > max_h - 5:
            break

    cmd_y = max_h - 4
    safe_addstr(win, cmd_y, 2, "[↑↓] Select  [A] Assign to module  [U] Unassign", curses.color_pair(CLR_DIM))

    render_footer(win, game, max_w, max_h)


def render_cargo_view(win, game, max_w, max_h):
    render_header(win, game, max_w)

    cargo_total = game.ship.get_total_cargo(game.cargo)
    cargo_max = game.ship.get_cargo_capacity()
    safe_addstr(win, 3, 2, "─── Cargo Hold ───", curses.color_pair(CLR_BORDER))
    safe_addstr(win, 3, 25, f"{cargo_total}/{cargo_max}", curses.color_pair(CLR_GOOD if cargo_total < cargo_max else CLR_WARN))

    y = 5
    col = 0
    for key in sorted(game.cargo.keys()):
        val = game.cargo[key]
        x = 4 + col * 25
        text = f"{key:<15} {val:>5}"
        clr = curses.color_pair(CLR_GOOD) if val > 0 else curses.color_pair(CLR_DIM)
        safe_addstr(win, y, x, text, clr)
        col += 1
        if col >= 3:
            col = 0
            y += 1

    if game.ship.count_module("refinery") > 0:
        ref_y = y + 3
        safe_addstr(win, ref_y, 2, "─── Refinery ───", curses.color_pair(CLR_BORDER))
        for i, (name, recipe) in enumerate(REFINE_RECIPES.items()):
            inputs_str = " + ".join(f"{v} {k}" for k, v in recipe["inputs"].items())
            selected = i == game.selected_recipe
            prefix = "▶ " if selected else "  "
            can = game.can_afford(recipe["inputs"])
            clr = curses.color_pair(CLR_GOOD if can else CLR_BAD)
            if selected:
                clr |= curses.A_BOLD
            text = f"{prefix}{inputs_str} → {recipe['output']} {name}"
            safe_addstr(win, ref_y + 1 + i, 4, text, clr)
        safe_addstr(win, ref_y + len(REFINE_RECIPES) + 1, 4, "[R] Refine  [↑↓] Select recipe", curses.color_pair(CLR_DIM))

    render_footer(win, game, max_w, max_h)


def render_systems_view(win, game, max_w, max_h):
    render_header(win, game, max_w)

    ship = game.ship
    safe_addstr(win, 3, 2, "─── Ship Systems ───", curses.color_pair(CLR_BORDER))

    pwr_gen, pwr_use = ship.get_power_balance()
    o2_gen, o2_use = ship.get_oxygen_balance()

    y = 5
    pwr_ok = pwr_gen >= pwr_use
    safe_addstr(win, y, 4, "POWER", curses.color_pair(CLR_BORDER))
    safe_addstr(win, y, 12, f"{'█' * pwr_gen}{'░' * max(0, pwr_use - pwr_gen)}", curses.color_pair(CLR_GOOD if pwr_ok else CLR_BAD))
    safe_addstr(win, y, 30, f"{pwr_gen}/{pwr_use} {'OK' if pwr_ok else 'DEFICIT!'}", curses.color_pair(CLR_GOOD if pwr_ok else CLR_BAD | curses.A_BOLD))

    y += 1
    o2_ok = o2_gen >= o2_use
    safe_addstr(win, y, 4, "OXYGEN", curses.color_pair(CLR_BORDER))
    safe_addstr(win, y, 12, f"{'█' * o2_gen}{'░' * max(0, o2_use - o2_gen)}", curses.color_pair(CLR_GOOD if o2_ok else CLR_BAD))
    safe_addstr(win, y, 30, f"{o2_gen}/{o2_use} {'OK' if o2_ok else 'DEFICIT!'}", curses.color_pair(CLR_GOOD if o2_ok else CLR_BAD | curses.A_BOLD))

    y += 2
    safe_addstr(win, y, 2, "─── Modules ───", curses.color_pair(CLR_BORDER))
    y += 1
    for pos, mt in sorted(ship.modules.items()):
        m = MODULES[mt]
        crew_m = game.roster.get_assigned_to(pos)
        crew_txt = crew_m.name if crew_m else ("(need crew)" if m["crew"] > 0 else "—")
        pwr_txt = f"+{abs(m['pwr'])}" if m["pwr"] < 0 else f"-{m['pwr']}"
        safe_addstr(win, y, 4, f"{m['sym']} {m['name']:<14} Pwr:{pwr_txt:>3}  O2:{m['o2']:>+3}  Crew: {crew_txt}")
        y += 1
        if y > max_h - 5:
            safe_addstr(win, y, 4, "... more modules below ...", curses.color_pair(CLR_DIM))
            break

    y = max_h - 4
    safe_addstr(win, y, 2, "─── Crew Status ───", curses.color_pair(CLR_BORDER))
    y += 1
    for m in game.roster.members[:4]:
        status = m.status_text()
        safe_addstr(win, y, 4, f"{m.name:<20} HP:{m.health}%  Morale:{m.morale}%  {status}")
        y += 1

    render_footer(win, game, max_w, max_h)


RENDERERS = {
    "ship": render_ship_view,
    "map": render_map_view,
    "crew": render_crew_view,
    "cargo": render_cargo_view,
    "systems": render_systems_view,
}


def render(win, game):
    max_h, max_w = win.getmaxyx()
    win.clear()
    renderer = RENDERERS.get(game.screen, render_ship_view)
    renderer(win, game, max_w, max_h)
    win.refresh()
