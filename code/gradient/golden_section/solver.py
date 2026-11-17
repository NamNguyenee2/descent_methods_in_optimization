from common import run
from line_search import search, golden


def solve(a, x0):
    return run(a, x0, 'golden', step=lambda obj, x, d, f: search(obj, x, d, f, golden))
