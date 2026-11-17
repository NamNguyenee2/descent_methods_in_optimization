"""Run all 24 experiments and save full histories and summary metrics."""
from pathlib import Path
import json
import numpy as np
from gradient.constant_step.solver import solve as constant
from gradient.variable_step.solver import solve as variable
from gradient.quadratic_fit.solver import solve as quadratic
from gradient.golden_section.solver import solve as golden
from newton.solver import solve as newton
from conjugate_gradient.solver import solve as cg

SOLVERS = [constant, variable, quadratic, golden, newton, cg]
STARTS = [(1.5, 2.), (4., 5.)]
RESULTS = Path(__file__).resolve().parent / 'results'


def main():
    RESULTS.mkdir(exist_ok=True)
    summary = []
    for solve in SOLVERS:
        for a in [1, 100]:
            for j, x0 in enumerate(STARTS, 1):
                result = solve(a, x0)
                key = f"{result['method']}_a{a}_start{j}"
                arrays = {k: result.pop(k) for k in ['trajectory', 'values', 'gradient_norms', 'steps']}
                np.savez_compressed(RESULTS / f'{key}.npz', **arrays)
                result['key'] = key
                summary.append(result)
                print(key, result['status'], result['iterations'], f"|g|={result['gradient_norm']:.3g}", flush=True)
    (RESULTS/'summary.json').write_text(json.dumps(summary, indent=2, allow_nan=False)+'\n')

if __name__ == '__main__':
    main()
