
import sys

from PySide2 import QtCore
from PySide2.QtCore import Qt, Slot, QPointF, QPoint
from PySide2.QtGui import QPainter, QPixmap, QColor, QPolygonF, QPen, QBrush
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
from xml.etree import ElementTree as ET

import extract_tables_from_xml as my

# TODO change to fuzzy matching
class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QVBoxLayout()
        #fix this
        self.scale = 4.16
        self.zoom = 2
        self.anchor_list = []
        self.top_anchor = []
        self.bottom_anchor = []
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        # fix this
        #self.filenames = ["../Other Data/Medical Data/nls-data-indiaPapers/91541450/image/" + x for x in os.listdir("../Other Data/Medical Data/nls-data-indiaPapers/91541450/image/")]
        #"91541967.3",
        # use write table no number
        #self.filenames = ["91540775.3","91540907.3","91541048.3","91541159.3","91541336.3"]
        self.filenames = ["91541574.3"]
        self.filenames_full = ["../Other Data/Medical Data/nls-data-indiaPapers/91541450/image/" + x + ".jpg" for x in self.filenames]
        self.index = 0
        self.jpg_path = self.filenames_full[self.index]
        print(self.jpg_path)
        self.xml = self.jpg_path.split("/image")[0] + "/alto/" + self.jpg_path.split("/image/")[1].split(".")[0] + ".34.xml"

        self.pixmap = QPixmap(self.jpg_path)
        print(u"pixmap width height", self.pixmap.width())
        self.pixmap = self.pixmap.scaled(self.pixmap.size().width()*self.zoom,
                                         self.pixmap.size().height()*self.zoom,
                                         Qt.KeepAspectRatio)

        #only for images that need rotate
        self.view.rotate(90)


        self.data = self.getData()
        self.scene.addPixmap(self.pixmap)

        self.layout.addWidget(self.view)

        self.b1 = QHBoxLayout()
        self.b2 = QHBoxLayout()
        self.b3 = QHBoxLayout()
        self.yearLabel = QLabel("Year:")
        self.yearEdit = QLineEdit()
        self.yearSubmit = QPushButton("Submit Year")
        self.b1.addWidget(self.yearLabel)
        self.b1.addWidget(self.yearEdit)
        self.b1.addWidget(self.yearSubmit)
        self.topAnchorLabel = QLabel("Top Anchor: ")
        self.topAnchorButton = QPushButton("Top Anchor")
        self.b2.addWidget(self.topAnchorLabel)
        self.b2.addWidget(self.topAnchorButton)

        self.bottomAnchorLabel = QLabel("Bottom Anchor: ")
        self.bottomAnchorButton = QPushButton("Bottom Anchor")
        self.b3.addWidget(self.bottomAnchorLabel)
        self.b3.addWidget(self.bottomAnchorButton)

        self.layout.addLayout(self.b1)
        self.layout.addLayout(self.b2)
        self.layout.addLayout(self.b3)
        self.submitButton = QPushButton("Submit")
        self.layout.addWidget(self.submitButton)

        self.setLayout(self.layout)
        self.view.show()

        # Sets up drawing capabilities:
        self.view.setMouseTracking(True)
        self.view.viewport().installEventFilter(self)
        self.start = None
        self.end = None

        #connects to function
        self.topAnchorButton.clicked.connect(self.topAnchorFunction)
        self.bottomAnchorButton.clicked.connect(self.bottomAnchorFunction)
        self.submitButton.clicked.connect(self.table_to_csv)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress and source is self.view.viewport():
            self.start = event.pos()
            self.start = self.view.mapToScene(self.start)
            print(u"mouse", self.start)

        if event.type() == QtCore.QEvent.MouseButtonRelease and source is self.view.viewport():
            self.end = event.pos()
            self.end = self.view.mapToScene(self.end)
            self.drawBox()
            self.select_table()


    def select_table(self):
        data = self.data
        data.HPOS = data.HPOS.astype(int)
        data.VPOS = data.VPOS.astype(int)
        x1 = self.start.x()*self.scale*(1/self.zoom)
        y1 = self.start.y()*self.scale*(1/self.zoom)
        x3 = self.end.x()*self.scale*(1/self.zoom)
        y3 = self.end.y()*self.scale*(1/self.zoom)
        table = data[(data.HPOS > x1) & (data.HPOS < x3) & (data.VPOS > y1) & (data.VPOS < y3)]

        my_list = self.anchor_list
        my_list.append(table.CONTENT[0])
        self.anchor_list = self.anchor_list
        print(self.anchor_list)



    @Slot()
    def topAnchorFunction(self):
        self.top_anchor = self.anchor_list
        self.topAnchorLabel.setText(str(self.top_anchor))
        self.anchor_list = []

    @Slot()
    def bottomAnchorFunction(self):
        self.bottom_anchor = self.anchor_list
        self.bottomAnchorLabel.setText(str(self.bottom_anchor))
        self.anchor_list = []

    @Slot()
    def table_to_csv(self):
        my.write_table_2(self.xml,self.top_anchor,self.bottom_anchor,self.yearEdit.text(),self.jpg_path)


    def drawBox(self):
        x1 = self.start.x()
        y1 = self.start.y()
        x3 = self.end.x()
        y3 = self.end.y()
        diff_x = x3-x1
        diff_y = y3-y1
        rectItem = QGraphicsRectItem(x1, y1, diff_x, diff_y)
        #rectItem.setBrush(QBrush(Qt.green))
        self.scene.addItem(rectItem)

    def getData(self):
        # will replace with one
        tree = ET.parse(self.xml)

        root = tree.getroot()

        NSMAP = {
            'mw': 'http://www.loc.gov/standards/alto/v3/alto.xsd'
        }
        pass
        all_name_elements = tree.findall('.//mw:TextLine', NSMAP)

        base = list(all_name_elements[0].getchildren()[0].attrib.items())
        column_names = pd.DataFrame(base, columns=['key', 'value']).transpose().iloc[0]
        master_df = pd.DataFrame()
        i = 0
        while i < len(all_name_elements):
            data_list = list(all_name_elements[i].getchildren()[0].attrib.items())
            if len(column_names) == len(data_list):
                df = pd.DataFrame(data_list, columns=['key', 'value'])
                row = df.transpose().iloc[1]
                master_df = master_df.append(row)
            else:
                print("Something wrong")
                print(data_list)
            i = i + 1

        master_df = master_df.rename(columns=column_names)

        return (master_df)








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
