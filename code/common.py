"""Objectives, analytic derivatives, counters, and the shared iteration loop."""
from dataclasses import dataclass, field
import numpy as np

TOL = 1e-3
MAX_ITER = 20_000

@dataclass
class Objective:
    a: float
    counts: dict = field(default_factory=lambda: dict(f=0, g=0, h=0))

    def f(self, x):
        self.counts['f'] += 1
        u, v = x
        with np.errstate(over='ignore', invalid='ignore'):
            return float(self.a * (u*u-v)**2 + (u-1)**2)

    def g(self, x):
        self.counts['g'] += 1
        u, v = x
        with np.errstate(over='ignore', invalid='ignore'):
            return np.array([4*self.a*u*(u*u-v)+2*(u-1), -2*self.a*(u*u-v)])

    def h(self, x):
        self.counts['h'] += 1
        u, v = x
        return np.array([[12*self.a*u*u-4*self.a*v+2, -4*self.a*u],
                         [-4*self.a*u, 2*self.a]])


def run(a, x0, name, step=None, max_iter=MAX_ITER, tol=TOL):
    obj = Objective(a)
    x = np.array(x0, dtype=float)
    f, g = obj.f(x), obj.g(x)
    xs, fs, norms, alphas = [x.copy()], [f], [float(np.linalg.norm(g))], []
    dprev = gprev = None
    restarts = 0
    status = 'iteration_limit'
    for k in range(max_iter + 1):
        if not np.isfinite(f) or not np.all(np.isfinite(g)):
            status = 'numerical_failure'; break
        if norms[-1] <= tol:
            status = 'converged'; break
        if k == max_iter:
            break
        try:
            if name == 'newton':
                d = np.linalg.solve(obj.h(x), -g)
                alpha = 1.0
            else:
                d = -g
                if name == 'fletcher_reeves' and k > 0:
                    # Restart every n=2 steps or if the new direction is not descent.
                    if k % len(x) == 0:
                        restarts += 1
                    else:
                        beta = float(g @ g / (gprev @ gprev))
                        d = -g + beta*dprev
                        if float(g @ d) >= 0:
                            d = -g
                            restarts += 1
                alpha = step(obj, x, d, f)
            if not np.isfinite(alpha) or alpha <= 0 or not np.all(np.isfinite(d)):
                raise ValueError('invalid step or direction')
            trial = x + alpha*d
            if not np.all(np.isfinite(trial)):
                raise ValueError('nonfinite iterate')
            gprev, dprev = g.copy(), d.copy()
            x = trial
            f, g = obj.f(x), obj.g(x)
            xs.append(x.copy()); fs.append(f); norms.append(float(np.linalg.norm(g)))
            alphas.append(float(alpha))
        except (ValueError, np.linalg.LinAlgError, FloatingPointError) as exc:
            status = 'failure: ' + str(exc); break
    return dict(method=name, a=a, x0=list(x0), x=x.tolist(), iterations=len(alphas),
                f=fs[-1], gradient_norm=norms[-1], status=status,
                evaluations=obj.counts, restarts=restarts,
                trajectory=np.array(xs), values=np.array(fs),
                gradient_norms=np.array(norms), steps=np.array(alphas))
