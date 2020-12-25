import sys
from PySide2.QtCore import Qt, Slot, QPointF
from PySide2.QtGui import QPainter, QPixmap, QColor, QPolygonF
from PIL.ImageQt import ImageQt
from PySide2.QtWidgets import (QAction, QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QTextEdit, QGraphicsRectItem, QGraphicsPolygonItem, QComboBox)
import os
from os import listdir
from os.path import isfile, join
from PySide2.QtCharts import QtCharts

import pandas as pd




#TODO change to fuzzy matching
class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        #Paths
        self.folderPath = "../Crop_Reports/Bengal Crop Reports PNG/"
        self.index = 0
        self.page_index = 0
        self.crop_report = ""
        self.pixmap = QPixmap()

        self.data = pd.read_csv("../Crop_Reports/Manual Check Crop Reports/crop_reports_verified.csv")

        #choices
        self.choices = listdir(self.folderPath)




        self.scene = QGraphicsScene()
        self.image = QGraphicsView(self.scene)
        self.image.show()
        self.submitButton = QPushButton("Submit")
        self.dateText = QLineEdit("")



        self.middle = QVBoxLayout()
        self.middle.setMargin(10)
        self.middle.addWidget(self.image)

        self.middle.addWidget(self.dateText)
        self.middle.addWidget(self.submitButton)


        # QWidget Layout
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.middle)



        # Set the layout to the QWidget
        self.setLayout(self.layout)

        # Here we connect widgets to functions
        self.submitButton.clicked.connect(self.submit)


    # Here we add functions

    @Slot()
    def submit(self):
        self.index = self.index+1
        self.scene.clear()

        temp_path = self.choices[self.index]
        self.crop_report_pages = os.listdir(temp_path)

        self.pixmap = QPixmap(temp_path)
        self.scene.addPixmap(self.pixmap)

    @Slot()
    def nextPage(self):
        self.page_index = self.page_index + 1









class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Tutorial")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        self.setCentralWidget(widget)


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    widget = Widget()
    # QMainWindow using QWidget as central widget
    window = MainWindow(widget)
    window.resize(800, 600)
    window.show()

    # Execute application
    sys.exit(app.exec_())
