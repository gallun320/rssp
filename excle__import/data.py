#! /usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import datetime
import psycopg2 as db



class ExcelAdd():
  def __init__(self,dict):
    
    self.sp_need = False
    
    self.dis_id = dict


    self.dictWYCIdByName = {
          u'Остальное поплнение': '888888',
          u'Водители колесных БТР-80': '124037',
          u'Водители категории Д': '845037',
          u'Водители категории "C"': '837037',
          u'Водители МТ-ЛБ': '843258',
          u'Стрелок-парашютист': '100915'
      }

    self.speaker = db.connect(host='127.0.0.1', user='postgres',password=1, dbname='rsSp')
  def get_book(self, book):
    self.rb = xlrd.open_workbook(book)
    namesBooks = self.rb.sheet_names()


    for book in namesBooks:
      sheet = self.rb.sheet_by_name(book)
      self.get_data(sheet)

  def get_data(self, sheet):
    name_sp_idx = 3
    content_idx_x = 6

    ser_arr = []

    if not sheet.nrows > 0:
      return 

    sp = sheet.row_values(name_sp_idx)

    self.wyc = self.dictWYCIdByName.get(sp[1])
    
    if self.wyc is None:
      self.sp_need = True

    for rownum in xrange(content_idx_x, sheet.nrows):
      row = sheet.row_values(rownum)[:17]

      if '' in row:
        break

      date_del = row[0]
      date_del = datetime.datetime(*xlrd.xldate_as_tuple(date_del, self.rb.datemode))

      a1 = row[1:5]
      a2 = row[5:9]
      b3 = row[9:13]
      b4 = row[13:17]
      
      sp = ""
      
      if self.sp_need:
        sp = row[17:18]
        self.wyc = self.get_unkonwn_sp(sp)
        
      
      ser_arr.append([date_del,a1,a2,b3,b4])
      
    self.inDB(ser_arr)

  def get_unkonwn_sp(self, sp):
    cur = self.speaker.cursor()
    
    cur.execute("select idx from spec_class where name ='%s'",[sp])
    
    res = cur.fetchall()[0][0]
    
    return res
    
  def inDB(self,arr):

    data = arr

    cur = self.speaker.cursor()

    for dt in data:
      cur.execute(
        '''with _a1 as 
      (insert into a1 (first_adm, second_adm,third_adm, without_adm) values (%s,%s,%s,%s) returning id), 
      _a2 as 
      (insert into a2 (first_adm, second_adm,third_adm, without_adm) values (%s,%s,%s,%s) returning id),
      _b3 as 
      (insert into b3 (first_adm, second_adm,third_adm, without_adm) values (%s,%s,%s,%s) returning id),
      _b4 as 
      (insert into b4 (first_adm, second_adm,third_adm, without_adm) values (%s,%s,%s,%s) returning id)
      insert into health (a1_id,a2_id, b3_id,b4_id) values 
      ((select id from _a1), (select id from _a2), (select id from _b3), (select id from _b4))
      returning id
      ''',
        [dt[1][0],dt[1][1],dt[1][2],dt[1][3],
         dt[2][0],dt[2][1],dt[2][2],dt[2][3],
         dt[3][0],dt[3][1],dt[3][2],dt[3][3],
         dt[4][0],dt[4][1],dt[4][2],dt[4][3]])

      health_id = cur.fetchall()[0][0]


      cur.execute('''
        insert into district (dis_id, health_id, type) values (%s,%s,%s) returning id
      ''', [self.dis_id,health_id, self.wyc])

      dis_id = cur.fetchall()[0][0]

      cur.execute('''
        insert into delivery (date_delivery, district_id) values (%s,%s)
      ''', [dt[0],dis_id])

      self.speaker.commit()
  
if __name__ == "__main__":
  
  exl = ExcelAdd()
  exl.get_book()