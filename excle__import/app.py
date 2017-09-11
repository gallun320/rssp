#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import io
import codecs
from itertools import izip
from api import *
from data import *

reload(sys)
sys.setdefaultencoding("utf-8")

from PyQt4.QtCore import *
from PyQt4.QtGui import *






class RsWindow(QMainWindow):
  def __init__(self):
    super(QMainWindow, self).__init__()
    self.api = Api()
    self.lst_dict = self.api.get_district()
    
    self.excelDt = ExcelAdd(self.lst_dict[0][0])
    
    self.setWindowTitle("RsWindow")
    self.resize(400, 240)
    self.create_import_view()
    
  
    self.setCentralWidget(self.xl_widget)
  
  def create_import_view(self):
    
    
    
    self.dis_combox = QComboBox()
    
    for dic in self.lst_dict:
      
      self.dis_combox.addItem(dic[1])
    
    self.choose_file_button = QPushButton(u"Выбрать файл",self)
    self.create_import_button = QPushButton(u"Загрузить в БД", self)
    self.create_import_button.setEnabled(False)
    
    self.import_box_layout = QVBoxLayout()
    #self.button_box_layout = QVBoxLayout()
    self.import_box_layout.addStretch(1)
    self.import_view_grid = QGridLayout()
    
    self.import_box_layout.addWidget(self.choose_file_button)
    self.import_box_layout.addWidget(self.create_import_button)
    self.import_box_layout.addWidget(self.dis_combox)
    
    self.import_view_grid.addLayout(self.import_box_layout,0,0)
    
    self.xl_widget = QWidget()
    
    self.choose_file_button.clicked.connect(self.selectFile)
    self.create_import_button.clicked.connect(self.createImport)
    
    self.dis_combox.activated.connect(self.dis_lst_click)
    
    self.xl_widget.setLayout(self.import_view_grid)
  
  def dis_lst_click(self,strD):

    dict_dt = self.lst_dict[strD][0]
    self.excelDt = ExcelAdd(dict_dt)
  
  def selectFile(self):
    self.filename = QFileDialog.getOpenFileName(self, 'Open file', '~')
    self.create_import_button.setEnabled(True)
    
  def createImport(self):
    QMessageBox.about(self, u"Импорт",u"Производится импорт в БД")
    self.excelDt.get_book(str(self.filename))
    QMessageBox.about(self, u"Импорт",u"Импорт в БД завершен")
    
def main():
  simulator = QApplication(sys.argv)
  rs_window = RsWindow()
  
  rs_window.show()
  rs_window.raise_()
  simulator.exec_()
  
  
if __name__ == "__main__":
  main()
    