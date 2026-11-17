"""Reproducible Times New Roman trajectory and convergence figures."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/optimization-mpl')
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D

BASE = Path(__file__).resolve().parent
OUT = BASE.parent/'6ad7d74c9659ce1c2cff5692/figures'
FONT = Path('/System/Library/Fonts/Supplemental/Times New Roman.ttf')
if FONT.exists():
    font_manager.fontManager.addfont(str(FONT))
font_manager.findfont('Times New Roman', fallback_to_default=False)
plt.rcParams.update({'font.family':'Times New Roman','font.size':8.5,
                     'axes.titlesize':8.5,'axes.labelsize':8.5,'xtick.labelsize':7.5,
                     'ytick.labelsize':7.5,'legend.fontsize':7.5,'pdf.fonttype':42,
                     'ps.fonttype':42,'axes.linewidth':.5,'lines.linewidth':1,
                     'mathtext.fontset':'custom','mathtext.rm':'Times New Roman',
                     'mathtext.it':'Times New Roman:italic','mathtext.bf':'Times New Roman:bold'})
NAMES = {'constant':'Constant step','variable':'Three candidate steps',
         'quadratic':'Quadratic-fit search','golden':'Golden-section search',
         'newton':'Newton-Raphson','fletcher_reeves':'Fletcher-Reeves'}
COLORS = {'constant':'#0072B2','variable':'#D55E00','quadratic':'#009E73',
          'golden':'#CC79A7','newton':'#0072B2','fletcher_reeves':'#D55E00'}
rows=json.loads((BASE/'results/summary.json').read_text())
OUT.mkdir(exist_ok=True)

def load(row):
    return np.load(BASE/'results'/(row['key']+'.npz'))

# Match limits across methods for each objective/initialization combination.
limits={}
for a in [1,100]:
    for start in [1,2]:
        paths=[load(r)['trajectory'] for r in rows if r['a']==a and r['key'].endswith(f'start{start}')]
        points=np.vstack(paths+[np.array([[1,1]])])
        low,high=points.min(axis=0),points.max(axis=0)
        pad=np.maximum((high-low)*.10,.12)
        limits[a,start]=(low-pad,high+pad)

for method in NAMES:
    fig,axs=plt.subplots(2,2,figsize=(3.45,3.3))
    for i,a in enumerate([1,100]):
        for j,start in enumerate([1,2]):
            ax=axs[i,j]
            row=next(r for r in rows if r['method']==method and r['a']==a and r['key'].endswith(f'start{start}'))
            data=load(row); path=data['trajectory']
            low,high=limits[a,start]
            xx,yy=np.meshgrid(np.linspace(low[0],high[0],320),np.linspace(low[1],high[1],320))
            z=a*(xx**2-yy)**2+(xx-1)**2
            levels=np.geomspace(.001,max(1,float(z.max())),12)
            contours=ax.contour(xx,yy,z,levels=levels,colors='#aaaaaa',linewidths=.4,zorder=0)
            ax.clabel(contours,levels[2::3],inline=True,fontsize=5.5,fmt='%.2g')
            ax.plot(path[:,0],path[:,1],color=COLORS[method],lw=.85,zorder=2)
            # Mark sparse iterates to indicate the path even when steps are dense.
            idx=np.unique(np.linspace(0,len(path)-1,min(14,len(path)),dtype=int))
            ax.plot(path[idx,0],path[idx,1],'.',color=COLORS[method],ms=1.8)
            ax.plot(*path[0],marker='o',mfc='white',mec='black',ms=3.6,zorder=5)
            ax.plot(*path[-1],marker='s',mfc=COLORS[method],mec='black',mew=.4,ms=3,zorder=5)
            ax.plot(1,1,marker='*',color='black',ms=5.3,zorder=6)
            ax.set(xlim=(low[0],high[0]),ylim=(low[1],high[1]),xlabel='$x_1$',ylabel='$x_2$')
            coords = "(1.5,2)" if start == 1 else "(4,5)"
            ax.set_title(f"$a={a}$, $x^0={coords}$",pad=4)
            status='limit' if row['status']=='iteration_limit' else ('converged' if row['status']=='converged' else 'failed')
            ax.text(.97,.03,f"k={row['iterations']:,}\n{status}",transform=ax.transAxes,
                    ha='right',va='bottom',fontsize=7,bbox=dict(fc='white',ec='none',alpha=.85,pad=.4))
            ax.tick_params(length=2,pad=1)
            ax.xaxis.labelpad=0; ax.yaxis.labelpad=0
    handles=[Line2D([],[],marker='o',mfc='white',color='black',ls='',ms=3,label='Start'),
             Line2D([],[],marker='s',color=COLORS[method],ls='',ms=3,label='Final'),
             Line2D([],[],marker='*',color='black',ls='',ms=5,label='Minimum')]
    fig.legend(handles=handles,loc='lower center',ncol=3,frameon=False,bbox_to_anchor=(.5,-.005),handletextpad=.3,columnspacing=1.1)
    fig.subplots_adjust(left=.13,right=.98,bottom=.13,top=.94,wspace=.38,hspace=.48)
    fig.savefig(OUT/f'{method}_trajectories.pdf')
    fig.savefig(OUT/f'{method}_trajectories.png',dpi=220)
    plt.close(fig)

# Compact convergence figure for the paper, using accepted saved histories.
fig,axs=plt.subplots(2,2,figsize=(3.45,3.5))
styles = dict(zip(NAMES, ['-', '-', '-', '--', '-.', ':']))
colors = dict(zip(NAMES, ['#0072B2','#D55E00','#009E73','#CC79A7','#7A5600','#333333']))
labels = dict(zip(NAMES, ['Constant','Variable','Quadratic','Golden','Newton','FR']))
for i,a in enumerate([1,100]):
    for j,start in enumerate([1,2]):
        ax=axs[i,j]
        for method in NAMES:
            row=next(r for r in rows if r['method']==method and r['a']==a and r['key'].endswith(f'start{start}'))
            norm=load(row)['gradient_norms']
            ax.loglog(np.arange(len(norm))+1,norm,color=colors[method],lw=.85,
                      ls=styles[method],label=labels[method])
        ax.axhline(1e-3,c='black',ls='--',lw=.5)
        coords = '(1.5,2)' if start == 1 else '(4,5)'
        ax.set(title=f'$a={a}$, $x^0={coords}$',xlabel='$k+1$',ylabel='Gradient norm')
        ax.set_xticks([1,100,10000])
        ax.set_yticks([1e-9,1e-6,1e-3,1,1e3])
        ax.tick_params(length=2,pad=1)
        ax.grid(alpha=.15)
        ax.xaxis.labelpad=0; ax.yaxis.labelpad=0
fig.legend(*axs[0,0].get_legend_handles_labels(),loc='lower center',ncol=3,
           frameon=False,columnspacing=.9,handlelength=1.5,handletextpad=.3)
fig.subplots_adjust(left=.16,right=.98,top=.94,bottom=.21,hspace=.55,wspace=.53)
fig.savefig(BASE/'results/convergence.pdf')
fig.savefig(OUT/'convergence.pdf')
fig.savefig(OUT/'convergence.png',dpi=220)
plt.close(fig)
print('Saved six trajectory figures and the convergence figure.')
