# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qtGUI.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QStatusBar, QTextEdit, QWidget)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtSvg import *
from regex2nfa import regex2nfa, transformAux 
from visualize_nfa import visualize, prepareForDrawing
import time
import os

def waitUntilSVG(file_path):
    #Function to wait for time_to_wait seconds until
    #a file exists in  file_path
    time_to_wait=10
    time_counter=0
    while not os.path.exists(file_path):
        time.sleep(1)
        time_counter += 1
        if(time_counter > time_to_wait):
            break
    print("done waiting")

class Ui_MainWindow(object):
    def convert2NFA(self):
        #Retreive entered regex from the text edit
        regex = self.textEdit.toPlainText()
        #validate(regex)
        
        #Start converting the regex to NFA
        nfa = transformAux(regex)

        #Visualize the converted NFA
        visualize(nfa)
        svg_file_path='out/nfa-graph.svg'
        #Wait until the visualized NFA-graph.svg is created
        waitUntilSVG(svg_file_path)

        #Render the visualized NFA-graph.svg on the layout
        self.get_size=QSvgRenderer(svg_file_path)
        self.SVGWidget=QSvgWidget(svg_file_path)
        self.SVGWidget.setFixedSize(self.get_size.defaultSize())
        self.scrollArea.setWidget(self.SVGWidget)
    
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(20, 30, 251, 61))
        
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(290, 30, 101, 31))
        self.pushButton.clicked.connect(self.convert2NFA)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 0, 171, 20))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 140, 121, 16))
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 160, 781, 391))
        self.svgContainer = QHBoxLayout(self.horizontalLayoutWidget)
        self.svgContainer.setObjectName(u"svgContainer")
        self.svgContainer.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.horizontalLayoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 777, 387))

        self.svgContainer.addWidget(self.scrollArea)
        self.SVGWidget = QSvgWidget()
        

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Convert to NFA", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Enter your Regex below", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"NFA/DFA outpt", None))
    # retranslateUi

