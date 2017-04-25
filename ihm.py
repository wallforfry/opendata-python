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
from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton, QInputDialog

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import normal

from functools import partial

from dataProvider import *


class ApplicationWindow(QtWidgets.QMainWindow):
    """
    Main window of the app. This window contain button, menus, maps and graphs
    """

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        # Get infos from parser
        self.infos = get_infos_for_basemap()
        self.country = self.infos.get("country")
        self.consumption = self.infos.get("consumption")
        self.fossil = self.infos.get("fossil")
        self.nuclear = self.infos.get("nuclear")
        self.hydroelectric = self.infos.get("hydroelectric")
        self.renewable = self.infos.get("renewable")
        self.latitude = self.infos.get("latitude")
        self.longitude = self.infos.get("longitude")

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("OpenData Python")
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(1000, 700)

        # Menu bar
        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Update data', self.update_data,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_R)
        self.file_menu.addAction('&Update counrty location', self.update_country_location)
        self.file_menu.addAction('&Change Geocoding Key', self.modal_google_api)
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
        self.background_choose_list.addItem("From hydroelectric")

        # Buttons
        button = QPushButton("Display first map")
        button2 = QPushButton("Display second map")

        # Maps part
        self.layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.figure = plt.figure(0)
        self.first_canvas = FigureCanvas(self.figure)
        self.first_canvas.draw()

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
        #button2.clicked.connect(self.plot_map2)
        button2.clicked.connect(self.draw_histogram)
        self.points_choose_list.activated.connect(partial(self.choose_points))
        #self.background_choose_list.activated.connect(partial(self.choose_background))
        self.background_choose_list.activated.connect(partial(self.draw_histogram))

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def update_data(self):
        """
        Update data.json with new data, open dialog when it's ended
        :return: None
        """
        # get_lat_long()
        merge_info()
        QtWidgets.QMessageBox.about(self, "Update data",
                                    """Data are now up to date"""
                                    )

    def update_country_location(self):
        """
        Update countryCoordonates.json with new country coordonates, open dialog when it's ended
        :return: None
        """
        get_lat_long()
        QtWidgets.QMessageBox.about(self, "Update country coordonates",
                                    """Country coordonates are now up to date"""
                                    )

    def about(self):
        """
        Open a message box with the following text
        :return: None
        """
        QtWidgets.QMessageBox.about(self, "About",
                                    """This is an OpenData project about energies in the world for our Python course"""
                                    )

    def modal_google_api(self):
        """
        Open a message box with line edit to change Google Maps Geocoding API Key
        :return:
        """
        last_value = get_google_api_key()
        key_value, okPressed = QInputDialog.getText(self, "Enter Api Key", "Google Maps Geocoding Api Key :",
                                                    text=last_value)

        if okPressed:
            set_google_api_key(key_value)

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
        m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=180, lat_ts=20,
                    resolution='c')
        m.drawcoastlines()
        m.fillcontinents(color='red', lake_color='aqua')
        # draw parallels and meridians.
        m.drawparallels(np.arange(-90., 91., 30.))
        m.drawmeridians(np.arange(-180., 181., 60.))
        m.drawmapboundary(fill_color='blue')
        self.first_canvas.draw()
        self.figure.clear()

    def draw_map(self):

        LATS = self.latitude
        LONGS = self.longitude
        TEMPS = self.fossil

        print(LATS)
        print(len(LONGS))
        print(len(TEMPS))

        MIN_TEMP = min(TEMPS)
        MY_MAP = Basemap(projection='robin', lat_0=0, lon_0=-100,
                         resolution='l', area_thresh=1000.0)
        # MY_MAP.bluemarble()
        MY_MAP.drawcoastlines()
        MY_MAP.drawmapboundary(fill_color='aqua')
        MY_MAP.drawcountries()
        MY_MAP.fillcontinents(color='coral')
        MY_MAP.drawmeridians(np.arange(0, 360, 30))
        MY_MAP.drawparallels(np.arange(-90, 90, 30))
        # Conversion des coordonnées géographiques en coordonnées graphiques
        X_COORD, Y_COORD = MY_MAP(LONGS, LATS)
        # Get a color map
        CMAP = plt.cm.get_cmap('Greens')
        # Construction d'un tableau de taille des points affichés
        SIZE = (np.array(TEMPS) - MIN_TEMP + 1) * 20
        # scatter plot des températures
        SCA = MY_MAP.scatter(X_COORD, Y_COORD, s=SIZE, marker='o', c=TEMPS, cmap=CMAP)
        plt.title('Température moyenne à 12:00 (janvier 2014)')
        plt.colorbar(SCA)
        # plt.show()
        self.first_canvas.draw()
        self.figure.clear()

    def draw_histogram(self):
        """
        Handle values of combobox and draw correspondant histogram
        :return: None
        """
        value = self.background_choose_list.currentText()

        if value == "From fossils":
            data = self.fossil
            title = "fossile"
        elif value == "From nuclear":
            data = self.nuclear
            title = "nuclear"
        elif value == "From renewable":
            data = self.renewable
            title = "renewable"
        elif value == "From hydroelectric":
            data = self.hydroelectric
            title = "hydroelectric"
        else:
            return

        plt.hist(data, bins=len(data)//20)
        plt.title("Consumption ratio of "+title+" energie in the world")
        plt.xlabel("Percentage of "+title)
        plt.ylabel("Number of country")

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

    # On First launch ask Api Key
    if get_google_api_key() == "":
        aw.modal_google_api()

    sys.exit(app.exec_())
