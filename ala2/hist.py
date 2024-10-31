import matplotlib.pyplot as plt
import numpy as np
import torch
# Force matplotlib to not use any Xwindows backend.
# matplotlib.use('Agg')

import multiprocessing


import time


def calculateFES(df, grid, sigma2=np.pi / 360):
    torsion = np.array([df[1], df[2]]).T

    l = grid.shape[0]
    fes = np.zeros(l)
    N = len(df.index)
    for i in range(l):
        t = grid[i]
        diff = np.abs(torsion - t)
        diff[diff > np.pi] = 2 * np.pi - diff[diff > np.pi]
        fes[i] = np.sum(np.exp(-np.sum(diff**2, axis=1) / 2 / sigma2)) / N

    return fes


def calculateFES_step(df, grid, sigma2, q, i):
    fes = calculateFES(df, grid, sigma2)
    print(fes)
    q[i] = fes


def calculateFES_multi(df, grid, nump, sigma2=np.pi / 360):
    l = grid.shape[0]
    n = int(l / nump)
    p = []
    q = multiprocessing.Manager().dict()
    fes = np.zeros(l)
    for i in range(nump):
        p.append(multiprocessing.Process(target=calculateFES_step,
                 args=(df, grid[i * n:i * n + n, :], sigma2, q, i)))
        p[-1].start()

    for i in range(nump):
        p[i].join()
        print(f"{i} process complete")

    for i in range(nump):
        fes[i * n:i * n + n] = q[i]
    return fes


def hist(data, xmin, xmax, ymin, ymax, Nbins, hist=None):
    dx = (xmax - xmin) / Nbins
    dy = (ymax - ymin) / Nbins
    dd = data - np.array([xmin, ymin])
    if hist is None:
        bins = np.zeros((Nbins, Nbins))
    else:
        bins = hist
    for i in range(data.shape[0]):
        x, y = int(np.floor(dd[i, 0] / dx)), int(np.floor(dd[i, 1] / dy))
        bins[x, y] = bins[x, y] + 1
    return bins


def hist_reweight(data, value, xmin, xmax, ymin, ymax, Nbins, hist=None):
    dx = (xmax - xmin) / Nbins
    dy = (ymax - ymin) / Nbins
    dd = data - np.array([xmin, ymin])
    if hist is None:
        bins = np.zeros((Nbins, Nbins))
    else:
        bins = hist

    for i in range(data.shape[0]):
        x, y = int(np.floor(dd[i, 0] / dx)), int(np.floor(dd[i, 1] / dy))
        bins[x, y] = bins[x, y] + value[i]
    return bins


def grid(xmin, xmax, ymin, ymax, xbins, ybins):
    x, y = np.linspace(xmin, xmax, xbins), np.linspace(ymin, ymax, ybins)
    x, y = np.meshgrid(x, y)
    return np.column_stack((x.flatten(), y.flatten()))


if __name__ == '__main__':

    DEBUG = True
    samples = 20

    # first, run a long simulation
    # run_macro_simulation(debug=DEBUG)
    ngrid = 180
    grid = np.linspace(-np.pi, np.pi, ngrid)
    y, x = np.meshgrid(grid, grid)
    y = y.flatten()
    x = x.flatten()
    g = np.array([x, y]).T
    filename = 'ala2/simulation/COLVAR_test'
    # filename='simulation/long/COLVAR'
    data = np.loadtxt(filename)
    print(data[:, 1:3])

    # fes=calculateFES_multi(df,grid,16)
    h = hist_reweight(data[:, 1:3], np.ones_like(
        data[:, 0]), -np.pi, np.pi, -np.pi, np.pi, ngrid)

    h = h.flatten()
    plt.clf()
    plt.scatter(g[:, 0][h > 0], g[:, 1][h > 0],
                cmap='turbo', c=np.log(h[h > 0]), s=1)
    plt.xlabel('$\\phi$')
    plt.ylabel('$\\psi$')
    plt.colorbar(label='FES')
    plt.savefig('fes_2.png', dpi=300)
    plt.clf()

    # draw point density
    '''
    pi=3.14159265
    plt.hist2d(df[1], df[2],range=[[-pi,pi], [-pi, pi]],bins=360,norm=LogNorm())
    plt.colorbar()

    # "improved" x/y axis ticks


    # axis labels (right order?)
    plt.xlabel('$\\phi$')
    plt.ylabel('$\\psi$')

    # 1:1 aspect ratio

    # remove grid lines
    print("Saving figure 'Ramachandran-Plot'")
    plt.savefig('Ramachandran-Plot.png', dpi=300)
    plt.clf()
    '''
