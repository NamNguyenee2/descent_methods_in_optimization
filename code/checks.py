"""Numerical checks of derivatives, searches, and saved experiment invariants."""
import json
from pathlib import Path
import numpy as np
from common import Objective
from line_search import bracket, golden, quadratic

for a in [1, 100]:
    obj = Objective(a)
    for x in [np.array([1.5,2.]), np.array([4.,5.]), np.array([0.,1.]), np.array([1.,1.])]:
        eps = 1e-5
        basis = np.eye(2)*eps
        gfd = np.array([(obj.f(x+e)-obj.f(x-e))/(2*eps) for e in basis])
        hfd = np.column_stack([(obj.g(x+e)-obj.g(x-e))/(2*eps) for e in basis])
        np.testing.assert_allclose(obj.g(x), gfd, rtol=1e-7, atol=1e-7)
        np.testing.assert_allclose(obj.h(x), hfd, rtol=1e-7, atol=1e-7)
for optimum in [.00003, .7, 5.]:
    phi = lambda t: (t-optimum)**2 + (t-optimum)**4
    abc = bracket(phi, 1.)
    for search in [golden, quadratic]:
        assert abs(search(phi, *abc)-optimum) < 1e-7
samples = []
def parabola(t):
    samples.append(t)
    return (t-.7)**2
assert abs(quadratic(parabola, 0., 1., 2.)-.7) < 1e-8
assert abs(samples[3]-.7) < 1e-12, 'Quadratic search must actually try its interpolated minimizer.'
root = Path(__file__).resolve().parent/'results'
summary = json.loads((root/'summary.json').read_text())
assert len(summary) == 24
for row in summary:
    data = np.load(root/(row['key']+'.npz'))
    xs, steps, norms = data['trajectory'], data['steps'], data['gradient_norms']
    assert len(xs) == len(steps)+1 == row['iterations']+1
    np.testing.assert_allclose(xs[0], row['x0'])
    np.testing.assert_allclose(xs[-1], row['x'])
    assert np.all(np.isfinite(xs)) and np.all(steps > 0)
    assert row['iterations'] <= 20000
    assert (row['status'] == 'converged') == (norms[-1] <= 1e-3)
    if row['status'] == 'iteration_limit':
        assert row['iterations'] == 20000
    obj = Objective(row['a'])
    if row['method'] in ['quadratic','golden','fletcher_reeves']:
        assert np.all(np.diff(data['values']) < 0)
    if row['method'] == 'constant':
        np.testing.assert_allclose(steps, .005/row['a'])
    if row['method'] == 'variable':
        candidates = np.array([.005,.05,.15])/row['a']
        for k in np.linspace(0,len(steps)-1,20,dtype=int):
            losses = [obj.f(xs[k]-alpha*obj.g(xs[k])) for alpha in candidates]
            assert steps[k] == candidates[np.argmin(losses)]
    if row['method'] == 'fletcher_reeves':
        previous = None
        for k, alpha in enumerate(steps):
            g = obj.g(xs[k])
            d = -g
            if k > 0 and k % 2 != 0:
                oldg = obj.g(xs[k-1])
                d = -g + (g@g)/(oldg@oldg)*previous
                if g@d >= 0:
                    d = -g
            np.testing.assert_allclose(xs[k+1]-xs[k],alpha*d,atol=1e-12)
            previous = d
    if row['method'] == 'newton':
        np.testing.assert_allclose(steps, 1.)
        for k in range(len(steps)):
            np.testing.assert_allclose(xs[k+1]-xs[k], np.linalg.solve(obj.h(xs[k]),-obj.g(xs[k])), atol=1e-12)
print('PASS: finite-difference derivatives, independent scalar-search minima, and 24 experiment histories.')
