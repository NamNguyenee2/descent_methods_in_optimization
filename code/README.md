# Project experiments

Run from the project root with Python 3, NumPy, and Matplotlib:

```sh
python code/code.py
python code/checks.py
python code/plot_results.py
python code/make_summary_table.py
```

The existing interpreter `/tmp/hw6-check-env/bin/python` was used for the delivered run (NumPy 2.3.5, Matplotlib 3.10.6). The plotting script requires Times New Roman and stops if it is unavailable. It embeds the font in vector PDF figures. Set `MPLCONFIGDIR` and `XDG_CACHE_HOME` to writable cache locations if needed.

## Layout

- `gradient/constant_step`, `gradient/variable_step`, `gradient/quadratic_fit`, `gradient/golden_section`: the four gradient configurations.
- `newton`: classical Newton-Raphson.
- `conjugate_gradient`: nonlinear Fletcher-Reeves with golden-section search.
- `common.py`: analytic objective, gradient, Hessian, evaluation counts, and iteration loop.
- `line_search.py`: self-written search routines. No optimizer from a library is used.
- `results/summary.json`: scalar metrics, status, evaluation counts, and restart counts for every run.
- `results/*.npz`: every iterate, objective, gradient norm, and accepted step.
- `results/convergence.pdf`: convergence diagnostic, also included as `figures/convergence.pdf` in the paper.
- `../paper/6ad7d74c9659ce1c2cff5692/figures`: six four-panel trajectory PDFs, one convergence PDF, and PNG previews.

## Numerical choices

All six configurations are run for a=1 and a=100, each from (1.5,2) and (4,5). The gradient tolerance is 0.001 and the outer iteration cap is 20,000. Initialization is iteration zero. Nonfinite quantities, search failure, or singular Newton systems are reported as failures, not convergence.

The constant step is 0.005/a. The L10 variable-step rule evaluates the three fixed candidates {0.005, 0.05, 0.15}/a at each iterate and selects the smallest resulting objective. Scaling by a accounts for the different penalty weights. The same settings apply to both initial points. These are documented experimental choices, not globally guaranteed stable step bounds.

Both line searches begin with a trial step 1/a. Halve it until the objective decreases, then expand the distance between trial steps by a factor of two until a right endpoint with no lower value is found. The shrink and expansion phases are each limited to 100 attempts. Function values are cached within each line search. Bracketing does not certify global unimodality of a quartic restriction, and the routines do not claim a global line minimum.

The inner stopping width is 1e-12 + 1e-8 times the magnitude of the current best step. Both searches allow at most 160 interval reductions. Quadratic fit uses three function samples and its interpolated minimizer. A trial outside the interior 90% of the bracket, within 5% of bracket width of the middle point, or with invalid/nonpositive curvature is replaced by a golden-fraction step into the larger side. Golden-section search uses (sqrt(5)-1)/2 and reuses cached evaluations. An inner iteration limit is reported as failure rather than silently accepting an unconverged search.

Newton uses a unit step and `numpy.linalg.solve(H, -g)`, with no damping, Hessian shifts, or fallback to gradient descent. Fletcher-Reeves uses beta = (g_new dot g_new)/(g_old dot g_old), restarting with the negative gradient every n=2 iterations or when the proposed direction is not descent. Golden-section search is applied along that direction. The restart choice is an explicit implementation safeguard permitted by the draft methodology.

Objective counts include outer monitoring and unique inner-search calls. Gradient and Hessian counts include all actual evaluations. Outer monitoring is recomputed after a line search, so its repeated endpoint evaluation is counted too. Runtime is not reported as a benchmark.

## Verification and plotting

`checks.py` compares analytic derivatives against central finite differences at four representative points for both objectives, checks both scalar searches on independently known minima, confirms that quadratic interpolation actually proposes the parabola minimizer, and checks all 24 histories. It verifies the fixed and candidate steps, Newton updates, Fletcher-Reeves recurrence with restarts, descent of line-search configurations, and stopping status.

Each paper figure has four panels: rows identify f1 and f2, columns display the actual initial points as x^0=(1.5,2) and x^0=(4,5). Gray lines are objective level curves, colored lines connect every stored iterate, sparse dots indicate iterates, circles mark the start, squares the final iterate, and stars the known minimizer. Axes limits are shared across methods for each problem/start so excursions are not hidden. Plot text is Times New Roman at 8.5 points, tick labels at 7.5 points, status annotations at 7 points, and contour labels at 5.5 points at the native 3.45-inch figure width. Contour levels use a geometric sequence and labels are rounded to two significant digits.

22 of 24 runs meet the tolerance. Constant-step runs for a=100 both reach the iteration cap and are clearly labeled `limit`. All raw data are retained. The paper contains figures, a 24-run comparison table, and the authorized parameter summary, without comparative results-analysis prose.

`make_summary_table.py` generates `summary_table.tex` from the saved JSON metrics. No experiment rerun is needed for formatting changes.
