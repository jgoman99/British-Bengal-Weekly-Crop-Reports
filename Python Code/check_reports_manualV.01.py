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

        self.pixmap = QPixmap()


        #Creates Combobox Choice options
        self.choices = listdir(self.folderPath)
        
        #Creating widgets
        #Left
        self.choiceCombo = QComboBox()
        self.choiceCombo.addItems(self.choices)
        self.insertionsLabel = QLabel("Insertions")
        self.insertions = QLineEdit("2")
        self.substitutionsLabel = QLabel("Substitutions")
        self.substitutions = QLineEdit("2")
        self.deletionsLabel = QLabel("Deletions")
        self.deletions = QLineEdit("2")
        self.errorsLabel = QLabel("Errors")
        self.errors = QLineEdit("2")
        self.searchTextOutputLabel = QLabel("Search Results")
        self.searchTextOutput = QTextEdit()
        self.searchTextOutput.setReadOnly(True)
        self.searchStringLabel = QLabel("Search for a word")
        self.searchString = QLineEdit()
        self.searchStringButton = QPushButton("Search")
        #middle
        self.nextImage = QPushButton("Next Image")
        self.previousImage = QPushButton("Previous Image")

        self.scene = QGraphicsScene()

        self.image = QGraphicsView(self.scene)
        self.image.show()

        self.zoomIn = QPushButton("Zoom In")
        self.zoomOut = QPushButton("Zoom Out")



        self.left = QVBoxLayout()
        self.left.setMargin(10)
        self.left.addWidget(self.choiceCombo)
        self.left.addWidget(self.insertionsLabel)
        self.left.addWidget(self.insertions)
        self.left.addWidget(self.substitutionsLabel)
        self.left.addWidget(self.substitutions)
        self.left.addWidget(self.deletionsLabel)
        self.left.addWidget(self.deletions)
        self.left.addWidget(self.errorsLabel)
        self.left.addWidget(self.errors)
        self.left.addWidget(self.searchTextOutputLabel)
        self.left.addWidget(self.searchTextOutput)
        self.left.addWidget(self.searchStringLabel)
        self.left.addWidget(self.searchString)
        self.left.addWidget(self.searchStringButton)

        self.middle = QVBoxLayout()
        self.middle.setMargin(10)
        self.middle.addWidget(self.image)
        self.middle.addWidget(self.nextImage)
        self.middle.addWidget(self.previousImage)
        self.middle.addWidget(self.zoomIn)
        self.middle.addWidget(self.zoomOut)

        # QWidget Layout
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.left)
        self.layout.addLayout(self.middle)



        # Set the layout to the QWidget
        self.setLayout(self.layout)

        # Here we connect widgets to functions
        self.searchStringButton.clicked.connect(self.search_data)
        self.nextImage.clicked.connect(self.next_image)
        self.previousImage.clicked.connect(self.previous_image)
        self.zoomIn.clicked.connect(self.zoom_in)
        self.zoomOut.clicked.connect(self.zoom_out)

    # Here we add functions

    @Slot()
    def search_data(self):
        mydata = self.data
        results = (mydata[mydata["word"]==self.searchString.text()])
        output = ["(" + word + ", " + img + ") " for word, img in zip(results["word"], results["shortName"])]
        print(output)

        #resets search index to 0
        self.searchIndex = 0

        self.searchOutput = results
        print(self.searchOutput)
        self.searchTextOutput.setText(str(output))


    @Slot()
    def next_image(self):
        self.searchIndex += 1

        if self.searchIndex > len(self.searchOutput)-1:
            self.searchIndex = 0


    @Slot()
    def previous_image(self):
        self.searchIndex -= 1

        if self.searchIndex < 0:
            self.searchIndex = len(self.searchOutput)-1




    @Slot()
    def zoom_in(self):

        self.scene.clear()
        self.pixmap = self.pixmap.scaled(self.pixmap.size().width()*1.25, self.pixmap.size().height()*1.25,
                                         Qt.KeepAspectRatio)
        self.scene.addPixmap(self.pixmap)


    @Slot()
    def zoom_out(self):

        self.scene.clear()
        self.pixmap = self.pixmap.scaled(self.pixmap.size().width()*0.8, self.pixmap.size().height()*0.8,
                                         Qt.KeepAspectRatio)
        self.scene.addPixmap(self.pixmap)

    @Slot()
    def post_image(self):
        print("filler")





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
