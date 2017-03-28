"""
Project : OpenData-python
File : ihm.py
Author : DELEVACQ Wallerand
Date : 28/03/2017
"""

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QPushButton

class GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(600, 500)
        self.move(300, 300)
        self.setWindowTitle('OpenData Python')
        self.setWindowIcon(QIcon('icon.png'))

    def showUI(self):
        self.show()

    def createButton(self, text, tooltip, x, y):
        btn = QPushButton(text, self)
        btn.setToolTip(tooltip)
        btn.resize(btn.sizeHint())
        btn.move(x, y)
        # btn.clicked.connect(self.method)

    def createCB(self):
        cb = QCheckBox('Change title', self)
        cb.move(20, 20)
        cb.stateChanged.connect(self.check_action)
        cb.toggle()

    def check_action(self, state):

        if state == Qt.Checked:
            self.setWindowTitle('Checked')
        else:
            self.setWindowTitle('OpenData python')


def main():
    app = QApplication(sys.argv)
    gui = GUI()
    gui.createButton("test", "tooltip", 50, 50)
    gui.createCB()
    gui.show()
    app.exec()
