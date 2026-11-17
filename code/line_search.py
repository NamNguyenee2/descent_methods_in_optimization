"""Self-written bracketing, golden-section search, and safeguarded quadratic fit."""
import math

REL_TOL = 1e-8
ABS_TOL = 1e-12
INNER_LIMIT = 160
BRACKET_LIMIT = 100
TAU = (math.sqrt(5)-1)/2


def bracket(phi, initial):
    """Shrink until descent, then double spacing to obtain f(b)<f(a),f(c)."""
    a, fa = 0.0, phi(0.0)
    b = initial
    for _ in range(BRACKET_LIMIT):
        fb = phi(b)
        if math.isfinite(fb) and fb < fa:
            break
        b *= 0.5
    else:
        raise ValueError('no decreasing bracket step')
    for _ in range(BRACKET_LIMIT):
        c = b + 2*(b-a)
        fc = phi(c)
        if not math.isfinite(fc):
            # Retain a finite right endpoint, without taking an infinite sample.
            for _ in range(BRACKET_LIMIT):
                c = (b+c)/2
                fc = phi(c)
                if math.isfinite(fc):
                    break
        if math.isfinite(fc) and fc > fb:
            return a, b, c
        if fc == fb:
            return a, b, c
        a, fa, b, fb = b, fb, c, fc
    raise ValueError('bracket expansion limit')


def tolerance(b):
    return ABS_TOL + REL_TOL*abs(b)


def golden(phi, a, b, c):
    u, v = c-TAU*(c-a), a+TAU*(c-a)
    fu, fv = phi(u), phi(v)
    best = min([(phi(a), a), (phi(b), b), (phi(c), c), (fu, u), (fv, v)])
    for _ in range(INNER_LIMIT):
        if c-a <= tolerance(best[1]):
            return best[1]
        if fu <= fv:
            c, v, fv = v, u, fu
            u = c-TAU*(c-a); fu = phi(u)
            best = min(best, (fu, u))
        else:
            a, u, fu = u, v, fv
            v = a+TAU*(c-a); fv = phi(v)
            best = min(best, (fv, v))
    raise ValueError('golden-section iteration limit')


def quadratic(phi, a, b, c):
    fa, fb, fc = phi(a), phi(b), phi(c)
    for _ in range(INNER_LIMIT):
        width = c-a
        if width <= tolerance(b):
            return b
        denominator = (b-a)*(fb-fc)-(b-c)*(fb-fa)
        # A negative denominator corresponds to positive fitted curvature here.
        if denominator < 0 and math.isfinite(denominator):
            u = b - .5*((b-a)**2*(fb-fc)-(b-c)**2*(fb-fa))/denominator
        else:
            u = math.nan
        # Keep new samples away from existing points to ensure interval progress.
        gap = 0.05*width
        if not math.isfinite(u) or not a+gap < u < c-gap or abs(u-b) < gap:
            u = b + (1-TAU)*(c-b) if c-b > b-a else b-(1-TAU)*(b-a)
        fu = phi(u)
        if u < b:
            if fu < fb:
                c, fc, b, fb = b, fb, u, fu
            else:
                a, fa = u, fu
        else:
            if fu < fb:
                a, fa, b, fb = b, fb, u, fu
            else:
                c, fc = u, fu
    raise ValueError('quadratic-fit iteration limit')


def search(obj, x, d, fx, algorithm):
    cache = {0.0: fx}
    def phi(alpha):
        alpha = float(alpha)
        if alpha not in cache:
            cache[alpha] = obj.f(x + alpha*d)
        return cache[alpha]
    abc = bracket(phi, 1.0/obj.a)
    alpha = algorithm(phi, *abc)
    if alpha <= 0 or not phi(alpha) < fx:
        raise ValueError('line search did not decrease objective')
    return alpha
