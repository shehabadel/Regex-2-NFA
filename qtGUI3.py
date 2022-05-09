# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qtGUI2.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QStatusBar, QTextBrowser, QTextEdit,
    QWidget, QMessageBox)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtSvg import *
from regex2nfa import regex2nfa, transformAux, validate,createFormalDescription
from visualize_nfa import visualize, prepareForDrawing
import time
import os   
import json

def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)

    return obj
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
    def validateRegex(self, regex, flag):
        try:
            validate(regex)
            flag=True
        except Exception as e:
            print(str(e))
            self.show_pop(str(e))
            flag=False
        return flag
    def outputFormalDescription(self):
        formalDescription = createFormalDescription()
        formalDescriptionJSON=json.dumps(formalDescription, indent=4, sort_keys=True, default=serialize_sets, ensure_ascii=False)
        self.textBrowser.setText(formalDescriptionJSON)

    
    def convert2NFA(self):
        #Retreive entered regex from the text edit
        regex = self.textEdit.toPlainText()
        flag=True
        flag=self.validateRegex(regex,flag)
        print(flag)
        if flag:
            try:
            #Start converting the regex to NFA
                nfa = transformAux(regex)
            #Visualize the converted NFA
                visualize(nfa)
                svg_file_path='out/nfa-graph.svg'
            #Wait until the visualized NFA-graph.svg is created
                self.outputFormalDescription()
                waitUntilSVG(svg_file_path)
            #Render the visualized NFA-graph.svg on the layout
                self.get_size=QSvgRenderer(svg_file_path)
                self.SVGWidget=QSvgWidget(svg_file_path)
                self.SVGWidget.setFixedSize(self.get_size.defaultSize())
                self.scrollArea.setWidget(self.SVGWidget)
            except Exception as e:
                self.show_pop(str(e))

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1047, 743)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.clicked.connect(self.convert2NFA)

        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)

        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout.addWidget(self.textBrowser, 2, 0, 1, 1)

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")

        self.gridLayout.addWidget(self.textEdit, 2, 1, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.svgContainer = QHBoxLayout()
        self.svgContainer.setObjectName(u"svgContainer")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1025, 325))
        self.horizontalLayout_2 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.svgContainer.addWidget(self.scrollArea)


        self.gridLayout_2.addLayout(self.svgContainer, 2, 0, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1047, 21))
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
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Enter your Regex below", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Formal Description Output", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"NFA/DFA output", None))
    # retranslateUi
    def show_pop(self, errorMsg):
        msg=QMessageBox()
        msg.setWindowTitle("Exception thrown")
        msg.setText(errorMsg)

        x = msg.exec_()
