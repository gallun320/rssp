#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import io
import codecs
from itertools import izip

reload(sys)
sys.setdefaultencoding("utf-8")

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from rs import *



class MyPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.rs_grid = QGridLayout()
        self.table = QTableWidget()
        
       
    def paintEvent(self, e):
        self.setLayout(self.rs_grid)
        self.rs_grid.addWidget(self.table, 0,0)
    def tableView(self, id, arr):
      
      #print id
      #print arr[id]['dis']
      if len(arr) > 0:
        self.table.setRowCount(len(arr[id]['dis']))
        self.table.setColumnCount(len(arr[id]['dis'][0]))
        
        self.table.setHorizontalHeaderLabels(QString(u"Название района;Распределено").split(";"))
        for idx, i in  enumerate(arr[id]['dis']):
          self.table.setItem(idx,0, QTableWidgetItem(i['name']))
          self.table.setItem(idx,1, QTableWidgetItem(str(i['count'])))
        self.table.setColumnWidth(0, 350)
        

class RsWindow(QMainWindow):
  def __init__(self):
    super(QMainWindow, self).__init__()
    self.sp = "all"
    self.dictWYCNameById = {
          'all': u'Все',
          '124037': u'Водитель БТР',
          '845037': u'Водитель категории Д',
          '837037': u'Водитель категории "C"',
          '837038': u'Водитель категории "B,C"',
          '837040': u'Водитель категории "B,C"',
          '843258': u'Механик водитель МТЛБ'
        }
        
    self.dictWYCIdByName = {
          u'Все': 'all',
          u'Водитель БТР': '124037',
          u'Водитель категории Д': '845037',
          u'Водитель категории "C"': '837037',
          u'Водитель категории "B,C"': '837038',
          u'Водитель категории "B,C"': '837040',
          u'Механик водитель МТЛБ': '843258'
      }
    self.sort_data = {
      'all': {
        'r': [],
        'ch': []
      }
    }
    self.dbC = DB()
    self.chData = self.dbC.getChData()
    self.rData = self.dbC.getRData()
    self.sort_data['all']['r'] = self.rData
    self.sort_data['all']['ch'] = self.chData
    self.sort_sp = self.dbC.getSpData()
    self.sort_sp = [('all',)] + self.sort_sp
    self.rs_alg = Rs()
    
    self.setWindowTitle("RsWindow")
    self.resize(1440, 1050)
    self.create_rs_view()
    
    
    self.setCentralWidget(self.rs_widget)
    self.connect(QShortcut(QKeySequence(Qt.Key_Escape), self), SIGNAL('activated()'),self.close)
  
  def create_rs_view(self):
    self.sort_box_layout = QVBoxLayout()
    self.button_box_layout = QVBoxLayout()
    self.label_rs_pshf = QLabel(u'Задание')
    self.label_rs = QLabel(u'Ресурсы')
    self.sp_combox = QComboBox()
    #self.sp_combox.addItem(self.dictWYCNameById['all'])
    for sp_s in self.sort_sp:
      
      self.sp_combox.addItem(self.dictWYCNameById[sp_s[0]])
  
    self.rs_pshf_button = QPushButton(u"1. распределение подшефных команд", self)
    self.rs_button = QPushButton(u"2. распределение остальных команд", self)
    self.rs_button.setEnabled(False)
    self.rs_grid = QGridLayout()
    self.rs_grid.addWidget(self.label_rs_pshf,0,0)
    self.rs_grid.addWidget(self.label_rs,0,1)
    
    #self.rs_grid.addWidget(self.sp_combox,0,4)
    
    #self.rs_grid.addWidget(self.rs_pshf_button,2,0)
    #self.rs_grid.addWidget(self.rs_button,2,1)
    
    self.rs_widget = QWidget()
    self.rs_widget.setLayout(self.rs_grid)
    
    self.table = QTableWidget()
    self.table_r = QTableWidget()
    self.table_item = QTableWidgetItem()
    self.table_item_r = QTableWidgetItem()
    
    self.res_label = QLabel()
    
    self.button_box_layout.addWidget(self.rs_pshf_button)
    self.button_box_layout.addWidget(self.rs_button)
    
    #self.sort_box_layout.addWidget(QLabel(u"Сортировка:"))
    self.sort_box_layout.addWidget(self.sp_combox)
    self.sort_box_layout.addWidget(self.res_label)
    
    self.rs_grid.addLayout(self.sort_box_layout, 2,1)
    self.rs_grid.addLayout(self.button_box_layout, 2,0)
    
    self.rs_grid.addWidget(self.table, 1,0)
    self.rs_grid.addWidget(self.table_r, 1,1)
    self.rs_pshf_table_view()
    self.r_table_view()
    #self.rs_pshf_button.clicked.connect(self.rs_pshf_table_view)
    self.rs_pshf_button.clicked.connect(self.button_click)
    self.rs_button.clicked.connect(self.button_click)
    
    self.sp_combox.activated.connect(self.sort_list_click)
    
    self.raspr()
    
  def sort_list_click(self, strD):
    arrCh = self.sort_data['all']['ch']
    arrR = self.sort_data['all']['r']
    arrR,arrCh = self.checkedArr(arrR, arrCh)
    if self.sort_sp[strD][0] != 'all':
      self.chData = [ el for el in arrCh if self.sort_sp[strD][0] == el['name_sp']]
      self.rData = [el for el in arrR if el.get(self.sort_sp[strD][0]) != None]
    else:
      self.chData = arrCh
      self.rData = arrR
    #for dt in arrR:
     # d = ((x,) for x in enumerate(dt['data'])
    self.sp = self.sort_sp[strD][0]
    self.raspr(self.sort_sp[strD][0])
    self.r_table_view()
    self.rs_pshf_table_view()
    print strD, self.sort_sp[strD][0]
  
  def checkedArr(self, arrR, arrCh):
    print 'checkedArr'
    for r,self_r in izip(arrR, self.rData):
      print r['id'], self_r['id']
      if r['id'] == self_r['id']:
        
        if r['count'] != self_r['count']:
          print r['id'],r['count'],self_r['count']
          r = self_r
    
    for ch, self_ch in izip(arrCh,self.chData):
      if ch['id'] == self_ch['id']:
        if ch['count'] != self_ch['count']:
          ch = self_ch
    return arrR, arrCh
  
  def button_click(self):
    if self.sender() is self.rs_pshf_button:
      self.rs_button.setEnabled(True)
      self.rs_pshf_button.setEnabled(False)
      QMessageBox.about(self, u"Распределение",u"Распределение подшефных команд начато")
      self.rs_alg.chRs(self.sort_data['all']['ch'], self.sort_data['all']['r'])
      QMessageBox.about(self, u"Распределение",u"Распределение подшефных команд завершено")
    else:
      self.rs_button.setEnabled(False)
      QMessageBox.about(self, u"Распределение",u"Распределение остальных команд начато")
      self.rs_alg.chRs(self.sort_data['all']['ch'], self.sort_data['all']['r'])
      QMessageBox.about(self, u"Распределение",u"Распределение остальных команд завершено")
    self.rs_pshf_table_view()
    self.raspr(self.sp)
    
  def rs_pshf_table_view(self):
    
    self.table.setRowCount(len(self.chData))
    self.table.setColumnCount(6)
    
    self.table.cellClicked.connect(self.cellClick)
    
    header = self.table.horizontalHeader()
    header.setResizeMode(0, QHeaderView.ResizeToContents)
    header.setResizeMode(1, QHeaderView.ResizeToContents)
    header.setResizeMode(2, QHeaderView.ResizeToContents)
    
    self.table.setHorizontalHeaderLabels(QString(u"Станция назначения;Команда;Дата отправки;Задание;Распределено;Специальность").split(";"))
    for ix, i in enumerate(self.chData):
        strBName = unicode(i['name'], 'cp1251')
        strBNTeam = unicode(i['nteam'], 'cp1251')
        dateOtp = str(i['date']).split('-')
        day = dateOtp[2][:2]
        dateOtp[2] = day
        
        self.table.setItem(ix,0, QTableWidgetItem(strBName))
        self.table.setItem(ix,1, QTableWidgetItem(strBNTeam))
        self.table.setItem(ix,2, QTableWidgetItem(dateOtp[2] + '.' + dateOtp[1] + '.' + dateOtp[0]))
        self.table.setItem(ix,3, QTableWidgetItem(str(i['need'])))
        self.table.setItem(ix,4, QTableWidgetItem(str(i['count'])))
        self.table.setItem(ix,5, QTableWidgetItem(self.dictWYCNameById.get(i['name_sp'])))
        if i['sh'] == True:
          self.table.item(ix,0).setBackground(QColor(243,218,11))
          self.table.item(ix,1).setBackground(QColor(243,218,11))
          self.table.item(ix,2).setBackground(QColor(243,218,11))
          self.table.item(ix,3).setBackground(QColor(243,218,11))
          self.table.item(ix,4).setBackground(QColor(243,218,11))
          self.table.item(ix,5).setBackground(QColor(243,218,11))
          
          
    self.r_table_view()
        
  def cellClick(self, row, cell):
    self.popup = MyPopup()
    self.popup.setGeometry(QRect(100, 100, 800, 300))
    self.popup.tableView(row, self.chData)
    self.popup.show()
      
  def raspr(self, sort_type = "count"):
    sort_type = sort_type if sort_type != 'all' else 'count' 
    sum_ch_need = sum(item['need'] for item in self.chData)
    sum_r = sum(item[sort_type] for item in self.rData)
    sum_ch_count = sum(item['count'] for item in self.chData)
    self.res_label.setText(u'Задание: %d, Ресурсы: %d, Распределено: %d' % (sum_ch_need,sum_r, sum_ch_count))
    #print sum_r, sum_ch
  def r_table_view(self):
    self.table_r.setRowCount(len(self.rData))
    self.table_r.setColumnCount(7)
    self.table_r.setHorizontalHeaderLabels(QString(u"Район;Ресурс;БТР;Категории 'C';Категории 'Д';МТЛБ;Остаток").split(";"))
    for idx, i in enumerate(self.rData):
      self.table_r.setItem(idx,0, QTableWidgetItem(str(i['name'])))
      self.table_r.setItem(idx,1, QTableWidgetItem(str(i['all'])))
      self.table_r.setItem(idx,2, QTableWidgetItem(str(i.get('124037',''))))
      self.table_r.setItem(idx,3, QTableWidgetItem(str(i.get('837037',''))))
      self.table_r.setItem(idx,4, QTableWidgetItem(str(i.get('845037',''))))
      self.table_r.setItem(idx,5, QTableWidgetItem(str(i.get('843258',''))))
      self.table_r.setItem(idx,6, QTableWidgetItem(str(i['count'])))
      
def main():
  simulator = QApplication(sys.argv)
  rs_window = RsWindow()
  
  rs_window.show()
  rs_window.raise_()
  simulator.exec_()
  
  
if __name__ == "__main__":
  main()