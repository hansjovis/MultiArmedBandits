# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 19:43:14 2015

@author: Hans-Christiaan
"""

import sys
from PyQt4 import QtGui

from QtUI import ui_test
import serverCommunication
from algorithm import Algorithm
from config import config

stopped = False
algorithm = Algorithm()

def main():
    app = QtGui.QApplication(sys.argv)
    window = ui_test.MainWindow()
    
    # Main loop
    # TODO: "Clean" exiting.    
    while not stopped:
        i = 0
        # Wait until all pending events have been processed
        # to avoid freezing the GUI.
        QtGui.QApplication.processEvents()
        while window.running and i in range(0,50000):
            context = serverCommunication.getContext(window.run_id, i)
            ad_data = algorithm.make_selection(context)
            datalist = (ad_data['header'], ad_data['adtype'], ad_data['color'],
						ad_data['productid'], ad_data['price'])
            result  = serverCommunication.proposePage(window.run_id, i, *datalist)
            algorithm.learn(context, ad_data, result)
            
            # calculate the reward for this advertisement
            reward = result * float(ad_data['price'])
            i = i+1
            # add the reward to the plot
            if reward is not None:
                window.add_new_observed_reward(i, reward)
                
            QtGui.QApplication.processEvents()
            
    sys.exit(app.exec_())
         