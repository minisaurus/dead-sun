# Dead Sun - Game Specification

## Project Overview

**Project Name:** Dead Sun  
**Type:** Space Colony / Ship Management Simulation  
**Core Concept:** Terminal-based spaceship building, crew management, and exploration game where the sun is dying and you must survive in space.  
**Target Users:** Fans of The Last Starship, Factorio-style automation, and deep management games.

## Version 2.0 - Vision

A more complete space survival game inspired by The Last Starship and Riftborne, featuring fleet management, automation, trading, and combat - all rendered in terminal-friendly ASCII/emoji graphics.

---

## Core Game Systems

### 1. Ship Building & Management

**Current State:** Grid-based single ship with modular tiles  
**Expanded State:**

- Multiple ships (fleet management)
- Each ship has its own grid (flexible size per ship)
- Ship modules with dependencies (power, oxygen, hull integrity)
- Ship-to-ship docking for crew movement and resource transfer

**Module Types (Expanded):**

| Category | Modules |
|----------|---------|
| Command | Cockpit, Bridge, Comms Array |
| Power | Reactor (multiple tiers), Solar Panels, Battery |
| Propulsion | Engine, Thruster, FTL Drive, Jump Drive |
| Life Support | Life Support, Oxygen Generator, Hydroponics, Farm |
| Cargo | Cargo Bay (multiple sizes), Storage Locker |
| Production | Mining Drill, Refinery, Fabricator, Assembler |
| Defense | Shield Generator, Armor Plates, Point Defense |
| Weapons | Laser Turret, Railgun, Missile Bay, Torpedoes |
| Crew | Crew Quarters, Med Bay, Workshop, Lab |

**Module Properties:**
- Power draw/generation
- Oxygen draw/generation
- Crew requirement
- Hull integrity (damage states)
- Production rate (for automated modules)

### 2. Crew System

**Current State:** Basic assignment to modules  
**Expanded State:**

- Crew roles: Commander, Engineer, Pilot, Miner, Scientist, Medic, Gunner
- Skill system affecting module efficiency
- Needs: Food, Oxygen, Sleep, Morale, Health
- Crew tasks: Manual commands OR automation queues

**Automation System (NEW):**
- Task queues per crew member
- "Do X when Y" conditions
- Production automation: machine runs until inventory full
- Logistics: automatic resource routing between ships

### 3. Economy & Trading

**NEW System:**

- Resource types: Metals, Electronics, Fuel, Food, Water, Ice, Rare Minerals
- Station types: Trading Post, Shipyard, Mining Outpost, Refinery, Black Market
- Buy/Sell prices vary by station and faction
- Player can establish trade routes (manual or automated)
- Contract system: transport missions, mining contracts, escort missions

### 4. Exploration & Progression

**Current State:** Small solar system with ~10 locations  
**Expanded State:**

- Procedural sector generation (multiple systems)
- Each system has 5-15 locations
- Exploration reveals new systems via Jump Drives
- Discovery bonuses and anomalies
- Faction reputation system

### 5. Combat System (NEW)

**Combat Mode:**

- Turn-based tactical view
- Targeting specific ship systems (hull, power, life support, weapons)
- Crew damage and evacuation
- Loot and salvage from destroyed ships
- Ship boarding mechanics

**Ship Combat Stats:**
- Hull points
- Shield points (regenerates)
- Evasion rating
- Accuracy rating

### 6. Resource Management

**Resources:**
- Raw: Iron Ore, Copper Ore, Silicon, Ice, Rare Minerals
- Refined: Metal, Electronics, Fuel, Food, Water
- Special: Stargate Resin, Antimatter, Dark Matter

**Production Chain:**
```
Mining Drill → Ore → Refinery → Metal/Electronics
Ice → Refinery → Water/Fuel
Fabricator → Complex items (weapons, modules)
```

### 7. Day/Night Cycle & Survival

**Survival Mechanics:**
- Daily resource consumption (food, oxygen)
- Ship degradation (need repairs)
- Random events: equipment failures, meteor showers, pirate attacks
- Health/Morale affecting crew efficiency

---

## Technical Architecture

### File Structure (v2)

```
dead-sun/
├── dead_sun.py          # Entry point
├── main.py              # Main game loop (new)
├── data/
│   ├── __init__.py
│   ├── items.py         # Item/resource definitions
│   ├── modules.py       # Module definitions
│   ├── locations.py     # Location types
│   └── config.py        # Game constants
├── world/
│   ├── __init__.py
│   ├── galaxy.py        # Multiple solar systems
│   ├── system.py        # Solar system
│   └── location.py      # Individual locations
├── ship/
│   ├── __init__.py
│   ├── ship.py          # Ship class
│   ├── grid.py          # Ship grid
│   └── module.py        # Module placement/logic
├── crew/
│   ├── __init__.py
│   ├── crew.py          # Crew member
│   ├── roster.py        # Crew management
│   ├── ai.py            # Crew automation (new)
│   └── roles.py         # Role definitions
├── economy/
│   ├── __init__.py
│   ├── market.py        # Trading system
│   ├── contracts.py     # Mission contracts
│   └── logistics.py     # Automated shipping (new)
├── combat/
│   ├── __init__.py
│   ├── battle.py        # Combat engine
│   ├── weapons.py       # Weapon systems
│   └── damage.py        # Damage calculation
├── events/
│   ├── __init__.py
│   ├── event.py         # Random events
│   └── anomalies.py     # Space anomalies
├── ui/
│   ├── __init__.py
│   ├── screen.py        # Base screen
│   ├── render.py        # Terminal rendering
│   ├── ship_screen.py   # Ship building UI
│   ├── map_screen.py    # Galaxy map UI
│   ├── crew_screen.py   # Crew management UI
│   ├── combat_screen.py # Combat UI (new)
│   └── trade_screen.py  # Trading UI (new)
└── saves/
    └── save_manager.py  # Save/load system (new)
```

### Rendering (Terminal)

- Color-coded module display
- ASCII art for ships and planets
- Emoji for resources and UI elements
- Mini-map for galaxy view
- Status bars for ship systems

---

## Development Phases

### Phase 1: Foundation (MVP)
- [ ] Refactor code to new modular structure
- [ ] Implement ship grid system (multiple ships)
- [ ] Expand module system with dependencies
- [ ] Basic crew with roles and skills
- [ ] Expand galaxy (multiple systems)
- [ ] Trading system (basic buy/sell)

**Milestone:** Playable prototype with 2+ ships, 20+ modules, trading

### Phase 2: Automation
- [ ] Crew task automation system
- [ ] Production automation (machines run on conditions)
- [ ] Logistics automation (auto-resource routing)
- [ ] Fleet management UI

**Milestone:** Semi-automated gameplay loop

### Phase 3: Combat & Depth
- [ ] Combat system with tactical view
- [ ] Random events and anomalies
- [ ] Faction reputation
- [ ] Mission contracts
- [ ] Save/load system

**Milestone:** Complete single-player loop

### Phase 4: Polish
- [ ] Visual improvements (ASCII art)
- [ ] Tutorial system
- [ ] Difficulty settings
- [ ] Performance optimization

**Milestone:** Release-ready version

---

## UI/UX Specification

### Screen Layout (Terminal)

**Main Screens:**
1. **Ship View** - Grid showing ship modules with status
2. **Galaxy Map** - ASCII star map with system markers
3. **Crew Panel** - Crew list with status and assignments
4. **Cargo/Resources** - Resource inventory with totals
5. **Systems Panel** - Power/Oxygen/Crew capacity stats
6. **Trade Screen** - Station interface for buying/selling
7. **Combat Screen** - Tactical view during combat

### Visual Style

**Color Scheme:**
- Title/System: Bright Yellow 🌅
- Good/Active: Green ✓
- Warning: Orange ⚠
- Danger/Critical: Red ✗
- Info: Cyan ℹ
- Muted: Gray ·

**ASCII/Emoji Key:**
- Ship hull: `█` blocks
- Modules: Emoji per type
- Resources: Symbols (◆, ●, ▲, etc.)
- Planets: ASCII art
- Stars: `*`

---

## Acceptance Criteria

### Must Have (MVP)
- [ ] Build and manage multiple ships
- [ ] At least 15 different module types
- [ ] Crew with roles and skills
- [ ] Mine resources from locations
- [ ] Refine raw materials
- [ ] Travel between systems
- [ ] Basic trading at stations
- [ ] Save game state

### Should Have
- [ ] Crew automation (task queues)
- [ ] Production automation
- [ ] Combat system
- [ ] Random events
- [ ] Faction reputation

### Nice to Have
- [ ] Procedural galaxy generation
- [ ] Mission contracts
- [ ] Fleet logistics automation
- [ ] Multiple save slots
- [ ] ASCII ship art

---

## Technology Stack

- **Language:** Python 3.11+
- **Rendering:** Curses (terminal)
- **Storage:** JSON saves
- **Optional:** Web UI layer (future)