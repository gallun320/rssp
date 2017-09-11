import os
import json
import pprint

class PshfWorker():
  def __init__(self):
    self.dictWYC = {}
    self.dictAdm = {}
    self.dictHlt = {}
    
    with open(os.path.abspath("config/sp_w.json")) as dt:
      self.dictWYC = json.load(dt)

    with open(os.path.abspath("config/adm_w.json")) as dt:
      self.dictAdm = json.load(dt)
    
    with open(os.path.abspath("config/health_w.json")) as dt:
      self.dictHlt = json.load(dt)
      
  def set_pshf(self, teams, districts):
    for team in teams:
      for psh in team['pod']:
        arr = psh.items()[0]
        dis_idx = int(arr[0])
        dis_dt = int(arr[1])
        
        team.setdefault('dis', {})

        if districts.has_key(dis_idx) == False:
          continue
  
        team['dis'].setdefault(dis_idx, 0)

        team['dis'][dis_idx] += dis_dt
        
        team['count'] += dis_dt
        
        districts[dis_idx]['count'] -= dis_dt
        team.setdefault('dis_dt', {})
        
        team['dis_dt'].setdefault(dis_idx, 0)
        team['dis_dt'][dis_idx] += dis_dt
        
        if team['count'] > team['need']:
          mi = team['count'] - team['need']
          team['count'] -= mi
          districts[dis_idx]['count'] += mi
          team['dis_dt'][dis_idx] -= mi
          
        desc = team.get('need_desc')
        
        
        
        hlt = self.dictHlt[desc.get('hlt')].get('param')
        adm = 0
        sp = ''
        
        try:
          adm = int(desc.get('adm')) - 1
          if adm > 3:
            adm = 3
        except:
          adm = 3
          
        if desc.get('mil_spec') is '-' and desc.get('gov_spec') is '-':
          sp = '888888'
        elif not desc.get('mil_spec') is '-':
          sp = desc.get('mil_spec')
        else:
          sp = desc.get('gov_spec')
        if districts[dis_idx]['sp'].has_key(sp) == False:
          continue
          
        districts[dis_idx]['sp'][sp][hlt][adm] -= dis_dt
        
    return (teams, districts)
        
        
        