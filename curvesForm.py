# -*- coding: utf-8 -*-

from PyQt5 import uic
from PyQt5 import QtWidgets
import numpy as np
import json
from PyQt5.QtCore import QSettings, QPoint, QSize
from PyQt5.QtWidgets import QApplication

import pyqtgraph as pg

qt_creator_file = "xml/curvesform.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)
import debugPrinter as dp

class CurvesForm(QtWidgets.QWidget, Ui_MainWindow):
    """
    A class representing a curves form widget.

    Inherits from QtWidgets.QWidget and Ui_MainWindow.

    Attributes:
        pw (pg.PlotWidget): The plot widget for displaying curves.
        plt (pg.PlotItem): The plot item for customizing the plot.
        curves_num_constant (int): The number of constant curves.
        curves_eeg_num (int): The number of EEG curves.
        curves_acc_num (int): The number of accelerometer curves.
        checkboxes (list): A list of checkboxes for each curve.
        scale_offset (int): The scale offset for displaying curves.
        gridLayout (QtWidgets.QGridLayout): The grid layout for the widget.
        curve_data_max_len (int): The maximum length of curve data.
        curve_data_max_len_acc (int): The maximum length of accelerometer curve data.
        curves (list): A list of curve items.
        curves_acc (list): A list of accelerometer curve items.
        data (numpy.ndarray): An array for storing curve data.
        data_acc (numpy.ndarray): An array for storing accelerometer curve data.
        usr_config_json (dict): A dictionary for storing user configuration.
        show_ch (numpy.ndarray): An array for storing the visibility of curves.
        settings (QSettings): The settings object for saving window size and position.

    Methods:
        __init__(): Initializes the CurvesForm widget.
        __del__(): Destructor for the CurvesForm widget.
        closeEvent(e): Event handler for the close event.
        close_win(): Closes the CurvesForm widget.
        cb_handler(): Event handler for checkbox state changes.
        deal_with_data_inlet(elapsed_time, y): Handles incoming curve data.
        deal_with_data_acc_inlet(elapsed_time, y): Handles incoming accelerometer curve data.
    """

    def __init__(self):
        """
        Initializes the CurvesForm widget.

        Sets up the UI, initializes plot items, loads user configuration, and sets up event handlers.
        """
        QtWidgets.QWidget.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Signals")

        self.pw = pg.plot(title="sig")
        self.plt = self.pw.getPlotItem()

        self.curves_num_constant = 12
        curves_eeg_num = 8
        curves_acc_num = 4

        self.checkboxes = [None]*self.curves_num_constant
        self.checkboxes[0]=self.checkBox
        self.checkboxes[1]=self.checkBox_2
        self.checkboxes[2]=self.checkBox_3
        self.checkboxes[3]=self.checkBox_4
        self.checkboxes[4]=self.checkBox_5
        self.checkboxes[5]=self.checkBox_6
        self.checkboxes[6]=self.checkBox_7
        self.checkboxes[7]=self.checkBox_8
        self.checkboxes[8]=self.checkBox_9
        self.checkboxes[9]=self.checkBox_10
        self.checkboxes[10]=self.checkBox_11
        self.checkboxes[11]=self.checkBox_12

        self.scale_offset = 100

        self.gridLayout.addWidget(self.pw)
        self.pw.setLabel('bottom', 'Time', 's')

        self.curve_data_max_len = 1000
        self.curve_data_max_len_acc = 100

        self.curves=[]
        self.curves_acc=[]

        for i in range(self.curves_num_constant):
            c = self.pw.plot()
            self.curves.append(c) 

        self.data = np.empty(shape=(0,curves_eeg_num+1))
        self.data_acc = np.empty(shape=(0,curves_acc_num+1))

        with open('config/user_config_curve_form.json', 'r') as file:
            self.usr_config_json = json.load(file)

        self.show_ch = np.array(self.usr_config_json['CH'])

        curves_num = len(self.curves)+len(self.curves_acc) 

        if self.show_ch.size==self.curves_num_constant:
            for i, ch in enumerate(self.show_ch):
                if i<curves_num:
                    if ch==1:
                        self.checkboxes[i].setChecked(True)
                        self.curves[i].show()
                    else:
                        self.checkboxes[i].setChecked(False)
                        self.curves[i].hide()

        for i in range(self.curves_num_constant):
             self.checkboxes[i].stateChanged.connect(self.cb_handler)

        self.settings = QSettings('mi_app/curveFormSetting.ini', QSettings.IniFormat)     
        self.resize(self.settings.value("size", QSize(270, 225)))
        if (self.settings.value("pos") is not None) and (self.settings.value("size") is not None):
            screenRect = QApplication.desktop().screenGeometry()
            self.height = screenRect.height()
            if self.settings.value("pos").x()<(screenRect.width()-100) and \
                self.settings.value("pos").y()<(screenRect.height()-100):
                self.move(self.settings.value("pos", QPoint(50, 50)))            

    def __del__(self):
        """
        Destructor for the CurvesForm widget.

        Prints a debug message when the widget is deleted.
        """
        dp.dpt('del curvesform')

    def closeEvent(self, e):
        """
        Event handler for the close event.

        Writes window size and position to the config file.

        Args:
            e (QCloseEvent): The close event object.
        """
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        e.accept()
        
    def close_win(self):
        """
        Closes the CurvesForm widget.

        Writes window size and position to the config file before closing.
        """
        dp.dpt('curveform close')
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.close()

    def cb_handler(self):
        """
        Event handler for checkbox state changes.

        Updates the visibility of curves based on the checkbox states.
        Updates the user configuration and saves it to a JSON file.
        """
        for i in range(self.curves_num_constant):
            if (self.checkboxes[i].isChecked()):
                self.curves[i].show()
                self.show_ch[i]=1
            else:
                self.show_ch[i]=0
                self.curves[i].hide()

        self.usr_config_json['CH']=list(self.show_ch)

        with open('config/user_config_curve_form.json', "w") as outfile:
            json.dump(self.usr_config_json, outfile)    

    def deal_with_data_inlet(self, elapsed_time, y):
        """
        Handles incoming curve data.

        Appends the incoming data to the data array.
        Trims the data array if it exceeds the maximum length.
        Updates the curves with the new data.

        Args:
            elapsed_time (float): The elapsed time for the incoming data.
            y (numpy.ndarray): The incoming curve data.
        """
        if y.shape[1]==1: 
            y = np.hstack((y,np.zeros(shape=(y.shape[0],7))))

        t = np.expand_dims(elapsed_time, axis=1)

        d = np.hstack((t,y))

        self.data = np.concatenate((self.data,d), axis=0)

        num_del = self.data.shape[0] - self.curve_data_max_len

        if(num_del>0):
            self.data = np.delete(self.data,np.s_[:num_del], axis=0)

        for i in range(self.data.shape[1]-1):
            if self.show_ch[i]:
                voltage_value = (self.data[:, i+1]-32768)*0.2
                self.curves[i].setData(x=self.data[:,0],y=voltage_value+self.scale_offset*i)

    def deal_with_data_acc_inlet(self, elapsed_time, y):
        """
        Handles incoming accelerometer curve data.

        Appends the incoming data to the accelerometer data array.
        Trims the accelerometer data array if it exceeds the maximum length.
        Updates the accelerometer curves with the new data.

        Args:
            elapsed_time (float): The elapsed time for the incoming data.
            y (numpy.ndarray): The incoming accelerometer curve data.
        """
        t = np.expand_dims(elapsed_time, axis=1)

        d = np.hstack((t,y))

        self.data_acc = np.concatenate((self.data_acc,d), axis=0)

        num_del = self.data_acc.shape[0] - self.curve_data_max_len_acc

        if(num_del>0):
            self.data_acc = np.delete(self.data_acc,np.s_[:num_del], axis=0)

        for i in range(self.data_acc.shape[1]-1):
            index_for_acc_curves = i+8
            if self.show_ch[index_for_acc_curves]:
                self.curves[index_for_acc_curves].setData(x=self.data_acc[:,0],y=self.data_acc[:, i+1])


