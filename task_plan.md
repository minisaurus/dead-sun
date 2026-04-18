# Dead Sun - Phase 1 Task Plan

## Goal
Implement Phase 1 MVP: Foundation with modular structure, multiple ships, expanded modules, crew roles, galaxy expansion, and trading.

## Phase 1 Tasks

### 1. Refactor Code to Modular Structure
- [ ] Create `data/` package with items.py, modules.py, locations.py, config.py
- [ ] Create `world/` package with galaxy.py, system.py, location.py
- [ ] Create `ship/` package with ship.py, grid.py, module.py
- [ ] Create `crew/` package with crew.py, roster.py, roles.py
- [ ] Create `economy/` package with market.py, contracts.py, logistics.py
- [ ] Create `ui/` package with screens
- [ ] Update main entry point

### 2. Ship Grid System (Multiple Ships)
- [ ] Fleet class managing multiple Ship instances
- [ ] Ship docking/undocking mechanics
- [ ] Inter-ship crew movement
- [ ] Fleet command interface

### 3. Expand Module System
- [ ] Add module dependencies (power, oxygen, crew)
- [ ] Add new module types (weapons, defense, production)
- [ ] Module status (active/damaged/offline)
- [ ] Module efficiency based on crew skills

### 4. Crew with Roles and Skills
- [ ] Define crew roles: Commander, Engineer, Pilot, Miner, Scientist, Medic, Gunner
- [ ] Skill system affecting module efficiency
- [ ] Crew needs (food, oxygen, morale, health)
- [ ] Crew task assignment improvements

### 5. Expand Galaxy (Multiple Systems)
- [ ] Generate multiple solar systems
- [ ] FTL travel between systems
- [ ] System-specific resources and dangers
- [ ] Galactic map view

### 6. Trading System
- [ ] Station types: Trading Post, Shipyard, Mining Outpost
- [ ] Buy/sell resources at stations
- [ ] Price variations by station type
- [ ] Trade route planning

## Progress
- [ ] Started: 2026-04-18
- [ ] Completed:
- [ ] Current Task:

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| - | - | - |