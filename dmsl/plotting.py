'''
Makes plots
'''


import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pymc3 as pm
import seaborn as sns
import corner
import numpy as np
import pandas as pd
import scipy

from datetime import datetime
from dmsl.convenience import flatten, prange, make_file_path
from dmsl.paths import *
from pymc3.backends.tracetab import trace_to_dataframe

def paper_plot():
    sns.set_context("paper")
    sns.set_style('ticks')
    sns.set_palette('colorblind')
    plt.rc('font', family='serif', serif='cm10')
    figparams = {
            'text.latex.preamble': r'\usepackage{amsmath} \boldmath \bf',
            'text.usetex':True,
            'axes.labelsize':16.,
            'xtick.labelsize':12,
            'ytick.labelsize':12,
            'figure.figsize':[6., 4.],
            'font.family':'DejaVu Sans',
            'legend.fontsize':12}
    plt.rcParams.update(figparams)
    cs = plt.rcParams['axes.prop_cycle'].by_key()['color']
    return cs

def plot_emcee(flatchain,nstars, nsamples,ndims, massprofile, surveyname,
        usefraction):
    massprofiletype = massprofile.type
    kwargs = massprofile.kwargs
    flatchain = np.array(flatchain)
    if usefraction:
        kwargs['f'] = 0
    for key in kwargs.keys():
        print(key)
        extra_string = f'post_{surveyname}_{massprofiletype}_{key}'
        if usefraction:
            extra_string += '_frac'
        outpath = make_file_path(RESULTSDIR, [np.log10(nstars),
            np.log10(nsamples), ndims],
                extra_string=extra_string,
                ext='.png')
        plt.close('all')
        paper_plot()
        i = 0
        if key == 'Ml': i  = 0
        else: i = 1
        fig = plt.figure()
        try:
            up95 = np.percentile(flatchain[:,i],90)
            plt.hist(flatchain[:, i], 50, color="k", histtype="step", density=True);
        except:
            up95 = np.percentile(flatchain, 90)
            plt.hist(flatchain, 50, color="k", histtype="step", density=True);
        plt.axvline(up95)
        if key == 'f':
            plt.xlabel(r'$f$');
        else:
            plt.xlabel(f'$\\log_{{10}} {key}$');
        plt.ylabel(f'$p({key})$');
        savefig(fig, outpath, writepdf=0, dpi=100)
    plt.close('all')
    fig = corner.corner(flatchain)
    extra_string = f'corner_{surveyname}_{massprofiletype}'
    if usefraction:
        extra_string += '_frac'
    outpath = make_file_path(RESULTSDIR, [np.log10(nstars),
        np.log10(nsamples), ndims],
        extra_string=extra_string, ext='.png')
    savefig(fig, outpath, writepdf=0, dpi=100)

def plot_chains(samples, outpath):
    plt.close('all')
    paper_plot()
    fig = plt.figure()
    plt.plot(samples[:,:,0])
    plt.ylabel(r'$\log_{10} M_l$');
    plt.xlabel(r'N');
    savefig(fig, outpath, writepdf=0, dpi=100)

def plot_logprob(samples, outpath):
    plt.close('all')
    paper_plot()
    fig = plt.figure()
    plt.plot(np.abs(samples[100:]))
    plt.yscale('log')
    plt.ylabel(r'$\mid \log \mathcal{L} \mid$');
    plt.xlabel(r'N');
    savefig(fig, outpath, writepdf=0, dpi=100)

def plot_sensitivity(flatchain, outpath):
    plt.close('all')
    cs = paper_plot()
    fig, ax = plt.subplots()
    xs = np.linspace(0, 8, 100)
    plt.plot(xs, 0.35*xs-2, c='black', label='Mishra-Sharma 95\% limit',
            linewidth=2)
    sns.kdeplot(flatchain[:,0], flatchain[:,1], ax=ax, shade=True,
            n_levels=3, cmap='Blues_r')
    fig.legend()
    ax.set_xlim([0, 8])
    ax.set_ylim([-3., 3.])
    ax.set_xlabel(r'$\log_{10} M_l$');
    ax.set_ylabel(r'$\log_{10} R~[\rm{pc}]$');
    savefig(fig, outpath, writepdf=False, dpi=100)

def make_histogram(data,bins, data_name, outpath):
    plt.close('all')
    cs = paper_plot()
    f = plt.figure()
    plt.hist(data, bins=bins, histtype='step', linewidth=3)
    plt.xlabel(f'${data_name}$')
    plt.ylabel('$N$')
    savefig(f, outpath, writepdf=False, dpi=100)

def plot_hists(samples, outpath):
    '''
    makes multiple hists on 1 plot based on samples, which should be a
    dictionary
    '''
    plt.close('all')
    cs = paper_plot()
    f = plt.figure()
    for i, (key, value) in enumerate(samples.items()):
        plt.hist(value, 50, histtype='step', linewidth=2, label=key,
                density=True, color=cs[i])
        up95 = np.percentile(value, 90)
        plt.axvline(up95, color=cs[i], lw=3, linestyle='dashed')
    plt.xlabel(r'$\log_{10} M_l$');
    plt.ylabel(r'$p(\log_{10} M_l)$');
    plt.legend();
    savefig(f, outpath, writepdf=False, dpi=300)

def make_scatter(x,y,axislabels, outpath):
    size = int(20*(len(x)/1000)**(-1))
    plt.close('all')
    cs = paper_plot()
    f = plt.figure()
    plt.scatter(x,y, s=size)
    plt.xlabel(f'${axislabels[0]}$')
    plt.ylabel(f'${axislabels[1]}$')
    savefig(f, outpath, writepdf=False, dpi=100)

def plot_corner(trace, outpath):
    # corner plot of posterior samples
    plt.close('all')
    corvars = [x for x in trace.varnames if x[-1] != '_']
    trace_df = trace_to_dataframe(trace, varnames=corvars)
    fig = corner.corner(trace_df,quantiles=[0.16, 0.5, 0.84],
                        show_titles=True, title_kwargs={"fontsize": 12},
                        title_fmt='.2g')
    savefig(fig, outpath, writepdf=0, dpi=100)

def savefig(fig, figpath, writepdf=True, dpi=450):
    fig.savefig(figpath, dpi=dpi, bbox_inches='tight')
    print('{}: made {}'.format(datetime.now().isoformat(), figpath))

    if writepdf:
        pdffigpath = figpath.replace('.png','.pdf')
        fig.savefig(pdffigpath, bbox_inches='tight', dpi=dpi)
        print('{}: made {}'.format(datetime.now().isoformat(), pdffigpath))

    plt.close('all')

def plot_lens_vector_field(x,y,lensx, lensy, rs_arcsec, outpath):
    ## use a weird symlog because lensx, lensy < 1.
    magnorm = np.sqrt(lensx**2+lensy**2)
    norm = matplotlib.colors.LogNorm(vmin=magnorm[np.nonzero(magnorm)].min(), vmax=magnorm.max())
    cm = matplotlib.cm.Blues
    sm = matplotlib.cm.ScalarMappable(cmap=cm, norm=norm)
    sm.set_array([])
    plt.close('all')
    paper_plot()
    fig1, ax1 = plt.subplots()
    ax1.set_aspect('equal')
    Q = ax1.quiver(x/rs_arcsec,y/rs_arcsec,lensx/magnorm, lensy/magnorm,
            color=cm(norm(magnorm)), pivot='mid', units='width', scale=3./1.,
            scale_units='xy')
    plt.annotate('', xy=(-3, -2), xytext=(-3, -3),
            arrowprops=dict(facecolor='black', shrink=0.05))
    plt.text(-2.9, -2.9,r'$v_l$', fontsize=20)
    circle1 = plt.Circle((0, 0), 1., color='k', fill=False,
            linewidth=0.5)
    ax1.add_artist(circle1)
    circle2 = plt.Circle((0, 0), 2., color='k', fill=False,
            linewidth=0.5)
    ax1.add_artist(circle2)
    circle3 = plt.Circle((0, 0), 3., color='k', fill=False,
            linewidth=0.5)
    ax1.add_artist(circle3)
    plt.scatter(0.0,0.0, marker='x',color='black', s=36)
    plt.colorbar(sm, label=r'$\|\alpha\|~[\mu\rm{as/yr}^2]$')
    plt.xlabel(r'$b_x/r_s$')
    plt.ylabel(r'$b_y/r_s$')
    savefig(fig1, outpath, writepdf=False)
    return fig1, ax1
