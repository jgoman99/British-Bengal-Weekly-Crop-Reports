import sys
from PySide2.QtCore import Qt, Slot, QPointF
from PySide2.QtGui import QPainter, QPixmap, QColor, QPolygonF
from PIL.ImageQt import ImageQt
from PySide2.QtWidgets import (QAction, QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QTextEdit,
                               QGraphicsRectItem, QGraphicsPolygonItem, QComboBox)
import os
from os import listdir
from os.path import isfile, join
from PySide2.QtCharts import QtCharts

import pandas as pd


# TODO change to fuzzy matching
class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.scene = QGraphicsScene()
        self.image = QGraphicsView(self.scene)
        self.image.show()
        self.submitButton = QPushButton("Submit")
        self.dateText = QLineEdit("")
        self.prevPageButton = QPushButton("Previous Page")
        self.nextPageButton = QPushButton("Next Page")
        self.middle = QVBoxLayout()
        self.left = QHBoxLayout()
        self.middle.setMargin(10)
        self.middle.addWidget(self.image)
        self.middle.addLayout(self.left)
        self.left.addWidget(self.prevPageButton)
        self.left.addWidget(self.nextPageButton)
        self.middle.addWidget(self.dateText)
        self.middle.addWidget(self.submitButton)

        # QWidget Layout

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.middle)

        # Set the layout to the QWidget
        self.setLayout(self.layout)

        #second
        self.data_path = "../Crop_Reports/Manual Check Crop Reports/crop_reports_verified.csv"
        self.data = pd.read_csv(self.data_path)
        self.dir_path = "../Crop_Reports/Bengal Crop Reports PNG/"
        #connect functions
        self.submitButton.clicked.connect(self.submit)
        self.nextPageButton.clicked.connect(self.nextImage)
        self.prevPageButton.clicked.connect(self.prevImage)


        self.crop_index = 0
        self.page_index = 0
        self.zoom = .2
        self.reports = os.listdir(self.dir_path)
        reports_already_done = set(self.data.ocr_report_path)
        lst = self.reports
        for finished in reports_already_done:
            lst.remove(finished)

        self.reports = lst

        remain_string = "remaining folders " + str(len(self.reports))
        self.remainingLabel = QLabel(remain_string)
        self.left.addWidget(self.remainingLabel)


        temp_path = os.path.join(self.dir_path,self.reports[self.crop_index])
        self.report = os.listdir(temp_path)

        if (len(self.report)>0):
            self.page = self.report[self.page_index]
            temp_path = os.path.join(self.dir_path,self.reports[self.crop_index],self.page)
            print(temp_path)
            self.pixmap = QPixmap(temp_path)
            self.scene.clear()
            self.pixmap = QPixmap(temp_path)
            #adjusts zoom
            self.pixmap = self.pixmap.scaled(self.pixmap.size().width() * self.zoom, self.pixmap.size().height() * self.zoom,
                                             Qt.KeepAspectRatio)
            self.scene.addPixmap(self.pixmap)

            #key bindings
            def key_press(event):
                key = event.char
                print(key, 'is pressed')


    @Slot()
    def submit(self):
        self.write_to_csv()
        self.page_index=0

        self.crop_index = self.crop_index + 1

        self.postImage()
        self.dateText.setText("")
        remain_string = "remaining folders " + str(len(self.reports)-self.crop_index)
        self.remainingLabel.setText(remain_string)


    @Slot()
    def nextImage(self):
        if ((len(self.report)-1) > self.page_index):
            self.page_index = self.page_index + 1
        else:
            self.page_index = 0

        self.postImage()

    @Slot()
    def prevImage(self):
        if (1 > self.page_index):
            self.page_index = len(self.report) - 1
        else:
            self.page_index = self.page_index - 1

        self.postImage()


    def postImage(self):
        temp_path = os.path.join(self.dir_path,self.reports[self.crop_index])
        self.report = os.listdir(temp_path)

        if (len(self.report)>0):
            print(self.page_index)
            self.page = self.report[self.page_index]
            temp_path = os.path.join(self.dir_path, self.reports[self.crop_index], self.page)
            print(temp_path)
            self.scene.clear()
            self.pixmap = QPixmap(temp_path)
            #adjusts zoom
            self.pixmap = self.pixmap.scaled(self.pixmap.size().width() * self.zoom, self.pixmap.size().height() * self.zoom,
                                             Qt.KeepAspectRatio)
            self.scene.addPixmap(self.pixmap)



    def write_to_csv(self):
        new_row = {'ocr_report_path': self.reports[self.crop_index], 'date': self.dateText.text()}
        self.data = self.data.append(new_row, ignore_index=True)
        self.data.to_csv(self.data_path, index=False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.submit()


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
