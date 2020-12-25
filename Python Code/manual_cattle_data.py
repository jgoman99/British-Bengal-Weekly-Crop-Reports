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
import ocr_to_data as dt

# will have to glue together words?
# save two copies, one df, one bounds?
start_date = '01-01-1930'
end_date = '01-01-1933'
index_districts = pd.read_csv("../Crop_Reports/Bengal Cattle Data/cg1930p1_folder_0.csv")
index_districts = index_districts.District.to_list()

# TODO change to fuzzy matching
class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.index_districts = index_districts

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
        self.badButton = QPushButton("BAD")
        self.goodButton = QPushButton("Good")
        self.noDataButton = QPushButton("No Data")
        self.districtText = QLineEdit("")
        self.cattleLabel = QLineEdit("Cattle:")
        self.top = QHBoxLayout()
        self.top.addWidget(self.cattleLabel)
        self.prevPageButton = QPushButton("Previous Page")
        self.nextPageButton = QPushButton("Next Page")
        self.middle = QVBoxLayout()
        self.left = QHBoxLayout()
        self.middle.setMargin(10)
        self.middle.addWidget(self.image)
        self.middle.addLayout(self.top)
        self.middle.addLayout(self.left)
        self.bottom = QHBoxLayout()
        self.left.addWidget(self.prevPageButton)
        self.left.addWidget(self.nextPageButton)
        self.middle.addWidget(self.districtText)
        self.bottom.addWidget(self.badButton)
        self.bottom.addWidget(self.noDataButton)
        self.bottom.addWidget(self.goodButton)
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
        self.zoom = .2

        self.out_folder = "../Crop_Reports/Bengal Cattle Data/"
        self.finished = os.listdir(self.out_folder)
        self.data = pd.read_csv("../Crop_Reports/Manual Check Crop Reports/crop_reports_verified_cleaned_is_good.csv")
        self.data.Date = pd.to_datetime(self.data.Date)
        self.data = self.data[(self.data.Date > start_date) & (self.data.Date < end_date)]

        self.columns = ["District","Date","Cattle_Result"]
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

        #something
        #self.draw_boxes()

    # error here, disregarded bc why not? :)
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease and source is self.image.viewport():
            if event.button() == Qt.RightButton:
                self.nextImage()

            if event.button() == Qt.MidButton:
                self.ignore()

            if event.button() == Qt.LeftButton:
                self.draw_bounding_box()

            #print(event.pos())
            #print(self.image.mapToScene(event.pos()))




    @Slot()
    def submit(self, cattle_result):
        self.postImage()


        ["District", "x1", "y1", "x3", "y3", "Date", "Raw_Text"]
        row = {'District':self.districtText.text(),'Date':self.date,'Cattle_Result': cattle_result}
        self.bound_data = self.bound_data.append(row, ignore_index= True)
        print(self.bound_data)

        self.districtText.setText("")
        cattle_label_text = "Length: " + str(len(self.bound_data.Cattle_Result)) + ". " + str(list(self.bound_data.Cattle_Result))
        self.cattleLabel.setText(cattle_label_text)

    @Slot()
    def undo(self):
        print(self.bound_data)
        self.bound_data.drop(self.bound_data.tail(1).index, inplace=True)

        cattle_label_text = "Length: " + str(len(self.bound_data.Cattle_Result)) + ". " + str(list(self.bound_data.Cattle_Result))
        self.cattleLabel.setText(cattle_label_text)

        print(self.bound_data)

    @Slot()
    def ignore(self):
        self.remain_string = "remaining folders " + str(len(self.reports)-self.crop_index-1)
        self.remainingLabel.setText(self.remain_string)

        path = self.out_folder + self.reports[self.crop_index] + ".csv"
        print(u"out path:",path)

        self.bound_data.District = self.index_districts
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
            self.draw_bounding_box()



    # def draw_bounding_box(self, x1, y1, x3, y3):
    #
    #     start = self.image.mapToScene(x1,y1)
    #     end = self.image.mapToScene(x3,y3)
    #     len_x = end.x()-start.x()
    #     len_y = end.y()-start.y()
    #     rectItem = QGraphicsRectItem(start.x(), start.y(), len_x, len_y)
    #     self.scene.addItem(rectItem)



    def draw_bounding_box(self):
        df = self.page_df

        scale = self.zoom
        no_df = df[df.word=="no"]
        tle_df = df[df.word.str.contains("tle", na = False)]
        catt_df = df[df.word.str.contains("catt", na=False)]
        rinder_df = df[df.word.str.contains("inder", na=False)]

        for index, row in no_df.iterrows():
            print(row)
            x1 = row.x1*scale
            y1 = row.y1*scale
            x3= row.x3*scale
            y3 = row.y3*scale
            diff_x = x3-x1
            diff_y = y3-y1
            rectItem = QGraphicsRectItem(x1,y1,diff_x,diff_y)
            rectItem.setBrush(QBrush(Qt.green))
            #rectItem = QGraphicsRectItem(0, 0, 100, 100)
            self.scene.addItem(rectItem)

        for index, row in tle_df.iterrows():
            print(row)
            x1 = row.x1 * scale
            y1 = row.y1 * scale
            x3 = row.x3 * scale
            y3 = row.y3 * scale
            diff_x = x3 - x1
            diff_y = y3 - y1
            rectItem = QGraphicsRectItem(x1, y1, diff_x, diff_y)
            rectItem.setBrush(QBrush(Qt.red))
            # rectItem = QGraphicsRectItem(0, 0, 100, 100)
            self.scene.addItem(rectItem)

        for index, row in rinder_df.iterrows():
            print(row)
            x1 = row.x1 * scale
            y1 = row.y1 * scale
            x3 = row.x3 * scale
            y3 = row.y3 * scale
            diff_x = x3 - x1
            diff_y = y3 - y1
            rectItem = QGraphicsRectItem(x1, y1, diff_x, diff_y)
            rectItem.setBrush(QBrush(Qt.red))
            # rectItem = QGraphicsRectItem(0, 0, 100, 100)
            self.scene.addItem(rectItem)

        for index, row in catt_df.iterrows():
            print(row)
            x1 = row.x1 * scale
            y1 = row.y1 * scale
            x3 = row.x3 * scale
            y3 = row.y3 * scale
            diff_x = x3 - x1
            diff_y = y3 - y1
            rectItem = QGraphicsRectItem(x1, y1, diff_x, diff_y)
            rectItem.setBrush(QBrush(Qt.red))
            # rectItem = QGraphicsRectItem(0, 0, 100, 100)
            self.scene.addItem(rectItem)

        # divider_x = (max(df.x3)-min(df.x1))/2
        # week_df = df[df.word.str.contains("icient", na=False)]
        # for index, row in week_df.iterrows():
        #     week_anchor = row
        #
        #     x1 = week_anchor.x1 * scale
        #     y1 = week_anchor.y1 * scale
        #     x3 = week_anchor.x3 * scale
        #     y3 = week_anchor.y3 * scale
        #     diff_x = x3 - x1
        #     diff_y = y3 - y1
        #     rectItem = QGraphicsRectItem(x1, y1, diff_x, diff_y)
        #     rectItem.setBrush(QBrush(Qt.blue))
        #     self.scene.addItem(rectItem)

        # right_df = df[df.x1 > divider_x]
        # right_df = right_df[right_df.y1 > week_anchor.y3]
        # for index, row in right_df.iterrows():
        #     x1 = row.x1 * scale
        #     y1 = row.y1 * scale
        #     x3 = row.x3 * scale
        #     y3 = row.y3 * scale
        #     diff_x = x3 - x1
        #     diff_y = y3 - y1
        #
        #     rectItem = QGraphicsRectItem(x1, y1, diff_x, diff_y)
        #     rectItem.setBrush(QBrush(Qt.red))
        #
        #     self.scene.addItem(rectItem)

        # for district in self.index_districts:
        #     print(district)
        #     row = df[df.word.str.contains(district, na=False)]
        #
        #     if (len(row.word) != 0):
        #         x1 = row.x1 * scale
        #         y1 = row.y1 * scale
        #         x3 = row.x3 * scale
        #         y3 = row.y3 * scale
        #         diff_x = x3 - x1
        #         diff_y = y3 - y1
        #
        #         rectItem = QGraphicsRectItem(x1, y1, diff_x, diff_y)
        #         rectItem.setBrush(QBrush(Qt.red))
        #
        #         self.scene.addItem(rectItem)









    # def write_to_csv(self):
    #     new_row = {'ocr_report_path': self.reports[self.crop_index], 'date': self.districtText.text()}
    #     self.data = self.data.append(new_row, ignore_index=True)
    #     self.data.to_csv(self.data_path, index=False)

    # reformat first half of year 1910 before 10/6
    def keyPressEvent(self, event):

        if event.key() == Qt.Key_A:
            #disease
            self.submit("bad")

        if event.key() == Qt.Key_W:
            # no mention
            self.submit("NR")

        if event.key() == Qt.Key_D:
            ##not bad
            self.submit("not_bad")




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
