import utils.api as api

import os
import json

class BuilderUtils():
  def __init__(self):
    self.api = api.Api()
    with open(os.path.abspath("config/sp_w.json")) as dt:
      self.dictWYC = json.load(dt)

    with open(os.path.abspath("config/adm_w.json")) as dt:
      self.dictAdm = json.load(dt)
    
    with open(os.path.abspath("config/health_w.json")) as dt:
      self.dictHlt = json.load(dt)

  def filterd_lst_teams(self, lst, fil_str):
    arr = []
    
    for idx, fil in enumerate(lst):
      desc_str = fil.get('need_desc').get('str_desc')
      if desc_str == fil_str:
        arr.append(idx)
        
    return arr

  def get_param_q(self, dt):
    
    adm = self.dictAdm.get(dt.get('adm')).get('param')
    
    hlt = self.dictHlt.get(dt.get('hlt')).get('param')
    
    sp = self.get_sp(dt.get('mil_spec'), dt.get('gov_spec')).get('param')
    
    return (adm, hlt, sp)
  def get_param_by_w(self, adm, hlt, spP):
      
    print 'Enter'
    adm = [x.get('param') for k,x in self.dictAdm.items() if x.get('weight') == adm][0]
    print adm
    hlt = [x.get('param') for k,x in self.dictHlt.items() if x.get('weight') == hlt][0]
    print hlt
    sp = [x.get('param') for k,x in self.dictWYC.items() if x.get('weight') == spP]
    print spP
    if len(sp) == 0 and spP == 2:
      sp = 888888
    else:
      sp = sp[0]
        
    print adm, hlt, sp
    return (adm, hlt, sp)
  
  def get_key_by_w(self, param,  keyW = ''):
    
    if keyW == "adm":
      adm = [k for k,x in self.dictAdm.items() if x.get('weight') == param][0]
      return adm
    elif keyW == "hlt":
      hlt = [k for k,x in self.dictHlt.items() if x.get('weight') == param][0]
      return hlt
    elif keyW == "sp":
      sp = [k for k,x in self.dictWYC.items() if x.get('weight') == param]
      if len(sp) == 0 and param == 2:
        sp = 888888
      else:
        sp = sp[0]
      return sp
    '''else:
      adm = [k for k,x in self.dictAdm.items() if x.get('weight') == adm][0]
      hlt = [k for k,x in self.dictHlt.items() if x.get('weight') == hlt][0]
      sp = [k for k,x in self.dictWYC.items() if x.get('weight') == sp][0]
      return (adm, hlt, sp)'''

  def get_sp(self, mil_spec, gov_spec):
    if mil_spec is '-' and gov_spec is '-':
      return self.dictWYC.get('888888')
    elif not mil_spec is '-':
      return self.dictWYC.get(mil_spec)
    else:
      res_a1 = self.api.get_count_gov_health('a1', gov_spec)
      
      res_a2 = self.api.get_count_gov_health('a2', gov_spec)
      
      res_b3 = self.api.get_count_gov_health('b3', gov_spec)
      
      res_b4 = self.api.get_count_gov_health('b4', gov_spec)
      
      res = res_a1 + res_a2 + res_b3 + res_b4
      
      return {'weight': 2, 'param': gov_spec}
    '''
      if res > 0:
        return {'weight': 2, 'param': gov_spec}
      else:
        return {'weight': 0, 'param': gov_spec}'''

  def get_weight_sum(self,dt):
    adm, hlt, sp = self.get_weight(dt)
    
    return adm + hlt + sp


  def get_weight(self, dt):
    
    adm = self.dictAdm.get(dt.get('adm')).get('weight')

    hlt = self.dictHlt.get(dt.get('hlt')).get('weight')
    
    sp = self.get_sp(dt.get('mil_spec'), dt.get('gov_spec')).get('weight')

    return (adm, hlt, sp)

  def get_res(self, teams):
    max = 0
    iter = 0
    
    for idx in xrange(0,len(teams)):
      if teams[idx] == None:
        continue
      else:
        team_w = self.get_weight_sum(teams[idx].get('need_desc'))
      
      
      
      if team_w > max:
        max = team_w
        iter = idx
      
    return iter

  def get_config_w(self):
    dictWYC = {}
    dictAdm = {}
    dictHlt = {}

    with open(os.path.abspath("config/sp_w.json")) as dt:
      dictWYC = json.load(dt)

    with open(os.path.abspath("config/adm_w.json")) as dt:
      dictAdm = json.load(dt)
    
    with open(os.path.abspath("config/health_w.json")) as dt:
      dictHlt = json.load(dt)


    return (dictWYC, dictAdm, dictHlt)

