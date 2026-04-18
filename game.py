import curses
from data import MODULES, SCREENS, REFINE_RECIPES, EMPTY, FLOOR
from data.config import HULL_COST, CLR_TITLE, CLR_GOOD, CLR_WARN, CLR_BAD, CLR_HIGHLIGHT, CLR_DIM, CLR_MODULE, CLR_CURSOR, CLR_BORDER
from render import init_colors, render


def handle_ship_input(game, key):
    ship = game.ship

    if game.build_menu_open:
        if key == 27 or key == ord('q'):
            game.build_menu_open = False
        elif key == curses.KEY_UP or key == ord('w'):
            game.build_choice = max(0, game.build_choice - 1)
        elif key == curses.KEY_DOWN or key == ord('s'):
            # Count available options
            tile = ship.get_tile(game.cursor_r, game.cursor_c)
            max_opt = _count_build_options(game) - 1
            game.build_choice = min(max_opt, game.build_choice + 1)
        elif key == ord('\n') or key == curses.KEY_ENTER:
            _execute_build(game)
        return

    if key == curses.KEY_UP or key == ord('w'):
        game.cursor_r = max(0, game.cursor_r - 1)
    elif key == curses.KEY_DOWN or key == ord('s'):
        game.cursor_r = min(ship.height - 1, game.cursor_r + 1)
    elif key == curses.KEY_LEFT or key == ord('a'):
        game.cursor_c = max(0, game.cursor_c - 1)
    elif key == curses.KEY_RIGHT or key == ord('d'):
        game.cursor_c = min(ship.width - 1, game.cursor_c + 1)
    elif key == ord('b'):
        tile = ship.get_tile(game.cursor_r, game.cursor_c)
        if tile == EMPTY and ship.is_buildable(game.cursor_r, game.cursor_c):
            game.build_menu_open = True
            game.build_choice = 0
        elif tile == FLOOR and ship.can_place_module(game.cursor_r, game.cursor_c):
            game.build_menu_open = True
            game.build_choice = 0
        else:
            game.show_message("Can't build here.")
    elif key == ord('x'):
        module = ship.get_module_at(game.cursor_r, game.cursor_c)
        if module:
            # Unassign crew first
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


def _count_build_options(game):
    tile = game.ship.get_tile(game.cursor_r, game.cursor_c)
    if tile == EMPTY:
        return 1  # hull extension
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


def handle_map_input(game, key):
    locs = [l for l in game.system.locations if l.loc_type != "star"]
    if key == curses.KEY_UP or key == ord('w'):
        game.selected_location = max(0, game.selected_location - 1)
    elif key == curses.KEY_DOWN or key == ord('s'):
        game.selected_location = min(len(game.system.locations) - 1, game.selected_location + 1)
    elif key == ord('n') or key == ord('\n') or key == curses.KEY_ENTER:
        if game.selected_location < len(game.system.locations):
            dest = game.system.locations[game.selected_location]
            if dest.name != game.current_location.name:
                game.do_travel(dest)
    elif key == ord('m'):
        game.do_mine()
    elif key == ord('r'):
        if game.ship.count_module("refinery") > 0:
            recipes = list(REFINE_RECIPES.keys())
            if game.selected_recipe < len(recipes):
                game.do_refine(recipes[game.selected_recipe])


def handle_crew_input(game, key):
    if key == curses.KEY_UP or key == ord('w'):
        game.selected_crew = max(0, game.selected_crew - 1)
    elif key == curses.KEY_DOWN or key == ord('s'):
        game.selected_crew = min(len(game.roster.members) - 1, game.selected_crew + 1)
    elif key == ord('a'):
        _assign_crew(game)
    elif key == ord('u'):
        if 0 <= game.selected_crew < len(game.roster.members):
            m = game.roster.members[game.selected_crew]
            if m.is_assigned():
                m.unassign()
                game.show_message(f"Unassigned {m.name}.")


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


def handle_cargo_input(game, key):
    if game.ship.count_module("refinery") > 0:
        recipes = list(REFINE_RECIPES.keys())
        if key == curses.KEY_UP or key == ord('w'):
            game.selected_recipe = max(0, game.selected_recipe - 1)
        elif key == curses.KEY_DOWN or key == ord('s'):
            game.selected_recipe = min(len(recipes) - 1, game.selected_recipe + 1)
        elif key == ord('r'):
            if game.selected_recipe < len(recipes):
                game.do_refine(recipes[game.selected_recipe])


def handle_input(game, key):
    # Global keys
    if key == ord('\t'):
        idx = SCREENS.index(game.screen) if game.screen in SCREENS else 0
        idx = (idx + 1) % len(SCREENS)
        game.screen = SCREENS[idx]
        game.build_menu_open = False
        return
    elif key == ord('q') and not game.build_menu_open:
        game.running = False
        return
    elif key == ord('?') or key == ord('h'):
        game.show_message("TAB:switch WASD:move Q:quit", 5)
        return

    # Screen-specific
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


def run_game(stdscr):
    from world.game_state import GameState

    curses.curs_set(0)
    curses.noecho()
    curses.raw()
    stdscr.keypad(True)
    stdscr.timeout(100)

    init_colors()

    game = GameState()
    render(stdscr, game)

    while game.running:
        try:
            key = stdscr.getch()
        except Exception:
            key = -1

        if key != -1:
            handle_input(game, key)
            render(stdscr, game)
