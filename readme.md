# Simple Beam Solver
This project is an assignment for Optimisation and Analysis of Aircraft Load Bearing Structures classes.
Solves reactions in perfectly horizontal beam.

## Coordinate System & Conventions
The program assumes standard 2D Cartesian coordinates and right-hand rule conventions:
* **X-axis:** Positive is right (+x), Negative is left (-x).
* **Y-axis:** Positive is up (+y), Negative is down (-y).
* **Moments:** Positive is Counter-Clockwise (CCW), Negative is Clockwise (CW). All moments are calculated around 0,0 point.
## Usage
To solve a beam first we need to initialize a `Beam` object and then call `solve()` method.
Initializer takes 2 lists, one for unknown and one for known loads, moments, and supports.
**Unknown list cant have more than 2 unknowns!**
```python
beam = bsolver.Beam(knowns, unknowns)
beam.solve()
```
We can add different kind of support and loads and a moment to the beam.
```python
import bsolver

# Roller/Pinned support at x=0
s1 = bsolver.RollerSupport(0)

# Pinned support at x=6, with a known upward reaction of 10
s2 = bsolver.PinnedSupport(6, bsolver.Vec2(0, 10))

# Simple Load: distance, then a force vector (vector can be omitted if unknown)
l1 = bsolver.SimpleLoad(2, bsolver.Vec2(0, -10))

# Uniform Load (rectangular): width of load, height (magnitude/m), starting distance
l2 = bsolver.UniformLoad(2, 1, 5)

# Triangular Load: width of load, max height, starting distance, direction
# direction=True -> pointy end towards -x (left)
# direction=False -> pointy end towards +x (right)
l3 = bsolver.TriangularLoad(3, 24, 3, True)

# Moment: magnitude (positive is CCW!), distance
m1 = bsolver.Moment(20, 2)
```

## Full Example
```python
import bsolver

# 1. Define Unknowns
u1 = bsolver.RollerSupport(6)
u2 = bsolver.SimpleLoad(7)
unknowns = [u1, u2]

# 2. Define Knowns
s1 = bsolver.PinnedSupport(0, bsolver.Vec2(0, 0))
m1 = bsolver.Moment(20, 2)
l1 = bsolver.SimpleLoad(2, bsolver.Vec2(0, -10))
l2 = bsolver.TriangularLoad(3, 24, 3, True)
knowns = [s1, m1, l1, l2]

# 3. Solve
beam = bsolver.Beam(knowns, unknowns)
beam.solve()
```

