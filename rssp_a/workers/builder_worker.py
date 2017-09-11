#! /usr/bin/env python
# -*- coding: utf-8 -*-


import utils.api as api
import utils.builder_utils as b_ut
import data.builder_db as db

from math import floor, ceil
import json
import bisect
import os
import pprint


class Builder():
  def __init__(self):
    with open(os.path.abspath("config/sp_w.json")) as dt:
      self.dictWYC = json.load(dt)

    with open(os.path.abspath("config/adm_w.json")) as dt:
      self.dictAdm = json.load(dt)
    
    with open(os.path.abspath("config/health_w.json")) as dt:
      self.dictHlt = json.load(dt)

    self.api = api.Api()
    self.b_utils = b_ut.BuilderUtils()

    self.db = db.BuilderDB()
    
    self.desc = {}
    
  def r_q(self, teams, districts):
    
    arrT = list(teams)
    arrLIdx = list(teams)

    district = dict(districts)
    
    while True:
      max_el = self.b_utils.get_res(arrLIdx)

      desc = arrT[max_el].get('need_desc')
      
      adm, hlt, sp = self.b_utils.get_param_q(desc)
     
      lst_idx = self.b_utils.filterd_lst_teams(arrT, desc.get('str_desc'))
    
      for idx in lst_idx:
        arrLIdx[idx] = None
      
      res = self.db.bld_q(adm, hlt, sp)
      
      arrT,district = self.res_q(res,arrT, lst_idx, district, desc)
      
      arrR = [x for x in arrLIdx if x != None]
      
      if len(arrR) == 0:
        break
    with open(os.path.abspath("config/adm_w.json"), 'w') as outfile:
      json.dump(self.dictAdm,outfile)
    with open(os.path.abspath("config/hlt_w.json"), 'w') as outfile:
      json.dump(self.dictHlt,outfile)   
    with open(os.path.abspath("config/sp_w.json"), 'w') as outfile:
      json.dump(self.dictWYC,outfile) 
    return arrT, district

  def res_q(self, rdata, teams, lst_idx, district,desc):
    self.desc = dict(desc)
    while True:
      
      arrTIdx = []
      arrD = []

      for it in lst_idx:

        team = teams[it] 
        for ir in rdata:
          if ir.get('count') == 0:
            continue
          print "Dis: ", ir.get('id'), ir.get('count'), unicode(team.get('st', ''), 'cp1251')
          rcount = float(ir.get('count'))
          rall = float(ir.get('all'))
          pr = rcount / rall
          res = 0.0

          if pr < 0.3:
            res = rcount * pr
          else:
            res = rcount * 0.2

          res = int(ceil(res))

          ir['count'] -= res
          team['count'] += res
          

          team.setdefault('dis_dt', {})
          team['dis_dt'].setdefault(ir.get('id'), 0)
          district[ir.get('id')]['count'] -= res 

          if district[ir.get('id')]['count'] < 0:
            print 'here 1'
            district[ir.get('id')]['count'] += res 
            team['count'] -= res
            continue


          team['dis_dt'][ir.get('id')] += res

          if team['count'] > team['need']:
            mi = team['count'] - team['need']
            ir['count'] += mi
            team['count'] -= mi
            district[ir.get('id')]['count'] += mi
            team['dis_dt'][ir.get('id')] -= mi
            
          
          if ir['count'] > 0:
            arrD.append(ir)
        
        if team['count'] < team['need']:
          arrTIdx.append(it)



      if len(arrTIdx) > 0:
        lst_idx = arrTIdx
        rdata = arrD
        if len(arrD) == 0:
          print 'here 2'
          rdata = self.change_q(self.desc) 
          if len(rdata) == 0:
            break
      else:
        break
    return teams, district


  def change_r(self, desc):

    dictWYC, dictAdm, dictHlt = self.b_utils.get_config_w()
    
    adm, hlt, sp = self.b_utils.get_weight(self.desc)

    try:

      admP, hltP, spP = self.change_weight(adm, hlt, sp, desc)
      
      admP,hltP, spP = self.b_utils.get_param_by_w(admP, hltP, spP)
      return (admP, hltP, spP)
    except ValueError:
      return ()
  def change_q(self, desc):
    res = []
    
    try:
      print 'Adm desc: ',desc.get('adm')
      print 'Sp desc: ',desc.get('mil_spec'), desc.get('gov_spec')
      adm, hlt, sp = self.change_r(desc)
      
      res = self.db.bld_q(adm, hlt, sp)
      
    except ValueError:
      return res
    
    return res
    
  def change_weight(self, adm, hlt, sp, tm):
    dictWYC, dictAdm, dictHlt = self.b_utils.get_config_w()
    print 'All param in start: ', adm, hlt, sp
    radm = self.change_adm(dictAdm, adm, tm)

    if radm > 0:
      self.desc['adm'] = self.b_utils.get_key_by_w(radm, 'adm')
      return (radm, hlt, sp)
    print 'All param after adm: ', radm, hlt, sp
    adm, rhlt = self.change_hlt(dictHlt, dictAdm, adm, hlt, tm)
    print 'Change hlt'
    if rhlt > 0:
      self.desc['hlt'] = self.b_utils.get_key_by_w(rhlt, 'hlt')
      return (adm, rhlt, sp)
    print 'All param after hlt: ', adm, rhlt, sp
    hlt, rsp = self.change_sp(dictHlt, dictWYC,hlt, sp, tm)
    print 'After change w: ', rsp
    if rsp > 0:
      self.desc['mil_spec'] = self.b_utils.get_key_by_w(rsp, 'sp')
      return (adm, hlt, rsp)

    else: 
      return ()


  def change_sp(self, dictHlt, dictWYC,hlt, sp, tm):
    dictHlt = dict(self.dictHlt)

    rhlt = dictHlt[str(tm.get('str_code')[3]) + str(tm.get('str_code')[4])].get('weight')

    spArr = sorted([(k,v.get('weight')) for k,v in dictWYC.items()], key=lambda x:x[1])

    sp = self.change_dt(spArr, sp)
    
    
    for el in spArr:
      dictWYC[el[0]]['weight'] = el[1]
    with open(os.path.abspath("config/health_w.json"), 'w') as outfile:
      json.dump(dictHlt,outfile)
    with open(os.path.abspath("config/sp_w.json"), 'w') as outfile:
      json.dump(dictWYC,outfile)
    return (rhlt,sp)

  def change_hlt(self, dictHlt, dictAdm, adm, hlt, tm):
    dictAdm = dict(self.dictAdm)

    radm = self.dictAdm[tm.get('str_code')[2]].get('weight')

    hltArr = sorted([(k,v.get('weight')) for k,v in dictHlt.items()], key=lambda x:x[1])
    hlt = self.change_dt(hltArr, hlt)
    
    
    for el in hltArr:
      dictHlt[el[0]]['weight'] = el[1]
    with open(os.path.abspath("config/adm_w.json"), 'w') as outfile:
      json.dump(dictAdm,outfile)
    with open(os.path.abspath("config/health_w.json"), 'w') as outfile:
      json.dump(dictHlt,outfile)
    return (radm,hlt)


  def change_adm(self, dictAdm, adm, tm):
    admArr = sorted([(k,v.get('weight')) for k,v in dictAdm.items()], key=lambda x:x[1])
    
    adm = self.change_dt(admArr, adm)
    
    for el in admArr:
      dictAdm[el[0]]['weight'] = el[1]

    with open(os.path.abspath("config/adm_w.json"), 'w') as outfile:
      json.dump(dictAdm,outfile)
    return adm

  def change_dt(self, arr, param):
    print arr, [ idx for idx, v in enumerate(arr) if v[1] == param], param
    idx = [ idx for idx, v in enumerate(arr) if v[1] == param]
    
    if len(idx) > 0:
      t = (arr[idx[0]][0], 0)
      arr[idx[0]] = t
    
    arrDt = [ v for  k,v in arr if v != 0]
    try:
      param = min(arrDt, key=lambda x: abs(x - param))
    except:
      param = 0
    print 'Get param: ', param, arrDt, arr
    return param

 