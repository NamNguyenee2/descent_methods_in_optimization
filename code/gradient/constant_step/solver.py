from common import run


def solve(a, x0):
    return run(a, x0, 'constant', step=lambda obj, x, d, f: 0.005/a)
