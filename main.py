
import re 
import sys 
import random
from regex2nfa import regex2nfa, transformAux, validate
from visualize_nfa import visualize, prepareForDrawing
from PySide6 import QtCore, QtWidgets, QtGui
from qtGUI3 import Ui_MainWindow


def convert(regex):
    
    validate(regex)
    nfa=transformAux(regex)   
    visualize(nfa)
          
        
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)


if __name__ == "__main__":

    #Run GUI
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
