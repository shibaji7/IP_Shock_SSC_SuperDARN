#!/usr/bin/env python

"""plot_utils.py: module is dedicated to plot different types of parameters"""

__author__ = "Chakraborty, S."
__copyright__ = "Copyright 2020, SuperDARN@VT"
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "shibaji7@vt.edu"
__status__ = "Research"

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, num2date
from matplotlib import patches
import matplotlib.patches as mpatches
import random


import utils

class RangeTimePlot(object):
    """
    Create plots for velocity or power.
    """

    def __init__(self, nrang, fig_title, num_subplots=1):
        self.nrang = nrang
        self.unique_gates = np.linspace(1, nrang, nrang)
        self.num_subplots = num_subplots
        self._num_subplots_created = 0
        self.fig = plt.figure(figsize=(8, 3*num_subplots), dpi=100) # Size for website
        plt.suptitle(fig_title, x=0.075, y=0.99, ha="left", fontweight="bold", fontsize=15)
        mpl.rcParams.update({"font.size": 10})
        return

    def _tight_layout(self):
        #self.fig.tight_layout(rect=[0, 0, 0.9, 0.97])
        return
    
    def show(self):
        plt.show()
        return
    
    def save(self, filepath):
        plt.savefig(filepath, bbox_inches="tight")
        return
    
    def close(self):
        self.fig.clf()
        plt.close()
        return

    def _add_axis(self):
        self._num_subplots_created += 1
        ax = self.fig.add_subplot(self.num_subplots, 1, self._num_subplots_created)
        return ax

    def _add_colorbar(self, fig, ax, bounds, colormap, label=""):
        """
        Add a colorbar to the right of an axis.
        :param fig:
        :param ax:
        :param bounds:
        :param colormap:
        :param label:
        :return:
        """
        import matplotlib as mpl
        pos = ax.get_position()
        cpos = [pos.x1 + 0.025, pos.y0 + 0.0125,
                0.015, pos.height * 0.9]                # this list defines (left, bottom, width, height
        cax = fig.add_axes(cpos)
        norm = mpl.colors.BoundaryNorm(bounds, colormap.N)
        cb2 = mpl.colorbar.ColorbarBase(cax, cmap=colormap,
                norm=norm,
                ticks=bounds,
                spacing="uniform",
                orientation="vertical")
        cb2.set_label(label)
        return

    def addPlot(self, df, beam, param="v", title="", pmax=200, step=25, xlabel="Time UT"):
        # add new axis
        df = df[df.bmnum==beam]
        self.ax = self._add_axis()
        # set up variables for plotter
        time = np.hstack(df["time"])
        gate = np.hstack(df["slist"])
        flags = np.hstack(df["v"])
        bounds = list(range(-pmax, pmax+1, step))
        cmap = plt.cm.jet
        
        X, Y, Z = utils.get_gridded_parameters(df, xparam="time", yparam="slist", zparam="v")
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        # cmap.set_bad("w", alpha=0.0)
        # Configure axes
        self.ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))
        hours = mdates.HourLocator(byhour=range(0, 24, 4))
        self.ax.xaxis.set_major_locator(hours)
        self.ax.set_xlabel(xlabel)
        self.ax.set_xlim([df.time.tolist()[0], df.time.tolist()[-1]])
        self.ax.set_ylabel("Range gate")
        self.ax.pcolormesh(X, Y, Z.T, lw=0.01, edgecolors="None", cmap=cmap, norm=norm)
        
        self._tight_layout()    # need to do this before adding the colorbar, because it depends on the axis position
        self._add_colorbar(self.fig, self.ax, bounds, cmap, label="Velocity [m/s]")
        self.ax.set_title(title, loc="left", fontdict={"fontweight": "bold"})
        return
