import bsolver

u1 = bsolver.RollerSupport(6)
u2 = bsolver.SimpleLoad(7)

unknowns = [u1, u2]

s1 = bsolver.PinnedSupport(0, bsolver.Vec2(0, 0))
m1 = bsolver.Moment(20, 2)
l1 = bsolver.SimpleLoad(2, bsolver.Vec2(0, -10))
l2 = bsolver.TriangularLoad(3, 24, 3, True)

knowns = [s1, m1, l1, l2]

beam = bsolver.Beam(knowns, unknowns)
beam.solve()
