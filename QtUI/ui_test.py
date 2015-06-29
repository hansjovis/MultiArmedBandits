# -*- coding: utf-8 -*-
"""

Code for testing the Qt GUI.

Created on Fri Jun 26 13:59:52 2015

@author: Hans-Christiaan
"""

import sys
import time
from PyQt4 import QtCore, QtGui, uic
from PyQt4 import Qwt5 as Qwt


class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("BanditsGUI.ui", self)
        
        self.running = False
        
        # rewards on the y-axis, iterations on the x-axis
        self.rewards = []
        self.iterations = []
        
        # connect the start button, stop button and spin widget to their appropriate methods.
        self.connect(self.button_start, QtCore.SIGNAL("clicked()"), self.start_run)        
        self.connect(self.spinBox_run_id, QtCore.SIGNAL("valueChanged(int)"), self.change_run_id)
        self.connect(self.button_stop, QtCore.SIGNAL("clicked()"), self.stop_run)
        self.connect(self.save_button, QtCore.SIGNAL("clicked()"), self.save_plot)        
        
        # set some properties of the graph
        self.plot_reward_over_time.setTitle("Total reward over time")        
        self.plot_reward_over_time.setCanvasBackground(QtCore.Qt.white)
        
        # make the (empty) curve and attach it to the graph
        self.plot_curve = Qwt.QwtPlotCurve("Total reward")
        self.plot_curve.attach(self.plot_reward_over_time)
        
        # show the GUI
        self.show()
    
    def change_run_id(self,new_id):
        self.run_id = new_id        
    
    def start_run(self):
        self.plot_reward_over_time.setTitle("Total reward over time (run id "+str(self.run_id)+")")
        self.running = True

    def stop_run(self):
        self.running = False       
    
    def add_new_observed_reward(self, iteration_n, new_reward):
        self.rewards = self.rewards + [new_reward]
        self.iterations = self.iterations + [iteration_n]
        
        #print self.rewards, self.iterations        
        
        self.plot_curve.setData(self.iterations, self.rewards)
        self.plot_reward_over_time.replot()
    
    """ 
        Saves the current plot as an image.
    """
    def save_plot(self):
        # Stop running
        self.running = False        
        default_path = " "
        # Open save dialog and get the save-path.
        save_path = QtGui.QFileDialog.getSaveFileName(self, 'Save', default_path, filter="*.png")
        # Save image.        
        QtGui.QPixmap.grabWidget(self.plot_reward_over_time).save(save_path)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()    
    
    # Only for testing real-time plotting.
    i = 0
    # TODO: "Clean" exit.
    while True:
        # Wait until all pending events have been processed
        # to avoid freezing the GUI.
        QtGui.QApplication.processEvents()
        while window.running:
            window.add_new_observed_reward(i,i*i)
            i += 1
            # Only for testing real-time plotting. 
            time.sleep(0.1)
            QtGui.QApplication.processEvents()                    

    sys.exit(app.exec_())
    
