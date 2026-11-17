from common import run


def solve(a, x0):
    # Classical undamped Newton. No Hessian modification or line search.
    return run(a, x0, 'newton')
