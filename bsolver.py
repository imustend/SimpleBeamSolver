import math

def solve_2x2(a, b, e, c, d, f):
    """
    a*x + b*y = e
    c*x + d*y = f
    """
    determinant = (a * d) - (b * c)

    if determinant == 0:
        print("equations unsolvable")
        return None, None

    x = ((e * d) - (b * f)) / determinant
    y = ((a * f) - (e * c)) / determinant

    return x, y

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_polar(cls, r, theta):
        """
        rad points towards +x, and it moves counterclockwise; 90°: +y...
        """
        return cls(r * math.cos(theta), r * math.sin(theta))

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Vec({self.x:.2f}, {self.y:.2f})"


class SimpleLoad:
    def __init__(self, distance, load = Vec2(0, 0)):
        self.load = load
        self.distance = distance

    def __repr__(self):
        return f"Load({self.load}, {self.distance})"


class UniformLoad:
    def __init__(self, a, h, starting_distance):
        magnitude = a * h
        self.load = Vec2(0, -magnitude)
        self.distance = starting_distance + a * 0.5

    def __repr__(self):
        return f"Uniform Load({self.load}, {self.distance})"

class TriangularLoad:
    """
    direction: true -> pointy end towards -x; false -> pointy end towards +x
    """
    def __init__(self, a, h, starting_distance, direction = True):
        magnitude = a * h * 0.5
        self.load = Vec2(0, -magnitude)
        self.distance = starting_distance + a * ((2/3) if direction else (1/3))

    def __repr__(self):
        return f"Uniform Load({self.load}, {self.distance})"

class PinnedSupport:
    def __init__(self, distance, reactions = Vec2(0, 0)):
        self.distance = distance
        self.reactions = reactions

    def __repr__(self):
        return f"PinSupport({self.reactions}, {self.distance})"

class RollerSupport:
    def __init__(self, distance , reactions = Vec2(0, 0)):
        self.distance = distance
        self.reactions = reactions

    def __repr__(self):
        return f"RollerSupport({self.reactions:.2f}, {self.distance})"

class Moment:
    """
    positive moment is CCW, while negative moment is CW
    """
    def __init__(self, moment, distance):
        self.moment = moment
        self.distance = distance

class Beam:
    """

    """
    def __init__(self, known, unknown):
        if len(unknown) > 2:
            print("unsolvable, too many unknowns")
            return
        self.known = known
        self.unknown = unknown

    def solve(self):
        load_sum = Vec2(0,0)
        moment_sum = 0
        if len(self.unknown) > 2:
            print("unsolvable, too many unknowns")
            return
        if len(self.unknown) == 0:
            print("solved")
            return
        for known in self.known:
            if isinstance(known, (RollerSupport, PinnedSupport)):
                load_sum += known.reactions
                moment_sum += known.reactions.y * known.distance
            elif isinstance(known, (SimpleLoad, UniformLoad, TriangularLoad)):
                load_sum += known.load
                moment_sum += known.load.y * known.distance
            elif isinstance(known, Moment):
                moment_sum += known.moment
            else:
                print(f"unknown type: {type(known)}")

        if len(self.unknown) == 1:
            u1 = self.unknown[0]
            val = -load_sum

            self._apply_solved_value(u1, val)

            print(f"solved 1 unknown: {u1}")
        elif len(self.unknown) == 2:
            u1 = self.unknown[0]
            u2 = self.unknown[1]

            a = 1
            b = 1
            e = -load_sum.y

            c = u1.distance
            d = u2.distance
            f = -moment_sum

            val1, val2 = solve_2x2(a, b, e, c, d, f)

            if val1 is not None and val2 is not None:
                self._apply_solved_value(u1, val1)
                self._apply_solved_value(u2, val2)
                print(f"solved 2 unknowns:\n -> {u1}\n -> {u2}")

    def _apply_solved_value(self, unknown_item, val):
        if isinstance(unknown_item, (SimpleLoad, UniformLoad, TriangularLoad)):
            unknown_item.load = val
        elif isinstance(unknown_item, (PinnedSupport, RollerSupport)):
                unknown_item.reactions = val