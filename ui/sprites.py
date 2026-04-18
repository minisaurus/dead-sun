import pygame
import random
import math

TILE_SIZE = 32

COLORS = {
    "bg": (10, 10, 25),
    "hull": (60, 65, 80),
    "hull_light": (80, 85, 100),
    "floor": (35, 38, 50),
    "floor_light": (45, 48, 60),
    "cursor": (255, 220, 80),
    "border": (40, 80, 140),
    "border_light": (60, 110, 180),
    "text": (200, 210, 230),
    "text_dim": (100, 110, 130),
    "good": (80, 200, 120),
    "warn": (220, 180, 60),
    "bad": (220, 60, 60),
    "title": (80, 200, 255),
    "module_bg": (50, 55, 75),
    "white": (240, 240, 245),
    "star": (200, 200, 220),
    "star_dim": (80, 80, 100),
}

MODULE_COLORS = {
    "cockpit": {"primary": (60, 180, 255), "secondary": (30, 100, 180), "accent": (200, 230, 255)},
    "bridge": {"primary": (80, 200, 255), "secondary": (40, 120, 200), "accent": (220, 240, 255)},
    "reactor": {"primary": (255, 200, 40), "secondary": (200, 140, 20), "accent": (255, 240, 150)},
    "solar_panel": {"primary": (60, 120, 200), "secondary": (40, 80, 160), "accent": (150, 200, 255)},
    "engine": {"primary": (200, 100, 40), "secondary": (150, 60, 20), "accent": (255, 160, 80)},
    "ftl_drive": {"primary": (160, 80, 255), "secondary": (100, 40, 180), "accent": (200, 160, 255)},
    "life_support": {"primary": (60, 200, 160), "secondary": (30, 140, 100), "accent": (160, 240, 220)},
    "habitat": {"primary": (120, 180, 100), "secondary": (70, 130, 60), "accent": (180, 220, 160)},
    "medbay": {"primary": (255, 80, 80), "secondary": (200, 40, 40), "accent": (255, 180, 180)},
    "cargo_bay": {"primary": (160, 140, 100), "secondary": (120, 100, 70), "accent": (200, 180, 150)},
    "mining_drill": {"primary": (180, 140, 60), "secondary": (130, 100, 40), "accent": (220, 200, 120)},
    "refinery": {"primary": (255, 100, 40), "secondary": (200, 60, 20), "accent": (255, 180, 120)},
    "scanner": {"primary": (80, 200, 255), "secondary": (40, 140, 200), "accent": (180, 230, 255)},
    "farm": {"primary": (80, 180, 60), "secondary": (50, 130, 30), "accent": (160, 220, 120)},
    "workshop": {"primary": (160, 160, 180), "secondary": (110, 110, 130), "accent": (200, 200, 220)},
    "shield": {"primary": (100, 140, 255), "secondary": (60, 80, 200), "accent": (180, 200, 255)},
    "armor_plating": {"primary": (120, 120, 140), "secondary": (80, 80, 100), "accent": (160, 160, 180)},
    "laser_turret": {"primary": (255, 60, 60), "secondary": (200, 30, 30), "accent": (255, 150, 100)},
}


def _draw_cockpit(surface, x, y, ts, c):
    cx, cy = x + ts // 2, y + ts // 2 - 1
    pygame.draw.rect(surface, c["secondary"], (x + 5, y + 3, ts - 10, ts - 6))
    pygame.draw.rect(surface, c["primary"], (x + 7, y + 5, ts - 14, ts - 10))
    pygame.draw.circle(surface, c["accent"], (cx, cy), 7)
    pygame.draw.circle(surface, c["primary"], (cx, cy), 5)
    pygame.draw.circle(surface, c["accent"], (cx, cy), 2)
    pygame.draw.rect(surface, c["secondary"], (x + 8, y + ts - 8, ts - 16, 3))
    surface.set_at((cx - 3, y + ts - 7), c["accent"])
    surface.set_at((cx, y + ts - 7), COLORS["good"])
    surface.set_at((cx + 3, y + ts - 7), c["primary"])


def _draw_bridge(surface, x, y, ts, c):
    pygame.draw.rect(surface, c["secondary"], (x + 4, y + 8, ts - 8, ts - 12))
    pygame.draw.rect(surface, c["primary"], (x + 6, y + 10, 7, 5))
    pygame.draw.rect(surface, c["primary"], (x + ts // 2 - 3, y + 10, 6, 5))
    pygame.draw.rect(surface, c["primary"], (x + ts - 13, y + 10, 7, 5))
    surface.set_at((x + 9, y + 12), c["accent"])
    surface.set_at((x + ts // 2, y + 12), c["accent"])
    surface.set_at((x + ts - 9, y + 12), c["accent"])
    pygame.draw.line(surface, c["primary"], (x + ts // 2, y + 2), (x + ts // 2, y + 8), 2)
    pygame.draw.circle(surface, c["accent"], (x + ts // 2, y + 2), 3)
    pygame.draw.rect(surface, c["primary"], (x + 7, y + 18, ts - 14, 3))
    surface.set_at((x + 10, y + 19), c["accent"])
    surface.set_at((x + ts - 11, y + 19), c["accent"])


def _draw_reactor(surface, x, y, ts, c):
    cx, cy = x + ts // 2, y + ts // 2
    pygame.draw.circle(surface, c["secondary"], (cx, cy), 11)
    pygame.draw.circle(surface, c["primary"], (cx, cy), 7)
    pygame.draw.circle(surface, c["accent"], (cx, cy), 3)
    for deg in range(0, 360, 45):
        rad = math.radians(deg)
        x1 = cx + int(8 * math.cos(rad))
        y1 = cy + int(8 * math.sin(rad))
        x2 = cx + int(12 * math.cos(rad))
        y2 = cy + int(12 * math.sin(rad))
        pygame.draw.line(surface, c["primary"], (x1, y1), (x2, y2), 2)
    pygame.draw.circle(surface, c["accent"], (cx, cy), 1)


def _draw_solar_panel(surface, x, y, ts, c):
    pygame.draw.rect(surface, c["secondary"], (x + 2, y + 4, ts - 4, ts - 8))
    pygame.draw.rect(surface, c["primary"], (x + 4, y + 6, ts - 8, ts - 12))
    pygame.draw.line(surface, c["secondary"], (x + ts // 3 + 1, y + 6), (x + ts // 3 + 1, y + ts - 6), 1)
    pygame.draw.line(surface, c["secondary"], (x + 2 * ts // 3, y + 6), (x + 2 * ts // 3, y + ts - 6), 1)
    pygame.draw.line(surface, c["secondary"], (x + 4, y + ts // 2), (x + ts - 4, y + ts // 2), 1)
    pygame.draw.rect(surface, c["accent"], (x + 2, y + 2, ts - 4, 3))
    surface.set_at((x + ts // 6, y + ts // 2 - 2), c["accent"])
    surface.set_at((x + ts // 2, y + ts // 3), c["accent"])
    surface.set_at((x + ts * 5 // 6, y + ts // 2 + 2), c["accent"])
    surface.set_at((x + ts // 3, y + ts * 2 // 3), c["accent"])


def _draw_engine(surface, x, y, ts, c):
    pygame.draw.rect(surface, COLORS["hull"], (x + 8, y + 2, ts - 16, 10))
    pygame.draw.rect(surface, c["secondary"], (x + 10, y + 4, ts - 20, 6))
    pygame.draw.polygon(surface, c["secondary"], [
        (x + 6, y + 12), (x + ts - 6, y + 12),
        (x + ts - 10, y + 20), (x + 10, y + 20)
    ])
    pygame.draw.polygon(surface, c["primary"], [
        (x + 10, y + 18), (x + ts - 10, y + 18),
        (x + ts - 12, y + 28), (x + 12, y + 28)
    ])
    pygame.draw.polygon(surface, c["accent"], [
        (x + 12, y + 24), (x + ts - 12, y + 24),
        (x + ts - 14, y + 30), (x + 14, y + 30)
    ])
    for i in range(3):
        surface.set_at((x + ts // 2 - 2 + i * 2, min(y + 30, y + ts - 1)), c["accent"])


def _draw_ftl_drive(surface, x, y, ts, c):
    cx, cy = x + ts // 2, y + ts // 2
    pygame.draw.circle(surface, c["secondary"], (cx, cy), 12)
    pygame.draw.circle(surface, c["primary"], (cx, cy), 9)
    pygame.draw.circle(surface, c["accent"], (cx, cy), 6)
    pygame.draw.circle(surface, c["secondary"], (cx, cy), 3)
    pygame.draw.circle(surface, c["primary"], (cx, cy), 1)
    for deg in range(0, 360, 30):
        rad = math.radians(deg)
        x1 = cx + int(4 * math.cos(rad))
        y1 = cy + int(4 * math.sin(rad))
        x2 = cx + int(9 * math.cos(rad))
        y2 = cy + int(9 * math.sin(rad))
        pygame.draw.line(surface, c["accent"], (x1, y1), (x2, y2), 1)


def _draw_life_support(surface, x, y, ts, c):
    pygame.draw.rect(surface, c["primary"], (x + ts // 2 - 2, y + 6, 4, ts - 12))
    pygame.draw.rect(surface, c["primary"], (x + 6, y + ts // 2 - 2, ts - 12, 4))
    pygame.draw.rect(surface, c["accent"], (x + ts // 2 - 1, y + 7, 2, ts - 14))
    pygame.draw.rect(surface, c["accent"], (x + 7, y + ts // 2 - 1, ts - 14, 2))
    pygame.draw.circle(surface, c["accent"], (x + 8, y + 8), 2)
    pygame.draw.circle(surface, c["accent"], (x + ts - 9, y + 8), 2)
    pygame.draw.circle(surface, c["accent"], (x + 8, y + ts - 9), 2)
    pygame.draw.circle(surface, c["accent"], (x + ts - 9, y + ts - 9), 2)
    pygame.draw.circle(surface, c["primary"], (x + 6, y + ts // 2 + 5), 1)
    pygame.draw.circle(surface, c["primary"], (x + ts - 7, y + ts // 2 - 5), 1)


def _draw_habitat(surface, x, y, ts, c):
    pygame.draw.polygon(surface, c["secondary"], [
        (x + ts // 2, y + 3),
        (x + 4, y + 14),
        (x + ts - 4, y + 14)
    ])
    pygame.draw.polygon(surface, c["primary"], [
        (x + ts // 2, y + 5),
        (x + 6, y + 13),
        (x + ts - 6, y + 13)
    ])
    pygame.draw.rect(surface, c["secondary"], (x + 6, y + 14, ts - 12, ts - 18))
    pygame.draw.rect(surface, c["primary"], (x + 8, y + 16, ts - 16, ts - 22))
    pygame.draw.rect(surface, c["accent"], (x + ts // 2 - 3, y + 18, 6, 5))
    pygame.draw.rect(surface, c["accent"], (x + 10, y + 22, 4, 4))
    pygame.draw.rect(surface, c["accent"], (x + ts - 14, y + 22, 4, 4))


def _draw_medbay(surface, x, y, ts, c):
    pygame.draw.rect(surface, COLORS["white"], (x + 5, y + 5, ts - 10, ts - 10))
    pygame.draw.rect(surface, c["primary"], (x + ts // 2 - 2, y + 6, 4, ts - 12))
    pygame.draw.rect(surface, c["primary"], (x + 6, y + ts // 2 - 2, ts - 12, 4))
    pygame.draw.rect(surface, c["secondary"], (x + ts // 2 - 1, y + 7, 2, ts - 14))
    pygame.draw.rect(surface, c["secondary"], (x + 7, y + ts // 2 - 1, ts - 14, 2))
    pygame.draw.rect(surface, c["primary"], (x + 5, y + 5, ts - 10, ts - 10), 1)


def _draw_cargo_bay(surface, x, y, ts, c):
    pygame.draw.rect(surface, c["primary"], (x + 4, y + 4, ts - 8, ts - 8))
    pygame.draw.line(surface, c["secondary"], (x + 4, y + 4), (x + ts - 4, y + ts - 4), 2)
    pygame.draw.line(surface, c["secondary"], (x + ts - 4, y + 4), (x + 4, y + ts - 4), 2)
    pygame.draw.rect(surface, c["accent"], (x + 4, y + 4, ts - 8, ts - 8), 1)
    surface.set_at((x + 5, y + 5), c["accent"])
    surface.set_at((x + ts - 6, y + 5), c["accent"])
    surface.set_at((x + 5, y + ts - 6), c["accent"])
    surface.set_at((x + ts - 6, y + ts - 6), c["accent"])
    surface.set_at((x + ts // 2, y + 4), c["accent"])
    surface.set_at((x + ts // 2, y + ts - 5), c["accent"])
    surface.set_at((x + 4, y + ts // 2), c["accent"])
    surface.set_at((x + ts - 5, y + ts // 2), c["accent"])


def _draw_mining_drill(surface, x, y, ts, c):
    pygame.draw.rect(surface, c["secondary"], (x + 8, y + 3, ts - 16, 8))
    pygame.draw.rect(surface, c["primary"], (x + 10, y + 5, ts - 20, 4))
    pygame.draw.polygon(surface, c["secondary"], [
        (x + 8, y + 11),
        (x + ts - 8, y + 11),
        (x + ts // 2, y + 28)
    ])
    pygame.draw.polygon(surface, c["primary"], [
        (x + 10, y + 11),
        (x + ts - 10, y + 11),
        (x + ts // 2, y + 26)
    ])
    pygame.draw.polygon(surface, c["accent"], [
        (x + 12, y + 11),
        (x + ts - 12, y + 11),
        (x + ts // 2, y + 24)
    ])
    surface.set_at((x + ts // 2, y + 27), c["accent"])
    for i in range(-1, 2):
        surface.set_at((x + ts // 2 + i, y + 28), c["primary"])


def _draw_refinery(surface, x, y, ts, c):
    pygame.draw.rect(surface, c["secondary"], (x + 5, y + 12, ts - 10, ts - 16))
    pygame.draw.rect(surface, c["primary"], (x + 7, y + 14, ts - 14, ts - 20))
    pygame.draw.polygon(surface, c["primary"], [
        (x + ts // 2 - 4, y + 3),
        (x + ts // 2 + 4, y + 3),
        (x + ts // 2 + 2, y + 12),
        (x + ts // 2 - 2, y + 12)
    ])
    pygame.draw.polygon(surface, c["accent"], [
        (x + ts // 2 - 2, y + 5),
        (x + ts // 2 + 2, y + 5),
        (x + ts // 2 + 1, y + 11),
        (x + ts // 2 - 1, y + 11)
    ])
    surface.set_at((x + ts // 2, y + 4), c["accent"])
    surface.set_at((x + ts // 2 - 1, y + 3), c["accent"])
    surface.set_at((x + ts // 2 + 1, y + 3), c["accent"])
    surface.set_at((x + 9, y + 18), c["accent"])
    surface.set_at((x + ts - 10, y + 18), c["accent"])
    pygame.draw.rect(surface, c["secondary"], (x + 5, y + 12, ts - 10, ts - 16), 1)


def _draw_scanner(surface, x, y, ts, c):
    cx = x + ts // 2
    pygame.draw.ellipse(surface, c["primary"], (x + 3, y + 4, ts - 6, 14))
    pygame.draw.rect(surface, COLORS["module_bg"], (x + 3, y + 4, ts - 6, 7))
    pygame.draw.ellipse(surface, c["secondary"], (x + 3, y + 4, ts - 6, 14), 1)
    pygame.draw.line(surface, c["secondary"], (cx, y + 14), (cx, y + ts - 5), 3)
    pygame.draw.rect(surface, c["secondary"], (cx - 7, y + ts - 6, 14, 3))
    pygame.draw.circle(surface, c["accent"], (cx, y + 12), 2)
    surface.set_at((cx - 5, y + 10), c["accent"])
    surface.set_at((cx + 5, y + 10), c["accent"])
    surface.set_at((cx - 3, y + 8), c["accent"])
    surface.set_at((cx + 3, y + 8), c["accent"])


def _draw_farm(surface, x, y, ts, c):
    pygame.draw.rect(surface, c["secondary"], (x + 3, y + ts - 10, ts - 6, 7))
    pygame.draw.rect(surface, c["primary"], (x + ts // 2 - 1, y + 10, 2, ts - 20))
    pygame.draw.polygon(surface, c["primary"], [
        (x + ts // 2, y + 5),
        (x + ts // 2 - 7, y + 14),
        (x + ts // 2 + 7, y + 14)
    ])
    pygame.draw.polygon(surface, c["accent"], [
        (x + ts // 2, y + 7),
        (x + ts // 2 - 5, y + 13),
        (x + ts // 2 + 5, y + 13)
    ])
    pygame.draw.polygon(surface, c["primary"], [
        (x + ts // 2, y + 11),
        (x + ts // 2 - 6, y + 18),
        (x + ts // 2 + 6, y + 18)
    ])
    pygame.draw.polygon(surface, c["accent"], [
        (x + ts // 2, y + 13),
        (x + ts // 2 - 4, y + 17),
        (x + ts // 2 + 4, y + 17)
    ])
    pygame.draw.circle(surface, c["accent"], (x + ts // 2 - 4, y + 4), 2)
    pygame.draw.circle(surface, c["accent"], (x + ts // 2 + 4, y + 4), 2)
    pygame.draw.circle(surface, c["primary"], (x + ts // 2, y + 3), 1)


def _draw_workshop(surface, x, y, ts, c):
    cx, cy = x + ts // 2, y + ts // 2
    for deg in range(0, 360, 45):
        rad = math.radians(deg)
        x1 = cx + int(7 * math.cos(rad))
        y1 = cy + int(7 * math.sin(rad))
        x2 = cx + int(12 * math.cos(rad))
        y2 = cy + int(12 * math.sin(rad))
        pygame.draw.line(surface, c["secondary"], (x1, y1), (x2, y2), 3)
    pygame.draw.circle(surface, c["primary"], (cx, cy), 8)
    pygame.draw.circle(surface, c["accent"], (cx, cy), 5)
    pygame.draw.circle(surface, c["secondary"], (cx, cy), 2)
    surface.set_at((cx, cy), c["accent"])
    for deg in range(0, 360, 45):
        rad = math.radians(deg)
        x1 = cx + int(7 * math.cos(rad))
        y1 = cy + int(7 * math.sin(rad))
        x2 = cx + int(12 * math.cos(rad))
        y2 = cy + int(12 * math.sin(rad))
        pygame.draw.line(surface, c["primary"], (x1, y1), (x2, y2), 1)


def _draw_shield(surface, x, y, ts, c):
    cx, cy = x + ts // 2, y + ts // 2
    outer = []
    inner1 = []
    inner2 = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        outer.append((cx + int(12 * math.cos(angle)), cy + int(12 * math.sin(angle))))
        inner1.append((cx + int(9 * math.cos(angle)), cy + int(9 * math.sin(angle))))
        inner2.append((cx + int(5 * math.cos(angle)), cy + int(5 * math.sin(angle))))
    pygame.draw.polygon(surface, c["secondary"], outer)
    pygame.draw.polygon(surface, c["primary"], inner1)
    pygame.draw.polygon(surface, c["accent"], inner2)
    pygame.draw.polygon(surface, c["secondary"], outer, 1)
    surface.set_at((cx, cy), COLORS["white"])


def _draw_armor_plating(surface, x, y, ts, c):
    pygame.draw.rect(surface, c["secondary"], (x + 3, y + 3, ts - 6, ts - 6))
    pygame.draw.rect(surface, c["primary"], (x + 5, y + 5, ts - 10, ts - 10))
    pygame.draw.rect(surface, c["accent"], (x + 7, y + 7, ts - 14, ts - 14))
    pygame.draw.rect(surface, c["primary"], (x + 3, y + 3, ts - 6, ts - 6), 1)
    for rx, ry in [
        (x + 6, y + 6), (x + ts - 7, y + 6),
        (x + 6, y + ts - 7), (x + ts - 7, y + ts - 7),
        (x + ts // 2, y + 6), (x + ts // 2, y + ts - 7),
        (x + 6, y + ts // 2), (x + ts - 7, y + ts // 2),
    ]:
        pygame.draw.circle(surface, c["secondary"], (rx, ry), 1)


def _draw_laser_turret(surface, x, y, ts, c):
    cx = x + ts // 2
    pygame.draw.rect(surface, COLORS["hull"], (x + 4, y + ts - 10, ts - 8, 6))
    pygame.draw.rect(surface, c["secondary"], (cx - 4, y + 6, 8, ts - 16))
    pygame.draw.rect(surface, c["primary"], (cx - 3, y + 4, 6, ts - 14))
    pygame.draw.rect(surface, c["accent"], (cx - 5, y + 2, 10, 5))
    pygame.draw.rect(surface, c["primary"], (cx - 3, y + 3, 6, 3))
    pygame.draw.circle(surface, c["accent"], (cx, y + 3), 2)
    surface.set_at((cx, y + 1), c["accent"])
    surface.set_at((cx - 1, y + 1), c["primary"])
    surface.set_at((cx + 1, y + 1), c["primary"])
    pygame.draw.rect(surface, c["secondary"], (x + 6, y + ts - 10, 4, 6))
    pygame.draw.rect(surface, c["secondary"], (x + ts - 10, y + ts - 10, 4, 6))


_MODULE_DRAWERS = {
    "cockpit": _draw_cockpit,
    "bridge": _draw_bridge,
    "reactor": _draw_reactor,
    "solar_panel": _draw_solar_panel,
    "engine": _draw_engine,
    "ftl_drive": _draw_ftl_drive,
    "life_support": _draw_life_support,
    "habitat": _draw_habitat,
    "medbay": _draw_medbay,
    "cargo_bay": _draw_cargo_bay,
    "mining_drill": _draw_mining_drill,
    "refinery": _draw_refinery,
    "scanner": _draw_scanner,
    "farm": _draw_farm,
    "workshop": _draw_workshop,
    "shield": _draw_shield,
    "armor_plating": _draw_armor_plating,
    "laser_turret": _draw_laser_turret,
}


def draw_module_sprite(surface, module_type, x, y, tile_size=32):
    c = MODULE_COLORS.get(module_type)
    if c is None:
        return
    ts = tile_size
    pygame.draw.rect(surface, COLORS["module_bg"], (x, y, ts, ts))
    pygame.draw.rect(surface, c["secondary"], (x, y, ts, ts), 1)
    drawer = _MODULE_DRAWERS.get(module_type)
    if drawer:
        drawer(surface, x, y, ts, c)


def draw_floor_tile(surface, x, y, tile_size=32):
    ts = tile_size
    pygame.draw.rect(surface, COLORS["floor"], (x, y, ts, ts))
    pygame.draw.rect(surface, COLORS["floor_light"], (x, y, ts, 1))
    pygame.draw.rect(surface, COLORS["floor_light"], (x, y, 1, ts))
    pygame.draw.line(surface, COLORS["floor_light"],
                     (x + ts // 2, y + 1), (x + ts // 2, y + ts - 2), 1)
    pygame.draw.line(surface, COLORS["floor_light"],
                     (x + 1, y + ts // 2), (x + ts - 2, y + ts // 2), 1)


def draw_empty_tile(surface, x, y, tile_size=32):
    ts = tile_size
    pygame.draw.rect(surface, COLORS["bg"], (x, y, ts, ts))


def draw_cursor(surface, x, y, tile_size=32):
    ts = tile_size
    pygame.draw.rect(surface, COLORS["cursor"], (x, y, ts, ts), 2)
    pygame.draw.line(surface, COLORS["cursor"], (x, y), (x + 4, y), 2)
    pygame.draw.line(surface, COLORS["cursor"], (x, y), (x, y + 4), 2)
    pygame.draw.line(surface, COLORS["cursor"], (x + ts - 1, y), (x + ts - 5, y), 2)
    pygame.draw.line(surface, COLORS["cursor"], (x + ts - 1, y), (x + ts - 1, y + 4), 2)
    pygame.draw.line(surface, COLORS["cursor"], (x, y + ts - 1), (x + 4, y + ts - 1), 2)
    pygame.draw.line(surface, COLORS["cursor"], (x, y + ts - 1), (x, y + ts - 5), 2)
    pygame.draw.line(surface, COLORS["cursor"], (x + ts - 1, y + ts - 1), (x + ts - 5, y + ts - 1), 2)
    pygame.draw.line(surface, COLORS["cursor"], (x + ts - 1, y + ts - 1), (x + ts - 1, y + ts - 5), 2)


def generate_star_field(width, height, count=100):
    surf = pygame.Surface((width, height))
    surf.fill(COLORS["bg"])
    for _ in range(count):
        sx = random.randint(0, width - 1)
        sy = random.randint(0, height - 1)
        if random.random() < 0.3:
            color = COLORS["star"]
        else:
            color = COLORS["star_dim"]
        surf.set_at((sx, sy), color)
        if random.random() < 0.1:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = sx + dx, sy + dy
                if 0 <= nx < width and 0 <= ny < height:
                    surf.set_at((nx, ny), color)
    return surf


def draw_mini_planet(surface, x, y, planet_type, radius=8):
    if planet_type == "rocky_planet":
        pygame.draw.circle(surface, (140, 100, 60), (x, y), radius)
        pygame.draw.circle(surface, (120, 80, 40), (x, y), radius, 1)
        surface.set_at((x - 2, y - 2), (160, 120, 80))
        surface.set_at((x + 3, y + 1), (100, 70, 30))
        surface.set_at((x - 1, y + 3), (150, 110, 70))
        surface.set_at((x + 2, y - 3), (110, 75, 35))
        surface.set_at((x + 1, y + 2), (130, 90, 50))
        surface.set_at((x - 3, y), (120, 85, 45))
    elif planet_type == "gas_giant":
        pygame.draw.circle(surface, (180, 140, 100), (x, y), radius)
        for i in range(-radius + 2, radius - 1, 3):
            half_w = int(math.sqrt(max(0, radius * radius - i * i)))
            col = (160, 120, 80) if (i // 3) % 2 == 0 else (200, 165, 130)
            if half_w > 0:
                pygame.draw.line(surface, col, (x - half_w, y + i), (x + half_w, y + i), 1)
        pygame.draw.circle(surface, (200, 160, 120), (x + 2, y - 2), 2)
        pygame.draw.circle(surface, (180, 140, 100), (x, y), radius, 1)
    elif planet_type == "ice_moon":
        pygame.draw.circle(surface, (180, 210, 240), (x, y), radius)
        pygame.draw.circle(surface, (200, 230, 250), (x - 1, y - 1), radius - 2)
        pygame.draw.circle(surface, (160, 200, 230), (x, y), radius, 1)
        surface.set_at((x - 2, y + 1), (220, 240, 255))
        surface.set_at((x + 3, y - 1), (150, 190, 220))
        surface.set_at((x + 1, y + 3), (210, 235, 250))
    elif planet_type == "asteroid_field":
        positions = [
            (-3, -2, 3), (3, 1, 2), (1, -3, 2), (-1, 3, 2),
            (4, -2, 1), (-4, 2, 1), (0, 0, 1), (2, 3, 1),
        ]
        colors = [
            (100, 95, 90), (120, 115, 105), (90, 85, 80),
            (110, 100, 95), (130, 120, 110), (95, 90, 85),
            (105, 100, 95), (115, 108, 100),
        ]
        for i, (dx, dy, r) in enumerate(positions):
            if r >= 2:
                pygame.draw.circle(surface, colors[i % len(colors)], (x + dx, y + dy), r)
            else:
                surface.set_at((x + dx, y + dy), colors[i % len(colors)])
    elif planet_type == "station":
        pygame.draw.rect(surface, (140, 150, 170), (x - 6, y - 2, 12, 4))
        pygame.draw.rect(surface, (160, 170, 190), (x - 2, y - 5, 4, 10))
        pygame.draw.rect(surface, (120, 130, 150), (x - 4, y - 4, 8, 8), 1)
        surface.set_at((x, y), (200, 220, 255))
        surface.set_at((x - 5, y - 1), (100, 110, 130))
        surface.set_at((x + 5, y - 1), (100, 110, 130))
        surface.set_at((x - 3, y - 3), (180, 190, 210))
        surface.set_at((x + 3, y + 3), (180, 190, 210))
    elif planet_type == "star":
        pygame.draw.circle(surface, (255, 255, 200), (x, y), radius)
        pygame.draw.circle(surface, (255, 240, 150), (x, y), radius - 2)
        pygame.draw.circle(surface, (255, 255, 240), (x, y), max(1, radius - 4))
        for deg in range(0, 360, 45):
            rad = math.radians(deg)
            x1 = x + int((radius - 1) * math.cos(rad))
            y1 = y + int((radius - 1) * math.sin(rad))
            x2 = x + int((radius + 3) * math.cos(rad))
            y2 = y + int((radius + 3) * math.sin(rad))
            pygame.draw.line(surface, (255, 255, 200), (x1, y1), (x2, y2), 1)


def draw_resource_icon(surface, resource_type, x, y, size=16):
    s = size
    hs = s // 2
    if resource_type == "metal":
        pygame.draw.polygon(surface, (120, 120, 135), [
            (x + 2, y + 5), (x + hs, y + 1), (x + s - 2, y + 5)
        ])
        pygame.draw.polygon(surface, (150, 150, 165), [
            (x + 3, y + 5), (x + hs, y + 2), (x + s - 3, y + 5)
        ])
        pygame.draw.rect(surface, (140, 140, 155), (x + 2, y + 5, s - 4, s - 7))
        pygame.draw.rect(surface, (170, 170, 185), (x + 3, y + 5, s - 6, s - 9))
    elif resource_type == "electronics":
        pygame.draw.rect(surface, (40, 100, 50), (x + 2, y + 2, s - 4, s - 4))
        pygame.draw.rect(surface, (60, 140, 70), (x + 4, y + 4, s - 8, s - 8))
        pygame.draw.line(surface, (80, 180, 90), (x + hs, y + 2), (x + hs, y + s - 2), 1)
        pygame.draw.line(surface, (80, 180, 90), (x + 2, y + hs), (x + s - 2, y + hs), 1)
        surface.set_at((x + 4, y + 4), (100, 200, 110))
        surface.set_at((x + s - 5, y + 4), (100, 200, 110))
        surface.set_at((x + 4, y + s - 5), (100, 200, 110))
        surface.set_at((x + s - 5, y + s - 5), (100, 200, 110))
    elif resource_type == "fuel":
        pygame.draw.rect(surface, (180, 60, 30), (x + 3, y + 4, s - 6, s - 6))
        pygame.draw.rect(surface, (220, 80, 40), (x + 4, y + 5, s - 8, s - 8))
        pygame.draw.rect(surface, (180, 60, 30), (x + hs - 2, y + 1, 4, 4))
        pygame.draw.rect(surface, (255, 120, 60), (x + 5, y + hs, s - 10, 2))
        surface.set_at((x + hs - 1, y + 2), (220, 80, 40))
        surface.set_at((x + hs + 1, y + 2), (220, 80, 40))
    elif resource_type == "food":
        pygame.draw.rect(surface, (100, 70, 30), (x + 3, y + hs, s - 6, hs - 1))
        pygame.draw.rect(surface, (60, 130, 40), (x + 2, y + 3, s - 4, hs - 2))
        pygame.draw.circle(surface, (80, 160, 50), (x + hs - 2, y + 5), 3)
        pygame.draw.circle(surface, (80, 160, 50), (x + hs + 2, y + 5), 3)
        surface.set_at((x + hs, y + 4), (100, 180, 60))
    elif resource_type == "water":
        pygame.draw.polygon(surface, (60, 140, 220), [
            (x + hs, y + 2),
            (x + 3, y + hs + 2),
            (x + s - 3, y + hs + 2)
        ])
        pygame.draw.polygon(surface, (80, 170, 250), [
            (x + hs, y + 4),
            (x + 5, y + hs + 1),
            (x + s - 5, y + hs + 1)
        ])
        pygame.draw.polygon(surface, (60, 140, 220), [
            (x + hs, y + hs + 2),
            (x + 3, y + s - 2),
            (x + s - 3, y + s - 2)
        ])
        surface.set_at((x + hs, y + hs), (120, 200, 255))
    elif resource_type == "iron_ore":
        pygame.draw.polygon(surface, (100, 70, 40), [
            (x + hs, y + 2), (x + s - 3, y + hs - 1),
            (x + s - 4, y + s - 3), (x + 3, y + s - 2)
        ])
        pygame.draw.polygon(surface, (130, 95, 55), [
            (x + hs, y + 4), (x + s - 5, y + hs),
            (x + s - 6, y + s - 4), (x + 5, y + s - 3)
        ])
        surface.set_at((x + hs + 1, y + hs), (150, 110, 70))
        surface.set_at((x + hs - 2, y + hs + 2), (80, 55, 30))
    elif resource_type == "copper_ore":
        pygame.draw.polygon(surface, (160, 90, 40), [
            (x + hs, y + 2), (x + s - 3, y + hs - 1),
            (x + s - 4, y + s - 3), (x + 3, y + s - 2)
        ])
        pygame.draw.polygon(surface, (200, 120, 60), [
            (x + hs, y + 4), (x + s - 5, y + hs),
            (x + s - 6, y + s - 4), (x + 5, y + s - 3)
        ])
        surface.set_at((x + hs, y + hs - 1), (220, 150, 80))
        surface.set_at((x + hs + 2, y + hs + 1), (180, 100, 50))
    elif resource_type == "silicon":
        pygame.draw.polygon(surface, (120, 60, 180), [
            (x + hs, y + 1), (x + s - 2, y + hs),
            (x + hs, y + s - 1), (x + 2, y + hs)
        ])
        pygame.draw.polygon(surface, (150, 90, 210), [
            (x + hs, y + 3), (x + s - 4, y + hs),
            (x + hs, y + s - 3), (x + 4, y + hs)
        ])
        surface.set_at((x + hs, y + hs), (180, 120, 240))
        surface.set_at((x + hs - 1, y + hs - 1), (200, 150, 255))
        surface.set_at((x + hs + 1, y + hs + 1), (130, 70, 190))
    elif resource_type == "ice":
        pygame.draw.polygon(surface, (140, 200, 240), [
            (x + hs, y + 1), (x + s - 2, y + hs),
            (x + hs, y + s - 1), (x + 2, y + hs)
        ])
        pygame.draw.polygon(surface, (180, 230, 255), [
            (x + hs, y + 3), (x + s - 4, y + hs),
            (x + hs, y + s - 3), (x + 4, y + hs)
        ])
        surface.set_at((x + hs, y + hs), (220, 245, 255))
        surface.set_at((x + hs - 1, y + hs - 1), (200, 240, 255))
        surface.set_at((x + hs + 1, y + hs + 1), (120, 180, 220))
