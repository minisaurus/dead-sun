import pygame
import sys
from ui.renderer import Renderer, SCREEN_W, SCREEN_H, TILE_SIZE
from world.game_state import GameState
from data.config import SCREENS, EMPTY, FLOOR, HULL_COST
from data.modules import MODULES, REFINE_RECIPES


def _count_build_options(game):
    tile = game.ship.get_tile(game.cursor_r, game.cursor_c)
    if tile == EMPTY:
        return 1
    elif tile == FLOOR:
        return len([k for k in MODULES if k != "cockpit"])
    return 0


def _execute_build(game):
    r, c = game.cursor_r, game.cursor_c
    ship = game.ship
    tile = ship.get_tile(r, c)
    choice = game.build_choice

    if tile == EMPTY and ship.is_buildable(r, c):
        if choice == 0:
            if game.can_afford(HULL_COST):
                game.spend(HULL_COST)
                ship.build_hull(r, c)
                game.show_message("Extended hull.")
                game.log_event("Extended hull.")
            else:
                game.show_message("Not enough resources.")
    elif tile == FLOOR and ship.can_place_module(r, c):
        modules = [k for k in MODULES if k != "cockpit"]
        if 0 <= choice < len(modules):
            mtype = modules[choice]
            cost = MODULES[mtype]["cost"]
            if game.can_afford(cost):
                game.spend(cost)
                ship.place_module(r, c, mtype)
                game.show_message(f"Built {MODULES[mtype]['name']}!")
                game.log_event(f"Built {MODULES[mtype]['name']} module.")
            else:
                game.show_message("Not enough resources.")

    game.build_menu_open = False


def _assign_crew(game):
    if game.selected_crew >= len(game.roster.members):
        return
    member = game.roster.members[game.selected_crew]
    if member.is_assigned():
        member.unassign()

    modules_needing_crew = []
    for pos, mt in game.ship.modules.items():
        m = MODULES[mt]
        if m["crew"] > 0 and game.roster.get_assigned_to(pos) is None:
            modules_needing_crew.append((pos, mt))

    if not modules_needing_crew:
        game.show_message("No modules need crew.")
        return

    member.assign(modules_needing_crew[0][0])
    mt = modules_needing_crew[0][1]
    game.show_message(f"Assigned {member.name} to {MODULES[mt]['name']}.")
    game.log_event(f"{member.name} assigned to {MODULES[mt]['name']}.")


def handle_ship_input(game, key):
    ship = game.ship

    if game.build_menu_open:
        if key == pygame.K_ESCAPE or key == pygame.K_q:
            game.build_menu_open = False
        elif key in (pygame.K_UP, pygame.K_w):
            game.build_choice = max(0, game.build_choice - 1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            max_opt = _count_build_options(game) - 1
            game.build_choice = min(max_opt, game.build_choice + 1)
        elif key == pygame.K_RETURN:
            _execute_build(game)
        return

    if key in (pygame.K_UP, pygame.K_w):
        game.cursor_r = max(0, game.cursor_r - 1)
    elif key in (pygame.K_DOWN, pygame.K_s):
        game.cursor_r = min(ship.height - 1, game.cursor_r + 1)
    elif key in (pygame.K_LEFT, pygame.K_a):
        game.cursor_c = max(0, game.cursor_c - 1)
    elif key in (pygame.K_RIGHT, pygame.K_d):
        game.cursor_c = min(ship.width - 1, game.cursor_c + 1)
    elif key == pygame.K_b:
        tile = ship.get_tile(game.cursor_r, game.cursor_c)
        if tile == EMPTY and ship.is_buildable(game.cursor_r, game.cursor_c):
            game.build_menu_open = True
            game.build_choice = 0
        elif tile == FLOOR and ship.can_place_module(game.cursor_r, game.cursor_c):
            game.build_menu_open = True
            game.build_choice = 0
        else:
            game.show_message("Can't build here.")
    elif key == pygame.K_x:
        module = ship.get_module_at(game.cursor_r, game.cursor_c)
        if module:
            crew_m = game.roster.get_assigned_to((game.cursor_r, game.cursor_c))
            if crew_m:
                crew_m.unassign()
            refund = ship.remove_module(game.cursor_r, game.cursor_c)
            game.receive(refund)
            parts = ", ".join(f"{v} {k}" for k, v in refund.items())
            game.show_message(f"Removed {module}. Refunded: {parts}")
            game.log_event(f"Removed {module} module.")
        else:
            game.show_message("Nothing to remove here.")


def handle_map_input(game, key):
    if key in (pygame.K_UP, pygame.K_w):
        game.selected_location = max(0, game.selected_location - 1)
    elif key in (pygame.K_DOWN, pygame.K_s):
        game.selected_location = min(len(game.system.locations) - 1, game.selected_location + 1)
    elif key in (pygame.K_n, pygame.K_RETURN):
        if game.selected_location < len(game.system.locations):
            dest = game.system.locations[game.selected_location]
            if dest.name != game.current_location.name:
                game.do_travel(dest)
    elif key == pygame.K_m:
        game.do_mine()
    elif key == pygame.K_r:
        if game.ship.count_module("refinery") > 0:
            recipes = list(REFINE_RECIPES.keys())
            if game.selected_recipe < len(recipes):
                game.do_refine(recipes[game.selected_recipe])


def handle_crew_input(game, key):
    if key in (pygame.K_UP, pygame.K_w):
        game.selected_crew = max(0, game.selected_crew - 1)
    elif key in (pygame.K_DOWN, pygame.K_s):
        game.selected_crew = min(len(game.roster.members) - 1, game.selected_crew + 1)
    elif key == pygame.K_a:
        _assign_crew(game)
    elif key == pygame.K_u:
        if 0 <= game.selected_crew < len(game.roster.members):
            m = game.roster.members[game.selected_crew]
            if m.is_assigned():
                m.unassign()
                game.show_message(f"Unassigned {m.name}.")


def handle_cargo_input(game, key):
    if game.ship.count_module("refinery") > 0:
        recipes = list(REFINE_RECIPES.keys())
        if key in (pygame.K_UP, pygame.K_w):
            game.selected_recipe = max(0, game.selected_recipe - 1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            game.selected_recipe = min(len(recipes) - 1, game.selected_recipe + 1)
        elif key == pygame.K_r:
            if game.selected_recipe < len(recipes):
                game.do_refine(recipes[game.selected_recipe])


def handle_input(game, key, renderer):
    if key == pygame.K_TAB:
        idx = SCREENS.index(game.screen) if game.screen in SCREENS else 0
        idx = (idx + 1) % len(SCREENS)
        game.screen = SCREENS[idx]
        game.build_menu_open = False
        return
    elif key == pygame.K_q and not game.build_menu_open:
        game.running = False
        return
    elif key in (pygame.K_SLASH, pygame.K_h):
        game.show_message("TAB:switch WASD:move Q:quit", 5)
        return

    handlers = {
        "ship": handle_ship_input,
        "map": handle_map_input,
        "crew": handle_crew_input,
        "cargo": handle_cargo_input,
        "systems": None,
    }
    handler = handlers.get(game.screen)
    if handler:
        handler(game, key)


def run_game():
    renderer = Renderer()
    game = GameState()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_input(game, event.key, renderer)

        game.running = running
        renderer.render(game)
        renderer.clock.tick(renderer.fps)

    pygame.quit()
    sys.exit()
