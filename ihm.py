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
        self.resize(1000, 600)

        # Menu bar
        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Update data', self.update_data,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_R)
        self.file_menu.addAction('&Update country location', self.update_country_location)
        self.file_menu.addAction('&Change Geocoding Key', self.modal_google_api)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)


        # Combobox part
        label_background = QLabel("Data choice : ", self)
        self.background_choose_list = QComboBox(self)
        self.background_choose_list.addItem("From fossils")
        self.background_choose_list.addItem("From nuclear")
        self.background_choose_list.addItem("From renewable")
        self.background_choose_list.addItem("From hydroelectric")

        # Buttons
        button = QPushButton("Display Map")
        button2 = QPushButton("Display Graph")

        #Main wigdet
        self.main_widget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QVBoxLayout(self.main_widget)

        # Maps part
        self.figure = plt.figure(0)
        self.first_canvas = FigureCanvas(self.figure)

        #Choice Widgets layout
        self.choice_widget = QtWidgets.QWidget(self)
        self.choice_widget_layout = QtWidgets.QHBoxLayout(self.choice_widget)
        self.choice_widget_layout.addWidget(label_background)
        self.choice_widget_layout.addWidget(self.background_choose_list)
        self.choice_widget_layout.addWidget(button)
        self.choice_widget_layout.addWidget(button2)
        self.choice_widget.setFixedHeight(50)

        # Add components in Main layout
        self.layout.addWidget(self.choice_widget)
        self.layout.addWidget(self.first_canvas)


        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("Welcome !", 2000)

        # Events Listeners
        button.clicked.connect(self.draw_map)
        button2.clicked.connect(self.draw_histogram)

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
        try:
            merge_info()
        except NoInternetConnexionException as e:
            QtWidgets.QMessageBox.warning(self, "Update data", str(e))
        else:
            QtWidgets.QMessageBox.about(self, "Update data",
                                        """Data are now up to date"""
                                        )

    def update_country_location(self):
        """
        Update countryCoordonates.json with new country coordonates, open dialog when it's ended
        :return: None
        """
        try:
            get_lat_long()
        except NoInternetConnexionException as e:
            QtWidgets.QMessageBox.warning(self, "Update data", str(e))
        else:
            QtWidgets.QMessageBox.about(self, "Update country coordonates",
                                    """Country coordonates are now up to date"""
                                    )

    def about(self):
        """
        Open a message box with the following text
        :return: None
        """
        QtWidgets.QMessageBox.about(self, "About",
                                    "This is an OpenData project about energies in the world for our Python "
                                    "course.\n\nCoded by COHEN Johana & DELEVACQ Wallerand\n\nFind us on "
                                    "https://github.com/wallforfry/opendata-python "
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

    def draw_map(self):
        """
        Draw the map chosen in the menu
        :return: none
        """
        plt.clf()
        d = {"From fossils": (self.fossil, 'Greys', " Percentage of Fossil Energy Production"), "From nuclear": (self.nuclear, 'Blues', " Percentage of Nuclear Energy Production"), "From renewable": (self.renewable, 'Greens', " Percentage of Renewable Energy Production"), 'From hydroelectric': (self.hydroelectric, "Purples", " Percentage of Hydroelectric Energy Production")}

        LATS = self.latitude
        LONGS = self.longitude
        DATA = d.get(self.background_choose_list.currentText())[0]
        COLOR = d.get(self.background_choose_list.currentText())[1]
        MY_MAP = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=180, lat_ts=20,
                         resolution='c')
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
        CMAP = plt.cm.get_cmap(COLOR)
        #Points size
        SIZE = 70
        # scatter plot des températures
        SCA = MY_MAP.scatter(X_COORD, Y_COORD, s=SIZE, marker='.', c=DATA, cmap=CMAP, zorder=10)
        plt.title(d.get(self.background_choose_list.currentText())[2])
        plt.colorbar(SCA)
        self.first_canvas.draw()

    def draw_histogram(self):
        """
        Handle values of combobox and draw correspondant histogram
        :return: None
        """
        plt.clf()
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

        plt.hist(data, bins=len(data) // 20)
        plt.title("Production ratio of "+title+" energy in the world")
        plt.xlabel("Percentage of "+title)
        plt.ylabel("Number of countries")

        self.first_canvas.draw()




def launch_gui():
    """
    Method called to launch the UI
    :return: None
    """
    app = QtWidgets.QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.show()
    sys.exit(app.exec_())
