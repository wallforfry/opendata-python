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
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

from functools import partial

from dataProvider import *

class ApplicationWindow(QtWidgets.QMainWindow):
    """
    Main window of the app. This window contain button, menus, maps and graphs
    """

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        # Get infos from parser
        #self.infos = get_infos()

        self.infos = []
        with open("data.json", mode="r") as f:
            self.infos = json.load(f)

        self.consumption = []
        self.fossil = []
        self.nuclear = []
        self.hydroelectric = []
        self.renewable = []
        self.longitude = []
        self.latitude = []

        for elt in self.infos:
            consumption = elt.get("consumption")
            self.consumption.append(consumption[:consumption.find(" ")])
            fossil = str(elt.get("fossil"))
            self.fossil.append(fossil[:fossil.find("%")])
            nuclear = str(elt.get("nuclear"))
            self.nuclear.append(nuclear[:nuclear.find("%")])
            hydroelectric = str(elt.get("hydroelectric"))
            self.hydroelectric.append(hydroelectric[:hydroelectric.find("%")])
            other = str(elt.get("other"))
            self.renewable.append(other[:other.find("%")])
            self.longitude.append(float(elt.get("coordonates").get("lng")))
            self.latitude.append(float(elt.get("coordonates").get("lat")))



        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("OpenData Python")
        self.setWindowIcon(QIcon('icon.png'))

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
        button.clicked.connect(self.draw_map)
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
        self.figure.clear()

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
        self.figure.clear()

    def draw_map(self):

        STATIONS = ['ABBEVILLE', 'AJACCIO', 'ALENCON', 'BALE-MULHOUSE',
                    'BELLE ILE-LE TALUT', 'BORDEAUX-MERIGNAC', 'BOURGES',
                    'BREST-GUIPAVAS', 'CAEN-CARPIQUET', 'CAP CEPET',
                    'CLERMONT-FD', 'DIJON-LONGVIC', 'EMBRUN', 'GOURDON',
                    'LE PUY-LOUDES', 'LILLE-LESQUIN', 'LIMOGES-BELLEGARDE',
                    'LYON-ST EXUPERY', 'MARIGNANE', 'MILLAU', 'MONT-DE-MARSAN',
                    'MONTELIMAR', 'MONTPELLIER', 'NANCY-OCHEY',
                    'NANTES-BOUGUENAIS', 'NICE', 'ORLY', 'PERPIGNAN',
                    "PLOUMANAC'H", 'POITIERS-BIARD', 'PTE DE CHASSIRON',
                    'PTE DE LA HAGUE', 'REIMS-PRUNAY', 'RENNES-ST JACQUES',
                    'ROUEN-BOOS', 'ST GIRONS', 'STRASBOURG-ENTZHEIM',
                    'TARBES-OSSUN', 'TOULOUSE-BLAGNAC', 'TOURS', 'TROYES-BARBEREY']

        LATS = [50.136, 41.918, 48.4455, 47.614333, 47.294333,
                44.830667, 47.059167, 48.444167, 49.18, 43.079333,
                45.786833, 47.267833, 44.565667, 44.745, 45.0745,
                50.57, 45.861167, 45.7265, 43.437667, 44.1185,
                43.909833, 44.581167, 43.577, 48.581, 47.15,
                43.648833, 48.716833, 42.737167, 48.825833,
                46.593833, 46.046833, 49.725167, 49.209667,
                48.068833, 49.383, 43.005333, 48.5495, 43.188,
                43.621, 47.4445, 48.324667]

        LONGS = [1.834, 8.792667, 0.110167, 7.51, -3.218333, -0.691333,
                 2.359833, -4.412, -0.456167, 5.940833, 3.149333, 5.088333,
                 6.502333, 1.396667, 3.764, 3.0975, 1.175, 5.077833, 5.216,
                 3.0195, -0.500167, 4.733, 3.963167, 5.959833, -1.608833,
                 7.209, 2.384333, 2.872833, -3.473167, 0.314333, -1.4115,
                 -1.939833, 4.155333, -1.734, 1.181667, 1.106833, 7.640333,
                 0.0, 1.378833, 0.727333, 4.02]

        TEMPS = [7.6, 13.5, 7.6, 6.8, 10.5, 11.5, 8.5, 9.7, 8.6, 11.8, 9.1,
                 7.2, 5.7, 9.2, 6.0, 7.2, 7.6, 8.4, 12.0, 6.1, 11.6, 9.6, 11.7,
                 6.5, 10.0, 11.7, 8.1, 12.6, 9.9, 9.1, 10.8, 9.5, 7.4, 9.0,
                 7.1, 10.3, 6.7, 10.8, 10.6, 8.4, 8.1]

        MIN_TEMP = min(TEMPS)
        MY_MAP = Basemap(llcrnrlon=-10, llcrnrlat=40, urcrnrlon=10, urcrnrlat=55,
                         rsphere=(6378137.00, 6356752.3142), resolution='l',
                         projection='merc')
        MY_MAP.bluemarble()
        MY_MAP.drawcoastlines()
        MY_MAP.drawmapboundary(fill_color='aqua')
        MY_MAP.drawcountries()
        MY_MAP.drawparallels(np.arange(40, 60, 5), labels=[1, 1, 0, 1])
        MY_MAP.drawmeridians(np.arange(-5, 15, 5), labels=[1, 1, 0, 1])
        # Conversion des coordonnées géographiques en coordonnées graphiques
        X_COORD, Y_COORD = MY_MAP(LONGS, LATS)
        # Get a color map
        CMAP = plt.cm.get_cmap('Oranges')
        # Construction d'un tableau de taille des points affichés
        SIZE = (np.array(TEMPS) - MIN_TEMP + 1) * 20
        # scatter plot des températures
        SCA = MY_MAP.scatter(X_COORD, Y_COORD, s=SIZE, marker='o', c=TEMPS, cmap=CMAP)
        plt.title('Température moyenne à 12:00 (janvier 2014)')
        plt.colorbar(SCA)
        #plt.show()
        self.first_canvas.draw()
        self.figure.clear()

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
