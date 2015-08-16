#! coding:utf-8
"""

matplotlibを使ったグラフウィジェット


"""
import sys

from PySide import QtGui, QtCore

import matplotlib

matplotlib.rcParams['backend.qt4'] = 'PySide'
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
import matplotlib.pyplot as plt


class MplCanvas(FigureCanvas):
    """ FigureCanvasウィジェット
    """

    def __init__(self, parent=None, width=5, height=4, dpi=72):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=[0.5, 0.5, 0.5], edgecolor=None, linewidth=1.0,
                          frameon=True, tight_layout=True)
        self.axes = self.fig.add_subplot(111)
        self.step = 1

        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        # Init figure
        self.compute_initial_fiugre()

        # Constractor
        FigureCanvas.__init__(self, self.fig)
        # Set Parent to QWidget
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)

        FigureCanvas.updateGeometry(self)

        self.timer = QtCore.QTimer(self)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.animate_fiugre)
        self.timer.setInterval(50)
        self.timer.start()

    def compute_initial_fiugre(self):
        dt = 0
        t = np.arange(0.0 + dt, 3.0 + dt, 0.01)
        s = np.sin(2. * np.pi * t) + np.sin(2. * np.pi * (1 / 3) * t)
        self.axes.plot(t, s)
        pass

    def animate_fiugre(self):
        """ super class method
        you write child class
        """
        # print 'compute_initial_figure'
        self.step += 1
        dt = 0.05 * self.step

        t = np.arange(0.0 + dt, 3.0 + dt, 0.01)
        A = np.sin(2. * np.pi * (0.1) * self.step)
        s = A * np.sin(2. * np.pi * t) + np.sin(2. * np.pi * (2.) * t)

        # self.axes.set_title('Google Analytics Statistics Data')
        self.axes.plot(t, s)
        self.axes.set_xlim(t[0], t[-1])
        self.draw()
        pass

    def update_figure(self, xdata=None, ydata=None):
        print 'update_figure'
        self.timer.stop()

        gxdata = range(len(xdata))
        gydata = ydata

        self.axes.plot(gxdata, gydata, 'r')

        # self.axes.set_title('google analystics statistics data')
        self.axes.set_title('URL : wedding movie cgi.ge*******/j***73/')

        self.axes.set_xlabel('days')
        self.axes.set_ylabel('users')
        self.axes.grid(True)

        self.axes.set_xticks(gxdata[::10])
        self.axes.set_xticklabels(xdata[::10], rotation=40)
        self.axes.tick_params(axis='x', labelsize=8)
        self.axes.tick_params(axis='y', labelsize=8)

        self.draw()
        pass


###################################################
#
# Demo
#
###################################################
class MplWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.canvas = MplCanvas()
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

        print type(self.canvas)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = MplWidget()
    w.show()
    sys.exit(app.exec_())
