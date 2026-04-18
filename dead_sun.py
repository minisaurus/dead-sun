#!/usr/bin/env python3
"""Dead Sun - A terminal spaceship command/colony game."""

import curses
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import run_game


def main():
    print("☀️  DEAD SUN ☀️")
    print("A terminal spaceship command/colony game")
    print()
    print("Controls:")
    print("  TAB     - Switch screens (Ship/Map/Crew/Cargo/Systems)")
    print("  WASD    - Move cursor / navigate lists")
    print("  Enter   - Confirm action")
    print("  B       - Build (Ship screen)")
    print("  X       - Remove module (Ship screen)")
    print("  N       - Navigate (Map screen)")
    print("  M       - Mine (Map screen)")
    print("  R       - Refine (Map/Cargo screen)")
    print("  A       - Assign crew (Crew screen)")
    print("  U       - Unassign crew (Crew screen)")
    print("  Q       - Quit")
    print()
    print("Starting...")
    try:
        curses.wrapper(run_game)
    except KeyboardInterrupt:
        print("\nDead Sun ended. The sun dies, but you survive... for now.")


if __name__ == "__main__":
    main()
