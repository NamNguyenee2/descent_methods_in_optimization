from common import run


def solve(a, x0):
    candidates = [0.005/a, 0.05/a, 0.15/a]
    def choose(obj, x, d, f):
        # L10 section 4b: compare all three candidates at every iteration.
        return min(candidates, key=lambda alpha: obj.f(x+alpha*d))
    return run(a, x0, 'variable', step=choose)
