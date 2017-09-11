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

import data.team_db as team
import data.district_db as district
import workers.pshf_worker as pshf
import workers.builder_worker as builder
import workers.hand_worker as hand
import utils.api as api


import json

class MyPopup(QWidget):
    def __init__(self, districts={}, teams=[]):
        QWidget.__init__(self)
        self.rs_grid = QGridLayout()
        self.table = QTableWidget()
        self.districts = dict(districts)
        self.teams = list(teams)
        self.mtx = hand.HandWorker(self.teams, self.districts)
        
    def paintEvent(self, e):
        
        
        self.setLayout(self.rs_grid)
        
        self.rs_grid.addWidget(self.table, 0,0)
    def tableView(self,arrD={}, arrT=[]):
      self.table.itemDoubleClicked.connect(self.cellClick)
      
      
      
      mtx_dt = self.mtx.get_mtx()

      arrT = [str(unicode(i.get('st'), 'cp1251')) + '   ' + str(i.get('count')) + '/' + str(i.get('need')) for i in arrT]
      arrD = [str(unicode(str(i[1].get('name')), 'utf8')) + '     ' + str(i[1].get('count')) + '/' + str(i[1].get('all')) for i in arrD.items()]

      self.table.setRowCount(len(arrT))
      self.table.setColumnCount(len(arrD))
      
      self.table.setHorizontalHeaderLabels(arrD)
      
      self.table.setVerticalHeaderLabels(arrT)
      
      header = self.table.horizontalHeader()
      
      '''for si, dt in enumerate(arrD):
        header.setResizeMode(si, QHeaderView.ResizeToContents)'''
      
      for i, row in enumerate(arrT):
        for j, col in enumerate(arrD):
          self.table.setItem(i, j, QTableWidgetItem(str(mtx_dt[i][j][3])))

    def tableTeamView(self, id, arr):
      if len(arr) > 0:
        dis = arr[id].get('dis_dt',{}).items()
        self.table.setRowCount(len(dis))
        self.table.setColumnCount(2)
        
        self.table.setHorizontalHeaderLabels(QString(u"Название района;Распределено").split(";"))
        for idx, i in  enumerate(dis):
          name = self.districts.get(i[0]).get('name')
          self.table.setItem(idx,0, QTableWidgetItem(name))
          self.table.setItem(idx,1, QTableWidgetItem(str(i[1])))
        self.table.setColumnWidth(0, 350)
        
    def cellClick(self, *args):
      self.table.itemChanged.connect(self.cellChange)
          
    def cellChange(self, item):  
      try:
        row = int(item.row())
        column = int(item.column())
        count = int(item.text())
      except ValueError:
        print 'Error type'
      
      self.mtx.set_mtx_item(row, column, count)
      self.teams[row]['count'] = count
      idx = self.districts.items()[column][0]
      
      self.districts[idx]['count'] = count
      self.teams[row]['dis_dt'][idx] = count

      self.rerendHeader(row, column)
      
    def rerendHeader(self, row, column):
      t = self.teams[row]
      idx = self.districts.items()[column][0]
      
      d = self.districts[idx]
      
      tText = str(unicode(t.get('st'), 'cp1251')) + '   ' + str(t.get('count')) + '/' + str(t.get('need'))
      dText = str(unicode(str(d.get('name')), 'utf8')) + '     ' + str(d.get('count')) + '/' + str(d.get('all'))
      self.table.setHorizontalHeaderItem(column, QTableWidgetItem(dText))
      self.table.setVerticalHeaderItem(row, QTableWidgetItem(tText))
      
      


class RsWindow(QMainWindow):
  def __init__(self):
    super(QMainWindow, self).__init__()
    self.api = api.Api()
    

    with open('config/health.json') as dt:
      self.hlt_conf = json.load(dt)

    with open('config/adm.json') as dt:
      self.adm_conf = json.load(dt)

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

    self.setWindowTitle("RsWindow")
    self.resize(1440, 1050)
    self.team = team.TeamDB()

    self.district = district.DisDB()
    self.pshf = pshf.PshfWorker()
    self.sort_sp = self.team.getSpData()
    self.sort_sp = [('all',)] + self.sort_sp
    
    
    self.teams = self.team.get_team_data()

    self.districts = self.district.get_district()
    self.builder = builder.Builder()
    
    self.sort_data['all']['ch'] = list(self.teams)
    self.sort_data['all']['r'] = dict(self.districts)
    
    self.popup = MyPopup(self.districts, self.teams)
    
    self.create_rs_view()

    self.setCentralWidget(self.rs_widget)
    self.connect(QShortcut(QKeySequence(Qt.Key_Escape), self),
                 SIGNAL('activated()'), self.close)

  def create_rs_view(self):
    self.rs_psh_button = QPushButton(
        u"1. Распределение подшефных команд", self)
    self.rs_button = QPushButton(
        u"2. Распределение команд остальных команд", self)
    self.rs_h_button = QPushButton(
        u"3. Ручное распределение команд", self)
    
    '''self.rs_button.setEnabled(False)
    self.rs_psh_button.setEnabled(True)
    self.rs_h_button.setEnabled(False)'''
    
    self.table_box_layout = QVBoxLayout()
    self.table_box_d_layout = QVBoxLayout()

    self.rs_grid = QGridLayout()

    self.rs_widget = QWidget()
    self.rs_widget.setLayout(self.rs_grid)
    
    self.res_label = QLabel()
    
    self.sp_combox = QComboBox()
    
    for sp_s in self.sort_sp:
      
      self.sp_combox.addItem(self.dictWYCNameById[sp_s[0]])
    
    self.table = QTableWidget()
    self.table_d = QTableWidget()
    self.table_item = QTableWidgetItem()
    self.table_d_item = QTableWidgetItem()

    self.table_box_layout.addWidget(self.table)
    self.table_box_d_layout.addWidget(self.table_d)

    self.table_box_layout.addWidget(self.rs_psh_button)
    self.table_box_layout.addWidget(self.rs_button)
    self.table_box_layout.addWidget(self.rs_h_button)
    self.table_box_d_layout.addWidget(self.sp_combox)
    self.table_box_d_layout.addWidget(self.res_label)

    self.rs_grid.addLayout(self.table_box_layout, 0, 0)
    self.rs_grid.addLayout(self.table_box_d_layout, 0, 1)
    
    self.table_district_view()
    self.table_team_view()
    
    self.rs_button.clicked.connect(self.button_click)
    self.rs_psh_button.clicked.connect(self.button_click)
    self.rs_h_button.clicked.connect(self.button_click)
    
    self.sp_combox.activated.connect(self.sort_list_click)
    
    self.raspr()
    
  def table_district_view(self):
    self.table_d.setRowCount(len(self.districts))
    self.table_d.setColumnCount(4)

    # self.table.cellClicked.connect(self.cellClick)

    header = self.table_d.horizontalHeader()
    header.setResizeMode(0, QHeaderView.ResizeToContents)
    header.setResizeMode(1, QHeaderView.ResizeToContents)
    header.setResizeMode(2, QHeaderView.ResizeToContents)
    header.setResizeMode(3, QHeaderView.ResizeToContents)
    self.table_d.setHorizontalHeaderLabels(
        QString(u"Район;Ресурс;Остаток; ;").split(";"))
    for jx, j in enumerate(self.districts.items()):
      self.about_d = QPushButton(u'Показать ресурс')
      self.table_d.setItem(jx, 0, QTableWidgetItem(j[1].get('name')))
      self.table_d.setItem(jx, 1, QTableWidgetItem(str(j[1].get('all'))))
      self.table_d.setItem(jx, 2, QTableWidgetItem(str(j[1].get('count'))))
      self.table_d.setCellWidget(jx,3,self.about_d)
                           
  def table_team_view(self):
    t = [] if self.teams == None else self.teams
    self.table.setRowCount(len(t))
    self.table.setColumnCount(6)

    self.table.cellClicked.connect(self.cellClick)

    header = self.table.horizontalHeader()
    header.setResizeMode(0, QHeaderView.ResizeToContents)
    header.setResizeMode(1, QHeaderView.ResizeToContents)
    header.setResizeMode(2, QHeaderView.ResizeToContents)
    header.setResizeMode(5, QHeaderView.ResizeToContents)

    self.table.setHorizontalHeaderLabels(QString(
        u"Станция назначения;Команда;Дата отправки;Задание;Распределено;Специальность").split(";"))
    for ix, i in enumerate(t):
        strBName = unicode(i.get('st'), 'cp1251')
        strBNTeam = unicode(i.get('n_team'), 'cp1251')
        dateOtp = i.get('tm').strftime("%d-%m-%Y")

        desc = self.read_desc(i.get('need_desc').get('str_code'))

        i['need_desc']['str_desc'] = desc

        self.table.setItem(ix, 0, QTableWidgetItem(strBName))
        self.table.setItem(ix, 1, QTableWidgetItem(strBNTeam))
        self.table.setItem(ix, 2, QTableWidgetItem(dateOtp))
        self.table.setItem(ix, 3, QTableWidgetItem(str(i.get('need'))))
        self.table.setItem(ix, 4, QTableWidgetItem(str(i.get('count'))))
        self.table.setItem(ix, 5, QTableWidgetItem(desc))
        if len(i.get('pod')) > 0:
          self.table.item(ix,0).setBackground(QColor(243,218,11))
          self.table.item(ix,1).setBackground(QColor(243,218,11))
          self.table.item(ix,2).setBackground(QColor(243,218,11))
          self.table.item(ix,3).setBackground(QColor(243,218,11))
          self.table.item(ix,4).setBackground(QColor(243,218,11))
          self.table.item(ix,5).setBackground(QColor(243,218,11))
          
  def button_click(self):
    if self.sender() is self.rs_psh_button:
      self.rs_button.setEnabled(True)
      self.rs_psh_button.setEnabled(False)
      self.rs_h_button.setEnabled(False)
      
      QMessageBox.about(self, u"Распределение",u"Распределение подшефных команд начато")
      self.pshf_r()
      QMessageBox.about(self, u"Распределение",u"Распределение подшефных команд завершено")
    elif self.sender() is self.rs_button:
      self.rs_button.setEnabled(False)
      self.rs_h_button.setEnabled(True)
      QMessageBox.about(self, u"Распределение",u"Распределение остальных команд начато")
      self.bld_g()
      QMessageBox.about(self, u"Распределение",u"Распределение остальных команд завершено")
    else:
      self.h_grid()
      
    self.table_district_view()
    self.table_team_view()
    self.raspr()
        
  def cellClick(self, row, cell):
    self.popup.setGeometry(QRect(100, 100, 800, 300))
    self.popup.tableTeamView(row, self.teams)
    self.popup.show()

  def read_desc(self, desc):
    sp_str=""
    adm_str=""
    hlt_str=""

    if desc[0] == "-" and desc[1] == "-":
      sp_str="Остальное пополнение"
    elif not desc[0] is "-":
      sp_str=self.api.get_sp(desc[0])
    else:
      sp_str=self.api.get_sp(desc[1])

    hlt_str=self.hlt_conf.get(desc[3] + str(desc[4]))

    adm_str=self.adm_conf.get(desc[2])

    return u"%s, %s, допуск: %s" % (sp_str, hlt_str, adm_str)

  def bld_g(self):
    self.teams,self.districts = self.builder.r_q(self.teams, self.districts)
    
    
  def pshf_r(self):
    self.teams,self.districts = self.pshf.set_pshf(self.teams,self.districts)
    
  def h_grid(self):
    self.popup = MyPopup(self.districts, self.teams)
    self.popup.setGeometry(QRect(100, 100, 800, 300))
    self.popup.tableView(self.districts, self.teams)
    self.popup.show()
    
  def sort_list_click(self, strD):
    arrCh = list(self.sort_data['all']['ch'])
    arrR = dict(self.sort_data['all']['r'])
    arrR,arrCh = self.checkedArr(arrR, arrCh)
    if self.sort_sp[strD][0] != 'all':
      self.teams = [ el for el in arrCh if self.sort_sp[strD][0] == el['need_desc']['mil_spec']]
      for k,v in arrR.items():
        sp = v.get('sp').items()
        for ks, vs in sp:
          if ks == self.sort_sp[strD][0]:
            self.districts.setdefault(k,{})
            
            self.districts[k] = v
    else:
      self.teams = arrCh
      self.districts = arrR
    #for dt in arrR:
     # d = ((x,) for x in enumerate(dt['data'])
    self.sp = self.sort_sp[strD][0]
    self.raspr()
    self.table_district_view()
    self.table_team_view()
  
  def checkedArr(self, arrR, arrCh):
    for r,self_r in izip(arrR.items(), self.districts.items()):
      print r[0], self_r[0]
      if r[0] == self_r[0]:
        
        if r[1]['count'] != self_r[1]['count']:
          print r['id'],r['count'],self_r['count']
          r = self_r
    
    for ch, self_ch in izip(arrCh,self.teams):
      if ch['n_team'] == self_ch['n_team']:
        if ch['count'] != self_ch['count']:
          ch = self_ch
    return arrR, arrCh
  
  def raspr(self):
    sum_ch_need = sum(item['need'] for item in self.teams)
    sum_r = sum(item['count'] for k,item in self.districts.items())
    sum_ch_count = sum(item['count'] for item in self.teams)
    self.res_label.setText(u'Задание: %d, Ресурсы: %d, Распределено: %d' % (sum_ch_need,sum_r, sum_ch_count))

def main():
  simulator=QApplication(sys.argv)
  rs_window=RsWindow()

  rs_window.show()
  rs_window.raise_()
  simulator.exec_()


if __name__ == "__main__":
  main()
