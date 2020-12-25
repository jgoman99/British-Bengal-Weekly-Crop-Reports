import sys

from PySide2 import QtCore
from PySide2.QtCore import Qt, Slot, QPointF, QPoint
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
import ocr_to_data as dt

# will have to glue together words?
# save two copies, one df, one bounds?
start_date = '01-01-1910'
end_date = '01-01-1911'

# TODO change to fuzzy matching
class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.x1 = ""
        self.x3 = ""
        self.y1 = ""
        self.y3 = ""

        self.scene = QGraphicsScene()
        self.image = QGraphicsView(self.scene)
        self.image.show()
        self.submitButton = QPushButton("Submit")
        self.undoButton = QPushButton("Undo")
        self.nextReport = QPushButton("Next Report")
        self.districtText = QLineEdit("")
        self.prevPageButton = QPushButton("Previous Page")
        self.nextPageButton = QPushButton("Next Page")
        self.middle = QVBoxLayout()
        self.left = QHBoxLayout()
        self.middle.setMargin(10)
        self.middle.addWidget(self.image)
        self.middle.addLayout(self.left)
        self.bottom = QHBoxLayout()
        self.left.addWidget(self.prevPageButton)
        self.left.addWidget(self.nextPageButton)
        self.middle.addWidget(self.districtText)
        self.bottom.addWidget(self.nextReport)
        self.bottom.addWidget(self.undoButton)
        self.bottom.addWidget(self.submitButton)
        self.middle.addLayout(self.bottom)

        # QWidget Layout

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.middle)

        # Set the layout to the QWidget
        self.setLayout(self.layout)

        # second
        # self.data_path = "../Crop_Reports/Manual Check Crop Reports/crop_reports_verified.csv"
        # self.data = pd.read_csv(self.data_path)
        self.dir_path = "../Crop_Reports/Bengal Crop Reports PNG/"
        # connect functions
        self.nextReport.clicked.connect(self.ignore)
        self.submitButton.clicked.connect(self.submit)
        self.undoButton.clicked.connect(self.undo)
        self.nextPageButton.clicked.connect(self.nextImage)
        self.prevPageButton.clicked.connect(self.prevImage)

        self.crop_index = 0
        self.page_index = 0
        self.zoom = .125

        self.out_folder = "../Crop_Reports/Bengal Crop Reports OCR Bounds/"
        self.finished = os.listdir(self.out_folder)
        self.data = pd.read_csv("../Crop_Reports/Manual Check Crop Reports/crop_reports_verified_cleaned_is_good.csv")
        self.data.Date = pd.to_datetime(self.data.Date)
        self.data = self.data[(self.data.Date > start_date) & (self.data.Date < end_date)]

        self.columns = ["District","x1","y1","x3","y3","Date","Raw_Text"]
        self.bound_data = pd.DataFrame(columns = self.columns)
        self.bound_data_text = ""

        self.ocr_data_list = list()

        data = self.data
        for string in self.finished:
            string = string.split(".")[0]
            data = data[data.Path != string]



        self.reports = list(data.Path)
        self.dates = list(data.Date)
        print(u"Data index:",data.index)


        self.remain_string = "remaining folders " + str(len(self.reports))
        self.remainingLabel = QLabel(self.remain_string)
        self.left.addWidget(self.remainingLabel)

        temp_path = os.path.join(self.dir_path, self.reports[self.crop_index])
        self.report = os.listdir(temp_path)
        self.postImage()

        # Sets up drawing capabilities:
        self.image.setMouseTracking(True)
        self.image.viewport().installEventFilter(self)
        self.start = None
        self.end = None

    # error here, disregarded bc why not? :)
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress and source is self.image.viewport():
            self.start = event.pos()
            #print(event.pos())
            #print(self.image.mapToScene(event.pos()))

        if event.type() == QtCore.QEvent.MouseButtonRelease and source is self.image.viewport():
            self.end = event.pos()
            self.draw_bounding_box()

    @Slot()
    def submit(self):
        self.postImage()

        ["District", "x1", "y1", "x3", "y3", "Date", "Raw_Text"]
        row = {'District':self.districtText.text(), 'x1':self.x1, 'y1':self.y1, 'x3':self.x3,'y3':self.y3,'Date':self.date,'Raw_Text':self.bound_data_text}
        self.bound_data = self.bound_data.append(row, ignore_index= True)
        print(self.bound_data)

        self.districtText.setText("")

    @Slot()
    def undo(self):
        print(self.bound_data)
        self.bound_data.drop(self.bound_data.tail(1).index, inplace=True)
        print(self.bound_data)

    @Slot()
    def ignore(self):
        self.remain_string = "remaining folders " + str(len(self.reports)-self.crop_index-1)
        self.remainingLabel.setText(self.remain_string)

        path = self.out_folder + self.reports[self.crop_index] + ".csv"
        print(u"out path:",path)

        self.bound_data.to_csv(path, index= False)
        self.bound_data = pd.DataFrame(columns = self.columns)


        self.crop_index = self.crop_index + 1
        self.page_index = 0
        self.postImage()






    @Slot()
    def nextImage(self):
        if ((len(self.report) - 1) > self.page_index):
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
        self.date = self.dates[self.crop_index]
        print(u"Date:",self.date)
        print(self.dates)
        temp_path = os.path.join(self.dir_path, self.reports[self.crop_index])
        report = os.listdir(temp_path)
        dt.sort_nicely(report)
        self.report = report
        self.ocr_data_list = dt.report_to_data(self.reports[self.crop_index])

        if (len(self.report) > 0):
            self.page = self.report[self.page_index]
            self.page_df = self.ocr_data_list[self.page_index]
            temp_path = os.path.join(self.dir_path, self.reports[self.crop_index], self.page)
            self.scene.clear()
            self.pixmap = QPixmap(temp_path)
            # adjusts zoom
            self.pixmap = self.pixmap.scaled(self.pixmap.size().width() * self.zoom,
                                             self.pixmap.size().height() * self.zoom,
                                             Qt.KeepAspectRatio)
            self.scene.addPixmap(self.pixmap)



    # def draw_bounding_box(self, x1, y1, x3, y3):
    #
    #     start = self.image.mapToScene(x1,y1)
    #     end = self.image.mapToScene(x3,y3)
    #     len_x = end.x()-start.x()
    #     len_y = end.y()-start.y()
    #     rectItem = QGraphicsRectItem(start.x(), start.y(), len_x, len_y)
    #     self.scene.addItem(rectItem)

    def draw_bounding_box(self):
        #self.item = QGraphicsPixmapItem(QPixmap(self.df["image"].iloc[self.index]))
        #self.scene.addItem(self.item)
        start = self.image.mapToScene(self.start)
        end = self.image.mapToScene(self.end)
        self.startSceneLoc = start
        self.endSceneLoc = end
        diff_x = (start.x() - end.x())
        diff_y = (start.y() - end.y())

        df = self.page_df

        scale = (1/self.zoom)
        self.x1 = start.x()*scale
        self.x3 = end.x()*scale
        self.y1 = start.y()*scale
        self.y3 = end.y()*scale
        df = df[(df.x1 > self.x1) & (df.x3 < self.x3) & (df.y1 > self.y1) & (df.y3 < self.y3)]
        print(u"x1:",self.x1,u" x3:",self.x3, u" y1:", self.y1, u" y3:",self.y3, u" Scale:", scale)
        print(u"Current image:",self.report[self.page_index], u" Current df image:", df.image.unique())
        print(df.word)
        self.bound_data_text = " ".join(df.word.to_list())

        rectItem = QGraphicsRectItem(start.x(), start.y(), -diff_x, -diff_y)
        self.scene.addItem(rectItem)

    # def write_to_csv(self):
    #     new_row = {'ocr_report_path': self.reports[self.crop_index], 'date': self.districtText.text()}
    #     self.data = self.data.append(new_row, ignore_index=True)
    #     self.data.to_csv(self.data_path, index=False)

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
