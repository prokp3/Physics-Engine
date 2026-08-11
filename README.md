# 2D Particle Physics Engine

A 2D particle physics simulator built from scratch in Python + Pygame, as a learning project to understand numerical simulation, collision detection/response, and spatial optimization. Long-term goal: extend this into a basic wind tunnel simulator.

## What it does

- Simulates particles under gravity using **Euler integration**
- Uses **real SI units** (meters, seconds, m/s, m/s²) internally, with a camera-style **meters → pixels** conversion only at draw time
- Particles **bounce elastically** off all four screen boundaries (walls, floor, ceiling)
- Supports **multiple particles**, stored in a list and updated/drawn each frame
- Uses a **spatial partitioning grid** to avoid expensive all-pairs collision checks as particle count grows
- (In progress) **Particle-particle collision detection and response**

## Core concepts

### Euler integration
Rather than solving equations of motion analytically, the simulation advances state forward in small timesteps (`dt`):

```
velocity += acceleration * dt
position += velocity * dt
```

This is why `dt` is recomputed every frame from `clock.tick(60)` rather than assumed constant — real frame times vary, and using a stale/fixed `dt` would desync the simulation from real elapsed time.

### Units and the camera transform
Particle position, velocity, and acceleration are stored in **meters**, not pixels. A single global `scale` (pixels per meter) converts between world space and screen space — but *only* inside `draw()`. Physics math (`update()`) never touches `scale`, since forces and motion don't care about how they're rendered.

```
pixel_coordinate = world_coordinate_in_meters * scale
```

### Boundary collisions
Each particle checks its position (accounting for radius) against the world's edges, converted from pixel dimensions (`WIDTH`, `HEIGHT`) into meters. On collision, the relevant velocity component is negated (`vy = -vy` for floor/ceiling, `vx = -vx` for walls) and position is clamped so the particle doesn't visually sink past the boundary. Currently perfectly elastic (no energy loss).

### Spatial grid (partitioning)
Checking every particle against every other particle scales as O(n²) — fine for a handful of particles, expensive at scale. Instead:

- The world is divided into square cells, sized to roughly the **largest particle's diameter** (`cell_size = 2 × max_radius`) — small enough to keep particles-per-cell low, large enough that one particle doesn't span many cells.
- Each frame, particles are bucketed into a dictionary: `grid[(col, row)] = [particles in that cell]`.
- To find a particle's potential collision candidates, only its own cell and the 8 surrounding cells are checked (9 total) — not the whole simulation.

### Collision detection (particle-particle)
Two particles are considered colliding when the distance between their centers is less than or equal to the sum of their radii:

```
distance = sqrt((x1-x2)² + (y1-y2)²)
colliding if distance <= r1 + r2
```

### Collision response (in progress)
For equal-mass, perfectly elastic collisions, velocity components along the line connecting the two particles' centers (the "normal" direction) are exchanged between the particles; components perpendicular to that line are unaffected.

## Project structure

Currently a single Jupyter notebook, built up cell by cell. Rough shape:

1. `Particle` class — `__init__`, `update(dt)`, `draw(screen)`, `check_bounds(width, height)`, `location(width, height)`, `is_colliding(other)`
2. Global config — `WIDTH`, `HEIGHT`, `scale`, `cell_size`
3. `count_cells(width, height)` — grid dimensions
4. Grid-building loop — populates `grid` dict each frame
5. `particles_nearby(particle, grid)` — returns candidate particles from the 9 surrounding cells
6. Main game loop — event handling, `dt` calculation, per-particle update/bounds/draw

## Status / next steps

- [x] Single particle with gravity, Euler integration
- [x] SI units + camera transform
- [x] Elastic wall/floor/ceiling collisions
- [x] Multiple particles in a list
- [x] Spatial grid for efficient neighbor lookup
- [x] Particle-particle collision detection (`is_colliding`)
- [ ] Particle-particle collision response (velocity exchange along normal)
- [ ] Wire collision response into the main loop using the grid
- [ ] Optional: restitution coefficient (`e < 1`) for energy-losing bounces
- [ ] Optional: drag / air resistance, terminal velocity
- [ ] Stretch goal: wind tunnel simulator (airflow forces on particles, possibly pressure readings from wall collisions)

## Requirements

```
pip install pygame numpy
```

(`math`, `random` are standard library)
