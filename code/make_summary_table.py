"""Generate the two-column paper table from accepted experiment data."""
import json
from pathlib import Path
base = Path(__file__).resolve().parent
rows = json.loads((base/'results/summary.json').read_text())
names = {'constant':'Constant', 'variable':'Variable', 'quadratic':'Quadratic',
         'golden':'Golden', 'newton':'Newton', 'fletcher_reeves':'Fletcher-Reeves'}
lines = [r'\begin{table*}[!t]', r'\centering',
         r'\caption{Run summary. $K$ is the number of updates, $f(\boldsymbol{x}_K,a)$ is the final objective value, and $\|\boldsymbol{g}_K\|_2$ is the final gradient norm. C denotes convergence and L the iteration limit. The initial point is denoted by $x^0$.}',
         r'\label{tab:run-summary}', r'\begingroup', r'\footnotesize',
         r'\setlength{\tabcolsep}{3pt}',
         r'\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lrrrcrrrc@{}}',
         r'\toprule',
         r' & \multicolumn{4}{c}{$a=1$} & \multicolumn{4}{c}{$a=100$} \\',
         r'\cmidrule(lr){2-5}\cmidrule(lr){6-9}',
         r'Method & $K$ & $\|\boldsymbol{g}_K\|_2$ & $f(\boldsymbol{x}_K,a)$ & Status & $K$ & $\|\boldsymbol{g}_K\|_2$ & $f(\boldsymbol{x}_K,a)$ & Status \\',
         r'\midrule']
for start in [1, 2]:
    coords = '(1.5,2)' if start == 1 else '(4,5)'
    lines.append(r'\multicolumn{9}{c}{$x^0='+coords+r'$} \\')
    for method, name in names.items():
        fields = [name]
        for a in [1, 100]:
            row = next(r for r in rows if r['method']==method and r['a']==a and r['key'].endswith('start'+str(start)))
            fields += [str(row['iterations']), f"{row['gradient_norm']:.3e}",
                       f"{row['f']:.3e}", 'C' if row['status']=='converged' else 'L']
        lines.append(' & '.join(fields)+r' \\')
    lines.append(r'\midrule')
lines[-1] = r'\bottomrule'
lines += [r'\end{tabular*}', r'\endgroup', r'\end{table*}']
(base.parent/'6ad7d74c9659ce1c2cff5692/summary_table.tex').write_text('\n'.join(lines)+'\n')
