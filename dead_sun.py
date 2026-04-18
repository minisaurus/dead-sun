#!/usr/bin/env python3
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'x11')

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.game_loop import run_game


def main():
    print("DEAD SUN - Launching pixel graphics...")
    print("Access via browser at http://localhost:8080/vnc.html")
    try:
        run_game()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Dead Sun ended.")


if __name__ == "__main__":
    main()
