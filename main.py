from dataclasses import dataclass
import math
import sympy as sp

# define the formulas before we start

m1, m2, v1i, v2i, v1f, v2f = sp.symbols('m_1, m_2, v_1i, v_2i, v_1f, v_2f')
half = sp.numer(1)/2

# We need to find a solution, 
# such that the momentum and kinetic energy remain the same
momentum_eq = sp.Eq(
    m1 * v1i + m2 * v2i, 
    m1 * v1f + m2 * v2f
)
energy_eq = sp.Eq(
    half * m1 * v1i**2 + half * m2 * v2i**2, 
    half * m1 * v1f**2 + half * m2 * v2f**2
)
solutions = sp.solve([momentum_eq, energy_eq], [v1f, v2f])

# Solutions where velocity doesn't chagne do not work for us,
# they are for the cases when there were no collision
solutions = [s for s in solutions if s != (v1i, v2i)][0]
v1f_solved, v2f_solved = [sp.simplify(s) for s in solutions]

# these functions give us the velocities after the collision 
v1f_f = sp.lambdify([m1, m2, v1i, v2i], v1f_solved)
v2f_f = sp.lambdify([m1, m2, v1i, v2i], v2f_solved)


class TerminateException(Exception):
    pass

@dataclass
class MovingObject:
    v: float
    d: float
    m: float

def play_to_next_collision(o1, o2):
    # that is end, second object runs away
    if o1.v >= 0 and o1.v < o2.v: 
        raise TerminateException()

    # the first object bounce back from the wall
    elif o1.v < 0:
        t = - o1.d / o1.v
        o1, o2 = play_to(o1, o2, t)
        return (
            MovingObject(-o1.v, o1.d, o1.m),
            MovingObject(o2.v, o2.d, o2.m)
        )

    # objects collide with each other
    else:
        t = (o2.d - o1.d)/(o1.v - o2.v)
        o1, o2 = play_to(o1, o2, t)
        return apply_collision(o1, o2)

def play_to(o1, o2, t):
    return (
        MovingObject(o1.v, o1.d + o1.v * t, o1.m),
        MovingObject(o2.v, o2.d + o2.v * t, o2.m)
    )

def apply_collision(o1, o2):
    v1 = v1f_f(o1.m, o2.m, o1.v, o2.v)
    v2 = v2f_f(o1.m, o2.m, o1.v, o2.v)

    return (
        MovingObject(v1, o1.d, o1.m),
        MovingObject(v2, o2.d, o2.m)
    )

if __name__ == "__main__":
    n = 5
    o1 = MovingObject(0, 5, 1)
    o2 = MovingObject(-1, 10, 100**n)

    try:
        for i in range(1, int(3.2*10**n)):
            o1, o2  = play_to_next_collision(o1, o2)
    except TerminateException:
        print(f'No more collisions at {i - 1}')


