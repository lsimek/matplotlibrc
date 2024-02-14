"""
test custom Matplotlib styles (.mplstyle files)
by drawing a number of plots
requirements: matplotlib, seaborn, numpy, scipy
"""

import os

import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
from scipy.stats import t, norm

def draw_plots(style=None, filename=None, **rc_params):
    """
    draw various matplotlib/seaborn plots in chosen style
    saves to plots/filename.png if filename is set
    set additional changes with rc_params

    some plots from https://seaborn.pydata.org/examples/
    """
    if style is not None:
        if not style.endswith('.mplstyle'):
            style += '.mplstyle'
        try:
            plt.style.use(style)
        except FileNotFoundError:
            print(f'Could not find file {style}')
            return

    for key, value in rc_params.items():
        try:
            plt.rcParams[key] = value
        except KeyError:
            print(f'Warning: {key} is not a valid rc parameter.')
            continue

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    bg_color, text_color = plt.rcParams['figure.facecolor'], plt.rcParams['axes.labelcolor']
        
    nrows, ncols = 2, 3
    if (nrows * ncols < 6):
        raise ValueError('Too few plots.')
        
    fig, ax = plt.subplots(nrows, ncols, figsize=np.array(plt.rcParams['figure.figsize'])*np.array([ncols * 1.2, nrows * 1.2]))
    fig.suptitle(f'Various graphs, style={"default" if style is None else style} with {rc_params=}')
    ax_iter = iter(ax.flatten())

    # 1 -- penguins (barplots)
    penguins = sns.load_dataset("penguins")
    g = sns.barplot(
        data=penguins,
        x="species", y="body_mass_g", hue="sex", errorbar=None,
        ax=(ax := next(ax_iter))
    )
    ax.set_ylabel('Body mass (g)')
    g.set_title('Penguin body mass (sns)')

    # 2 -- random walks
    sns.lineplot(
        np.random.choice([1, -1], size=5000).cumsum(),
        ax=(ax := next(ax_iter)),
        label='p=0.5'
    )
    sns.lineplot(
        np.random.choice([1, -1], p=[0.51, 0.49], size=5000).cumsum(),
        ax=ax,
        color=colors[1],
        label='p=0.51'
    )
    sns.lineplot(
        np.random.choice([1, -1], p=[0.49, 0.51], size=5000).cumsum(),
        ax=ax,
        color=colors[2],
        label='p=0.49'
    )
    ax.set_xlabel('Step no.')
    ax.set_ylabel('Distance')
    ax.set_title('Random walks (sns)')

    # 3 -- linear model
    ax = next(ax_iter)
    coeff, inter = 2, 3
    x=np.random.uniform(0, 20, (100, ))
    y=coeff * x + inter + np.random.normal(0, 5, (100, ))
    ax.scatter(x, y)
    ax.plot(x := np.linspace(-2, 22, 1000), coeff * x + inter, linestyle='--', color=colors[1], label='y=2x+3')
    ax.legend()
    ax.grid()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Linear model')

    # 4 -- t distributions
    ax = next(ax_iter)
    dfs = [0.5, 1, 2, 5, 10, 20]
    x = np.linspace(-5, 5, 5000)
    for df in dfs:
        ax.plot(x, t.pdf(x, df), label=f'{df=}')
    ax.plot(x, norm.pdf(x), linestyle=':', alpha=1, color=text_color, label='normal')
    ax.legend()
    ax.set(
        title='t-distributions',
        xlabel='x',
        ylabel='Density'
    )

    # 5 -- smokers (boxplots)
    ax=next(ax_iter)
    tips = sns.load_dataset("tips")
    sns.boxplot(
        x='day', y='total_bill', hue='smoker',
        data=tips, ax=ax
    )
    ax.set(title='Smokers (sns)', xlabel='Day of the week', ylabel='Total bill')

    # 6 -- penguins II (swarmplot)
    ax = next(ax_iter)
    df = sns.load_dataset('penguins')
    ax = sns.swarmplot(data=df, x='body_mass_g', y='sex', hue='species')
    ax.set(title='Penguins II (sns)', xlabel='Body mass (g)', ylabel='')

    # save plots to folder plots/
    if filename is not None:
        os.makedirs('plots/', exist_ok=True)
        if not filename.endswith('.png'):
            filename += '.png'
        path = f'plots/{filename}'
        no = 1

        while os.path.exists(path):
            path = f'plots/{filename}-{(no := no + 1)}.png'
        
        plt.savefig(path)
        
if __name__ == '__main__':
    for style in [
        None,
        'seagreen-light-thick.mplstyle',
        'seagreen-light-thin.mplstyle',
        'lavender-dark-thick.mplstyle',
        'lavender-dark-thin.mplstyle'
    ]:
        name = style[:-len('.mplstyle')] if style is not None else 'default'
        draw_plots(style=style, filename=f'{name}.png')

