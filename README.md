# Space Shooter
### A Python × Pygame arcade game — Mid-Term Group Project

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Requirements & Installation](#requirements--installation)
5. [How to Run](#how-to-run)
6. [Controls](#controls)
7. [Gameplay Mechanics](#gameplay-mechanics)
   - [Waves](#waves)
   - [Enemies](#enemies)
   - [Boss Fights](#boss-fights)
   - [Pickups](#pickups)
   - [Scoring](#scoring)
8. [HUD & Screens](#hud--screens)
9. [Persistent Save System](#persistent-save-system)
10. [Configuration & Tuning](#configuration--tuning)
11. [Team & Contributions](#team--contributions)

---

## Overview

**Space Shooter** is a top-down 2D arcade shooter built with Python and Pygame. The player controls a spaceship defending against waves of increasingly difficult enemies, culminating in multi-phase boss encounters every fifth wave. The game features a persistent high-score system, dynamic difficulty scaling, and pickup items that keep runs varied.

---

## Features

- **Endless wave progression** — enemy count, speed, and health all scale with each wave
- **Multi-phase boss fights** — every 5th wave spawns a Boss with two distinct combat phases and spread-shot attacks
- **Two pickup types** — Health (green) and Ammo (cyan) drops restore player resources mid-run
- **Dynamic HUD** — colour-coded health and ammo bars, live score, wave counter, and all-time best score display
- **Persistent save system** — high score, best wave, total games played, and total enemies killed are saved to `data.json` between sessions
- **New Record detection** — the game-over screen flashes a "★ NEW RECORD! ★" banner when the player beats their personal best
- **Scrolling star field** — parallax-style background for visual depth
- **Three game screens** — Start, Playing, and Game Over, each with contextual information

---

## Project Structure

```
space-shooter/
│
├── main.py            # Game loop, state machine, input handling, collision logic
├── player.py          # Player class — movement, shooting, health/ammo management
├── enemy.py           # Enemy class — movement, drift, health bar, damage handling
├── boss.py            # Boss + BossBullet classes — two-phase AI, spread fire, entry animation
├── bullet.py          # Player bullet class
├── pickup.py          # Pickup class — health and ammo drops
├── wave_manger.py     # WaveManager — spawning, wave progression, collision checks
├── Hud.py             # HUD class — all on-screen UI rendering
├── save_manager.py    # SaveManager — JSON read/write for persistent stats
│
├── settings.py        # All game constants (speed, health, colours, screen size)
├── data.json          # Auto-generated save file — do not delete manually
│
└── assets/
    └── player.png     # Player sprite (50×60 px, PNG with transparency)
```

### File responsibilities at a glance

| File | Owner | Key responsibility |
|---|---|---|
| `pickup.py` | Sheikh Syeed | Pickup spawning, kind selection, collision apply, drawing |
| `Hud.py` | Sheikh Syeed | All UI rendering — bars, score, wave, start/game-over screens |
| `main.py` | Team | Central game loop and state machine |
| `wave_manger.py` | Team | Enemy/boss spawning, bullet-hit checks, score tracking |
| `boss.py` | Team | Boss AI, phase transitions, bullet patterns |
| `save_manager.py` | Team | Persistent data via `data.json` |

---

## Requirements & Installation

**Python version:** 3.10 or higher (required for `list[BossBullet]` and `Boss | None` type hints)

**Dependencies:**
```
pygame
```

Install with pip:
```bash
pip install pygame
```

Or, if a `requirements.txt` is present:
```bash
pip install -r requirements.txt
```

---

## How to Run

From the project root directory:
```bash
python main.py
```

Make sure the `assets/` folder containing `player.png` is in the same directory as `main.py`, or the game will raise a `FileNotFoundError` on startup.

---

## Controls

| Key | Action |
|---|---|
| `←` / `→` / `↑` / `↓` | Move the player ship |
| `Space` | Fire a bullet (costs 1 ammo, 250 ms cooldown) |
| `Enter` | Start the game from the title screen |
| `R` | Restart after Game Over |
| `Escape` | Quit the game |

---

## Gameplay Mechanics

### Waves

The game runs in continuous waves managed by `WaveManager`. When all enemies on screen are destroyed, `is_wave_clear()` returns `True` and `next_wave()` is called automatically.

- **Normal waves** (all waves not divisible by 5): enemies spawn staggered from a queue with a 40-frame delay between each
- **Boss waves** (wave 5, 10, 15, ...): a single Boss spawns instead of a regular enemy formation
- Enemy count caps at 20 per wave; speed caps at 6.0 px/frame

**Scaling formula (normal waves):**
```
count  = min(8 + 2 × (wave − 1), 20)
speed  = min(2.0 + 0.3 × (wave − 1), 6.0)
health = 40 + 10 × (wave − 1)
```

### Enemies

Each `Enemy` instance has:
- A random horizontal drift (`−0.4` to `+0.4` px/frame) that reverses on wall contact, making movement unpredictable
- A per-entity health bar rendered above the sprite
- A 30% chance to drop a Pickup on death
- Colour that cycles through a palette (red → orange → yellow → cyan → purple) per wave

If an enemy reaches the bottom of the screen without being shot, it despawns silently (no damage to the player). Contact with the player deals **20 damage** and destroys the enemy.

### Boss Fights

The `Boss` class has two distinct phases:

| | Phase 1 | Phase 2 |
|---|---|---|
| **Trigger** | Spawns at start of boss wave | Health drops to ≤ 50% of max |
| **Colour** | Purple / Cyan | Orange / Yellow |
| **Movement speed** | 2.0 px/frame | 4.0 px/frame (+ 0.5 per extra boss cycle) |
| **Shoot interval** | Every 90 frames | Every 45 frames |
| **Bullet pattern** | 1 bullet (centre) | 3 spread bullets (−20, 0, +20 px offset) |
| **Max health** | 300 + 100 × extra cycles | — |
| **Flash on hit** | Yes (6 frames white flash) | Yes |

The Boss enters from off-screen top, sliding down to y = 80 before beginning its patrol. Boss bullets (`BossBullet`) deal **15 damage** per hit. Destroying the boss awards **1 000 points** and advances to the next wave.

### Pickups

Pickups are dropped by enemies on death with a **30% chance**. Each pickup is randomly assigned one of two types at creation:

| Type | Colour | Label | Value |
|---|---|---|---|
| Health | Green | `H` | +15 HP (capped at MAX_HEALTH = 100) |
| Ammo | Cyan | `A` | +15 ammo (capped at MAX_AMMO = 200) |

Pickups fall at 1.2 px/frame and despawn if they reach the bottom of the screen. Collection is handled via `pygame.Rect.colliderect()` between the pickup and the player's rect.

### Scoring

| Event | Points |
|---|---|
| Enemy killed | +100 |
| Boss killed | +1 000 |

Score is tracked in `main.py` and accumulated from `wave_manager.score_earned` each frame. The current session score is displayed live on the HUD; the all-time best is loaded from `data.json` at startup.

---

## HUD & Screens

All UI rendering is handled by the `HUD` class in `Hud.py`.

### In-game HUD (top-left and top-right)

- **Health bar** — 150 px wide, colour shifts from green (>50%) → yellow (25–50%) → red (<25%)
- **Ammo bar** — cyan when >25% full, orange when low
- **Score** — top-right, yellow
- **All-time best** — displayed below score in orange
- **Wave number** — below the best-score line, cyan

### Start screen

Displays the game title, controls reference, and — after the first session — the player's personal best score and wave.

### Game Over screen

Shows:
- Final score and wave reached
- All-time best score and best wave
- "★ NEW RECORD! ★" banner (yellow) if a new personal best was set this run
- Prompt to press `R` to restart or `Esc` to quit

---

## Persistent Save System

Handled entirely by `SaveManager` in `save_manager.py`. Data is stored in `data.json` in the project root.

**Tracked fields:**

| Field | Description |
|---|---|
| `high_score` | Highest score ever achieved |
| `best_wave` | Furthest wave ever reached |
| `total_games` | Total number of completed runs |
| `total_enemies` | Cumulative enemies killed across all sessions |

**How it works:**
- On startup, `SaveManager.load()` reads `data.json`. If the file is missing or corrupt, it recreates it with default zeros.
- When a game ends (player death), `update_after_game(score, wave, enemies_killed)` compares the session result against stored records, updates if improved, and writes back to disk.
- Returns `True` if a new record was set — `main.py` uses this to trigger the "NEW RECORD!" banner.

**Example `data.json`:**
```json
{
    "high_score": 8200,
    "best_wave": 11,
    "total_games": 1,
    "total_enemies": 82
}
```

> **Note:** Do not delete `data.json` manually unless you want to reset all statistics. The game will recreate it automatically with zeroed values if it is missing.

---

## Configuration & Tuning

All tunable constants live in `settings.py`. Change values here to adjust difficulty or feel without touching game logic.

```python
# Screen
WIDTH  = 800
HEIGHT = 600
FPS    = 60

# Player
PLAYER_SPEED   = 5
MAX_HEALTH     = 100
MAX_AMMO       = 200
SHOOT_COOLDOWN = 250   # milliseconds between shots

# Bullets
BULLET_SPEED  = 35
BULLET_DAMAGE = 55

# Enemies
ENEMY_SPEED_BASE = 2
ENEMY_HEALTH     = 40
WAVE_SIZE        = 8   # base enemies per wave

# Boss
BOSS_HEALTH = 300

# Pickups
HEALTH_PICKUP_VALUE = 15
AMMO_PICKUP_VALUE   = 15
PICKUP_DROP_CHANCE  = 0.3   # 0.0 – 1.0
```

---

## Team & Contributions

This is a group project developed for the **Programming in Python** course.

| Member | Primary responsibilities |
|---|---|
| Sheikh Syeed | `pickup.py` — pickup spawning, type logic, collision & apply; `Hud.py` — all HUD and screen rendering, high score display, new-record detection |
| Member 2 | *(add name and contribution)* |
| Member 3 | *(add name and contribution)* |

---

*Built with [Python](https://www.python.org/) and [Pygame](https://www.pygame.org/).*
