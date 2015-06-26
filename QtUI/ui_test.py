# -*- coding: utf-8 -*-
"""

Code for testing the Qt GUI.

Created on Fri Jun 26 13:59:52 2015

@author: Hans-Christiaan
"""

import sys
from PyQt4 import QtCore, QtGui, uic

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("BanditsGUI.ui", self)
        
        self.connect(self.button_start, QtCore.SIGNAL("clicked()"), self.button_test)        
        
        self.show()
    
    def button_test(self):
        print "button clicked!"

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())