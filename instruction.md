This is the instruction to complete my project "Project-1.pdf".
The main reference can be used is "main_ref.pdf". We also need to search on Internet for more references but I will do it by myself so we will not make up any reference.

Your main work is help me complete this project by the following steps (I will introduce step-by-step so you dont need to be overwhelm).
Also, when you do something, include on this .md to guarantee that you dont miss any information.

## Rules
- Avoid all AI slop
- Never use emdash "--" or "---"
- Rarely use ";" when writing texts
- Use "." or "," after every equations
- Define all variables, do not miss any
- This is an engineering research conferecen paper

## Step 0: Understand the project
### Project requirements (reviewed and validated)

- `Project-1.pdf` is the EEL6026 assignment, due Thursday, November 19, 2026.
- Compare algorithms on `f1(x1,x2) = (x1^2-x2)^2 + (x1-1)^2` and `f2(x1,x2) = 100(x1^2-x2)^2 + (x1-1)^2`.
- Required methods: steepest descent with a constant step size, a variable step size (the assignment says to use three values of our choice), quadratic-fit line search, and golden-section line search; Newton–Raphson; and a self-written "Fletcher-Powell Conjugate Gradient" algorithm using a preferred step-size method from part (a).
- Run every method on both functions from both initial guesses: `(1.5, 2)` and `(4, 5)`.
- Stop when the gradient norm is at most `0.001`, or when the iteration count reaches `20,000`. The gradient-norm notation was verified visually in the assignment PDF because text extraction omitted symbols.
- Show the iterate trajectories on level curves in all cases. Compare results and emphasize our own observations and conclusions.
- The assignment permits at most six pages; our target remains five pages as instructed below. Include title, abstract, introduction, body/results, conclusion, references, and relevant figures/tables; do not include computer code in the paper.
- Required layout: two columns, single spacing, 10-point font, 1-inch top/bottom margins, 0.7-inch side margins, 3.45-inch column width, and 0.2-inch column separation. The supplied template's actual dimensions still need to be checked against these requirements.

### Reference and existing files

- `main_ref.pdf` is an 88-page excerpt (printed pages 69–156) from *An Introduction to Optimization: With Applications to Machine Learning*, fifth edition, Edwin K. P. Chong, Wu-Sheng Lu, and Stanislaw H. Zak, Wiley, 2024. It covers Chapters 6–10: optimality conditions, one-dimensional searches, gradient methods, Newton's method, and conjugate directions. Reviewed the relevant algorithm sections; this was not a line-by-line review of every exercise and proof.
- Useful reference locations: Section 7.2 (golden section), Sections 7.7–7.8 (bracketing and line search), Exercise 7.9 (three-point quadratic fit using objective values), Chapter 8 (gradient methods), Chapter 9 (Newton), and Sections 10.3–10.4 (linear/nonlinear conjugate gradient).
- `code/code.py` runs all six implemented configurations on four objective/start combinations, for 24 experiments. Full histories and summary metrics are saved under `code/results`.
- `paper/6ad7d74c9659ce1c2cff5692/root.tex` builds the paper. Preliminary, Methodology, and Numerical Results contain the approved text and experimental setup. Results include six trajectory figures, one convergence figure, and a 24-run summary table. Introduction and Related Work still contain only headings, and Conclusion is empty.
- `reference.bib` and `output.bbl` contain existing references largely about neural networks, modeling, and control. These are not automatically validated or selected for this project. `root.tex` currently has no bibliography commands.
- `ieeeconf.cls`, `IEEEtran.bst`, and `IEEEabrv.bib` are template support files; inspected their identity and role rather than auditing every line of their implementation. `.gitignore` excludes LaTeX build outputs. Generated files include the current five-page `root.pdf`, compilation log, auxiliary files, dependency records, and SyncTeX data.

### Resolved issues and remaining work

- Both objectives have the unique global minimizer `(1,1)` with value zero and are nonconvex. The title and abstract have been corrected accordingly.
- The objective labels have been corrected to `f_1` and `f_2` and grouped using subequations.
- The assignment says Fletcher-Powell, but the supplied class notes and L14 explicitly identify Fletcher-Reeves. Following the user's clarification, the paper and code use nonlinear Fletcher-Reeves, with golden-section search selected by the user.
- L10 section 4b resolves variable steps: at every iteration, evaluate three candidate steps and select the one giving the smallest objective. This rule is implemented.
- Numerical settings and failure handling are implemented and documented in `code/README.md` and the parameter summary in Numerical Results. The abstract remains provisional and should later summarize the measured findings.
- No internet references were searched or invented. The user supplies references, and blue citation placeholders remain in the paper.

## Step 1: Writing methodology first
- Template provided
- Each sentence end with "." will be start by a new line in tex file
- The length of paper is 5 pages
- Problem Formulation is a separate section before Methodology: define the generic unconstrained problem `min_{x in R^n} f(x)`, smoothness assumptions, and gradient/Hessian notation without assuming global convexity. Keep the exact test functions in Numerical Results.
- `root.tex` includes `problem.tex` between Related Work and Methodology. Its current heading is Preliminary, and it includes the generic formulation, definitions, optimality conditions, and a concise general algorithm.
- Agreed organization: present all methods in general form in Methodology, using a generic objective `f`; introduce the exact test functions only in Numerical Results.
- Current Methodology structure: Gradient Method with four step-size strategies, Newton's Method, and nonlinear Fletcher-Reeves. The gradient and line-search subsections were merged at the user's request.
- Numerical Results will define the two test functions, their specific derivatives and minimizer as needed, initial guesses, concrete parameter choices and stopping criteria, and then present trajectories, comparisons, and observations. Do not add a test-function formulation subsection to Methodology.


### Step 1 draft completed (November 11, 2026)
- Wrote `problem.tex`: generic unconstrained problem, smoothness and optimality conditions, gradient/Hessian notation, iterative update, and symbolic stopping criteria.
- Wrote `method.tex`: quadratic-fit and golden-section searches, gradient descent step-size strategies, classical Newton–Raphson, and nonlinear conjugate gradient. Exact test functions remain in Numerical Results. Each prose sentence starts on a new source line.
- Added the supplied textbook to `reference.bib` under `chong2024optimization` and enabled the bibliography in `root.tex`. No external references were searched or added.
- Fletcher-Reeves is now explicitly selected following the supplied class notes. The implementation follows L10 for variable steps and uses the documented line-search and restart settings.
- Compiled successfully with `latexmk` into `/tmp/optimization-paper-check/root.pdf` (two pages for the current incomplete paper). Checked both rendered pages; no overflow was visible and the final LaTeX log contained no warnings or undefined references.
- The title/abstract convexity correction is complete. Introduction, Related Work, Conclusion, and the final abstract still need completion. Final verification of required margins remains pending.

### Citation convention update
- Use `\textcolor{blue}{[cite]}` for all citation placeholders in the paper; the user will supply citations later. This supersedes the earlier citation setup.
- Replaced both textbook citations in Problem Formulation and Methodology with blue placeholders and commented out the bibliography commands in `root.tex`. Existing bibliography entries are preserved for later use.

### Nonquadratic-objective clarification
- Clarified in `method.tex` that quadratic-fit line search interpolates three objective values and does not require a quadratic objective or Taylor expansion.
- Identified Newton's model explicitly as a second-order Taylor approximation, added its little-o remainder relation under the stated twice-continuous-differentiability assumption, and explained that derivatives are reevaluated at each iterate.
- Clarified that nonlinear conjugate gradient works with the original objective and gradients without explicitly constructing a Taylor model; finite termination is only a quadratic-case property under the stated conditions.

### Methodology structure update
- Merged the former one-dimensional search and gradient subsections into one Gradient Method subsection with four subsubsections: Constant Step Size, Variable Step Size, Quadratic Fit, and Golden-Section Search.
- Introduced the gradient update and shared line-search setup before the four strategies. Newton and conjugate gradient remain separate subsections. Updated the conjugate-gradient line-search description to use its own search direction. This supersedes the earlier separate-subsection plan.


## Step 2: Write results scenario

### Step 2 scenario draft
- Drafted Scenario Setup in `result.tex`, preserving the separate results subsections for gradient, Newton, and conjugate-gradient methods.
- Defined and correctly labeled both objectives; supplied their common parameterization, analytic gradient/Hessian, unique global minimizer, and a direct nonconvexity check.
- Specified both starting points, four objective/initialization combinations per configuration, gradient-norm tolerance `1e-3`, and the `20,000`-iteration limit.
- Measured histories and metrics are now saved for all 24 runs. The paper reports iterations, final gradient norms, objective evaluation counts, termination status, and level-curve trajectories. Final objective values and all derivative counts are also retained in `code/results/summary.json`.
- Concrete settings are implemented and recorded under Step 3. Numerical Results now includes a parameter summary. Earlier provisional statements in Methodology can be finalized during the next writing step.

### Algorithm length revision
- Shortened the general algorithm to roughly half its previous length, retaining initialization, direction and step selection, iterate storage, gradient evaluation, and the two stopping conditions. Detailed failure branches were replaced by a brief prose statement.


- For consecutive equations such as (13), (14) and (15), (16), use subequations instead
### Subequation formatting update
- Grouped the two test objectives, their gradient and Hessian, and the conjugate-gradient update pair into subequations with lettered numbering. Preserved equation punctuation and labels.


## Step 3: Code all methods and include figures
- Create folders for each subsection of the methods
- Then go ahead and code them following the methods you wrote down.
- Plotting the results, include to the pdf. You should go back and forth to see if it fit the template.
- Initially add figures without results commentary. The user subsequently authorized a compact results table, convergence plots, and a parameter summary. Detailed results interpretation remains for a later step.
- Use Timenewroman fontsize for the plots.
- Remember to show level curve.
- Suggest me what we should add more.



### Step 3 completion and user approval
- All six configurations are implemented in separate folders under `code/gradient`, `code/newton`, and `code/conjugate_gradient`. No library optimizer is used. `common.py` provides analytic derivatives and iteration handling, and `line_search.py` implements bracketing, golden-section search, and safeguarded quadratic interpolation.
- Reviewed L10, L11, L12, and L14 visually. They cover step choices and interpolation, golden-section search, Newton, and Fletcher-Reeves. L10 resolves the three-candidate variable-step rule, and L14 confirms the conjugate-gradient identity.
- The user reviewed and accepted the Step 3 results. Preserve the accepted numerical settings, histories, and results unless changes are requested.
- Fixed step: `0.005/a`, equal to `0.005` for f1 and `0.00005` for f2. This is constant within each run. Variable steps: choose the best of `{0.005, 0.05, 0.15}/a` at every iterate.
- Bracketing: start at `1/a`, halve until decrease, then double the trial spacing until a right endpoint is no better. Each phase permits 100 attempts. Both searches use width tolerance `1e-12 + 1e-8*abs(best_step)` and a 160-reduction limit. Quadratic interpolation has a golden-fraction fallback for invalid curvature or samples too close to existing points. Full details are in `code/README.md`.
- Newton uses unit steps without Hessian modification. Fletcher-Reeves uses golden-section search and restarts every two iterations or when the proposed direction is not descent.
- All 24 histories and evaluation counts are stored in `code/results`. Twenty-two runs converge. Both constant-step runs for f2 reach the 20,000-iteration cap, and are explicitly marked as iteration-limit outcomes.
- Six trajectory figures show every objective/start combination, with level curves, start and final markers, the known minimizer, and iteration/status annotations. Fonts are embedded Times New Roman. No outcomes were changed to improve presentation.
- `code/checks.py` passes derivative finite-difference checks, known scalar-minimum checks, quadratic interpolation verification, and checks of all run histories, update rules, and stopping statuses.

### Authorized additions and status update (November 17, 2026)
- Added a 24-run comparison table generated directly from `code/results/summary.json` by `code/make_summary_table.py`. It reports iterations, final gradient norm, objective evaluation count, and status. Gradient and Hessian evaluation counts are explained in the setup.
- Added four-panel gradient-norm convergence plots for all methods, with the stopping threshold and actual history endpoints. `code/plot_results.py` regenerates all seven paper figures.
- Added a concise parameter summary to Numerical Results covering the constant and candidate steps, bracketing, search tolerances and limits, quadratic safeguards, Newton steps, and Fletcher-Reeves restarts.
- Kept the accepted numerical runs unchanged. Added descriptive captions and setup details without writing comparative conclusions.
- Reconciled outdated statements in this instruction file. Step 3 remains complete and accepted. The paper now compiles to five pages with no warnings or overfull boxes, and the added table and figures were visually checked.
- Remaining work: Introduction, Related Work, Conclusion, final abstract, detailed results interpretation if requested, user-supplied citations, and final format verification. Further text may require layout adjustments to retain the five-page target.

### Full-width table revision
- Changed the run-summary table to `table*` spanning both columns, with f1 and f2 side by side and separate groups for the two initial points. All 24 runs and metrics are preserved.
- Updated `code/make_summary_table.py` so regeneration retains this layout. The table uses larger text and the full text width.
- Compilation passed without warnings, and the rendered table was visually checked. The paper remains five pages.

### Plot labels and size update
- Per the user's correction, use `x^0=(1.5,2)` and `x^0=(4,5)` instead of start numbers in all plot panel titles and table groups. This is a superscript zero, not a subscript.
- Increased trajectory figure height from 2.95 to 3.30 inches and convergence figure height from 3.15 to 3.50 inches at the same column width. Increased plot text and annotation sizes and reduced some internal spacing to enlarge the axes.
- Updated the generators, regenerated the figures/table without changing numerical results, and visually checked the compiled layout. The paper remains five pages and compiles without warnings.

### Solution columns in results table
- Replaced the objective-evaluation column N_f with final solution coordinates and objective values, generated from the saved accepted data. Retained iteration counts, final gradient norms, and status.
- The full-width table now groups rows by actual initial point and objective to keep the additional columns readable. Coordinates are displayed to six decimal places and objective values to four significant digits.
- The caption states the exact optimum (1,1) with value zero and identifies computed outputs as final estimates. Iteration-limit rows are not described as optimal solutions.
- Updated the generator and table reference sentence. Visually checked the table and compiled successfully without warnings. The paper remains five pages.

### Table layout correction
- Supersedes the preceding solution-column revision: restored the previous table* template with f1 and f2 side by side and groups labeled by x^0.
- Replaced only N_f with the final objective value f(x_K). Removed solution-coordinate columns. Retained K, final gradient norm, and termination status.
- Updated the generator and accompanying table reference. Compilation and visual layout checks passed, with five pages and no warnings.

### Unified objective notation
- Replaced the competing f1, f2, and f_a notation in the paper with f(x,a), where a is fixed at 1 or 100 and only x is optimized. The scenario defines the family in one equation, with derivatives explicitly taken with respect to x.
- Plot titles and table column groups now identify a=1 and a=100. Table objective values use f(x_K,a). Initial-point labels retain x^0.
- Preserved the user's footnotesize table and updated its generator to keep that choice on regeneration. Numerical results are unchanged.
- Regenerated figures and table, compiled without warnings, and visually checked the layout. The paper remains five pages. Earlier references to f1 and f2 in this instruction history mean a=1 and a=100, respectively.
- The current user-edited result section has a Discussion heading and no convergence figure. Preserved this structure and removed its stale convergence-figure cross-reference. The updated convergence plot remains available as a generated asset.


## Step 4: Write the results part
- Based on the plots, table, write the result part.
- in the "Discussion" section, write the comparison between methods

### Step 4 results and discussion drafted
- Wrote method-specific results in `result.tex` using the accepted table, trajectory plots, and saved histories. Reported convergence counts, objective values, and the two constant-step iteration-limit outcomes without changing experiments.
- Verified Newton's objective histories and described its temporary increases in three of four runs, including the a=100, x^0=(4,5) example. Fast termination is not described as monotonic descent.
- Added Discussion comparing updates, objective/derivative evaluation work, sensitivity to initial point and penalty weight, and final accuracy under the common stopping rule. Explicitly noted that the 1/a step scaling also affects the penalty comparison and that these runs do not establish runtime rankings or general guarantees.
- Preserved the table's footnotesize, accepted data, and enlarged plots. Allowed figure floating to fit the added prose without reducing plot size. Figures are referenced from their method-specific text.
- Built in an isolated temporary output directory after the local build encountered a malformed auxiliary file. The clean build passed without warnings or undefined references, produced five pages, and the results pages were visually checked. Copied the verified PDF to the paper's root.pdf.
- Step 4 is drafted for user review. Introduction, Related Work, final abstract, Conclusion content, citations, and final format verification still require the user's next instructions.


## Step 5: Write Introduction and Conclusion

Structure to write introduction:
- Overview of the importance of Opimization.
- Applications to different fields, keep \textcolor{blue}{[cite]} (I will do it)
- Applications to Machine learning.
- Well-known optimization technique => descent.
- In descent technique we have gradident (explain ...), Newton, ....
- This paper proposes a systematic analysis on ....
- Extensive simulation results have been investigates ...
- We show that ...
- Structure of paper..

Total should be 8 citations
### Step 5 Introduction drafted
- Wrote `intro.tex` following the requested progression: optimization importance, engineering and other applications, machine learning, descent methods, gradient/Newton/conjugate-gradient approaches, the comparison scope, measured findings, and paper organization.
- Included exactly eight blue citation placeholders. No references were searched or invented. Preserved the user's current bibliography configuration and disabled Related Work input.
- Described the study as 24 runs and restricted its conclusions to the tested objectives, starting points, and settings. Reported Newton's temporary objective increases and the two constant-step iteration-limit outcomes.
- Checked writing rules and visually inspected the rendered Introduction. The isolated build passed without warnings or undefined references, and the verified PDF was copied to the paper folder.
- Adding the Introduction brings the current paper to six pages. This meets the assignment maximum but exceeds the user's five-page target. Approved existing prose and plot sizes were preserved. A later condensation/layout pass is needed for the five-page target, particularly when adding Conclusion content and finalizing the abstract.


### Step 5 completion update
- The user approved the Introduction and requested a Conclusion. Added `conclusion.tex` summarizing the measured method comparisons, Newton's temporary objective increases, Fletcher-Reeves performance with restarts, and the two constant-step iteration-limit outcomes.
- Limited conclusions to the tested cases and numerical settings. Noted the distinction between iteration counts and computational costs, and identified broader objectives, dimensions, and runtime measurements as future work.
- Introduction retains exactly eight blue citation placeholders. No new citations were added to the Conclusion. Accepted results, table formatting, and figure sizes are unchanged.
- Compiled successfully without warnings and visually checked the Conclusion page. The verified paper remains six pages, within the assignment limit but above the five-page target. Copied the compiled PDF to the paper folder.
- Step 5 drafting is complete. Final abstract revision, user-supplied citations, and final format/page-length review remain pending.

### Abstract finalized from measured results
- Replaced the provisional abstract in root.tex with a 176-word abstract, meeting the requested 150–200-word range.
- Summarized all six configurations and 24 runs, Newton and Fletcher-Reeves iteration counts, the similar gradient line-search outcomes, and the two constant-step iteration-limit cases. Distinguished iteration counts from evaluation costs and limited conclusions to the tested settings.
- No citations were added. Each sentence starts on a new source line. Compilation passed and the paper remains six pages.
