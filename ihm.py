"""
Project : OpenData-python
File : ihm.py
Author : DELEVACQ Wallerand
Date : 28/03/2017
"""

from __future__ import unicode_literals
import sys
import os
import random
import matplotlib

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

from functools import partial


class ApplicationWindow(QtWidgets.QMainWindow):
    """
    Main window of the app. This window contain button, menus, maps and graphs
    """

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("OpenData Python")

        # Menu bar
        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtWidgets.QWidget(self)

        # First combobox part
        label_points = QLabel("Points :", self)
        self.points_choose_list = QComboBox(self)
        self.points_choose_list.addItem("Consumption")
        self.points_choose_list.addItem("Production")

        # Second combobox part
        label_background = QLabel("Map's background : ", self)
        self.background_choose_list = QComboBox(self)
        self.background_choose_list.addItem("From fossils")
        self.background_choose_list.addItem("From nuclear")
        self.background_choose_list.addItem("From renewable")

        # Buttons
        button = QPushButton("Display first map")
        button2 = QPushButton("Display second map")

        # Maps part
        self.layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.figure = plt.figure(0)
        self.first_canvas = FigureCanvas(self.figure)

        # Add components in layout
        self.layout.addWidget(label_points)
        self.layout.addWidget(self.points_choose_list)
        self.layout.addWidget(label_background)
        self.layout.addWidget(self.background_choose_list)
        self.layout.addWidget(self.first_canvas)
        self.layout.addWidget(button)
        self.layout.addWidget(button2)


        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("Welcome !", 2000)

        # Events Listeners
        button.clicked.connect(self.plot_map)
        button2.clicked.connect(self.plot_map2)
        self.points_choose_list.activated.connect(partial(self.choose_points))
        self.background_choose_list.activated.connect(partial(self.choose_background))

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        """
        Open a message box with the following text
        :return: None
        """
        QtWidgets.QMessageBox.about(self, "About",
                                    """This is an OpenData project about energies in the world for our Python course"""
                                    )

    def plot_map(self):
        m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80, \
                    llcrnrlon=-180, urcrnrlon=180, lat_ts=20, resolution='c')
        m.drawcoastlines()
        m.fillcontinents(color='coral', lake_color='aqua')
        # draw parallels and meridians.
        m.drawparallels(np.arange(-90., 91., 30.))
        m.drawmeridians(np.arange(-180., 181., 60.))
        m.drawmapboundary(fill_color='aqua')
        self.first_canvas.draw()

    def plot_map2(self):
        m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80, \
                    llcrnrlon=-180, urcrnrlon=180, lat_ts=20, resolution='c')
        m.drawcoastlines()
        m.fillcontinents(color='red', lake_color='aqua')
        # draw parallels and meridians.
        m.drawparallels(np.arange(-90., 91., 30.))
        m.drawmeridians(np.arange(-180., 181., 60.))
        m.drawmapboundary(fill_color='blue')
        self.first_canvas.draw()

    def choose_points(self):
        """
        Handle values of the first combobox
        :return: None
        """
        value = self.points_choose_list.currentText()
        print(value)
        if value == "Consumption":
            pass
        elif value == "Production":
            pass
        else:
            pass

    def choose_background(self):
        """
        Handle values of the second combobox
        :return: None
        """
        value = self.background_choose_list.currentText()
        print(value)

        if value == "From fossile":
            pass
        elif value == "From nuclear":
            pass
        elif value == "From renewable":
            pass
        else:
            pass


def launch_gui():
    """
    Method called to launch the UI
    :return: None
    """
    app = QtWidgets.QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.show()
    sys.exit(app.exec_())
