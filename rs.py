import psycopg2 as db
import sqlite3 as dbs
from math import floor, ceil
import pprint

chData = [
  {
    "_id": 0,
    "count": 0,
    "need": 1,
    "type": "spec",
    "name_sp": "dr",
    "dis": []
  },
  {
    "_id": 1,
    "count": 0,
    "need": 43,
    "type": "spec",
    "name_sp": "mtlb",
    "dis": []
  },
  {
    "_id": 2,
    "count": 0,
    "need": 25,
    "type": "spec",
    "name_sp": "btr",
    "dis": []
  },
  {
    "_id": 3,
    "count": 0,
    "need": 19,
    "type": "spec",
    "name_sp": "dr",
    "dis": []
  },
  {
    "_id": 4,
    "count": 0,
    "need": 44,
    "type": "spec",
    "name_sp": "btr",
    "dis": []
  },
  {
    "_id": 5,
    "count": 0,
    "need": 18,
    "type": "spec",
    "name_sp": "btr",
    "dis": []
  },
  {
    "_id": 6,
    "count": 0,
    "need": 23,
    "type": "spec",
    "name_sp": "mtlb",
    "dis": []
  },
  {
    "_id": 7,
    "count": 0,
    "need": 2,
    "type": "spec",
    "name_sp": "mtlb",
    "dis": []
  },
  {
    "_id": 8,
    "count": 0,
    "need": 28,
    "type": "spec",
    "name_sp": "dr",
    "dis": []
  },
  {
    "_id": 9,
    "count": 0,
    "need": 43,
    "type": "spec",
    "name_sp": "btr",
    "dis": []
  },
  {
    "_id": 10,
    "count": 0,
    "need": 37,
    "type": "spec",
    "name_sp": "dr",
    "dis": []
  }
]

rData = [
  {
    "_id": 0,
    "data": [
      {
        "all": 2,
        "type": "btr"
      },
      {
        "all": 8,
        "type": "mtlb"
      },
      {
        "all": 4,
        "type": "dr"
      }
    ]
  },
  {
    "_id": 1,
    "data": [
      {
        "all": 16,
        "type": "btr"
      },
      {
        "all": 19,
        "type": "mtlb"
      },
      {
        "all": 9,
        "type": "dr"
      }
    ]
  },
  {
    "_id": 2,
    "data": [
      {
        "all": 12,
        "type": "btr"
      },
      {
        "all": 18,
        "type": "mtlb"
      },
      {
        "all": 16,
        "type": "dr"
      }
    ]
  },
  {
    "_id": 3,
    "data": [
      {
        "all": 18,
        "type": "btr"
      },
      {
        "all": 20,
        "type": "mtlb"
      },
      {
        "all": 13,
        "type": "dr"
      }
    ]
  },
  {
    "_id": 4,
    "data": [
      {
        "all": 13,
        "type": "btr"
      },
      {
        "all": 9,
        "type": "mtlb"
      },
      {
        "all": 13,
        "type": "dr"
      }
    ]
  },
  {
    "_id": 5,
    "data": [
      {
        "all": 12,
        "type": "btr"
      },
      {
        "all": 1,
        "type": "mtlb"
      },
      {
        "all": 15,
        "type": "dr"
      }
    ]
  },
  {
    "_id": 6,
    "data": [
      {
        "all": 7,
        "type": "btr"
      },
      {
        "all": 12,
        "type": "mtlb"
      },
      {
        "all": 19,
        "type": "dr"
      }
    ]
  },
  {
    "_id": 7,
    "data": [
      {
        "all": 19,
        "type": "btr"
      },
      {
        "all": 2,
        "type": "mtlb"
      },
      {
        "all": 8,
        "type": "dr"
      }
    ]
  },
  {
    "_id": 8,
    "data": [
      {
        "all": 9,
        "type": "btr"
      },
      {
        "all": 6,
        "type": "mtlb"
      },
      {
        "all": 2,
        "type": "dr"
      }
    ]
  }
]

#pp = pprint.PrettyPrinter(indent=4)


class Rs():
  def __init__(self):
    pass
  def rs(self, chdata, rdata):
    arr = []
    for ch in chdata:
      if ch['count'] < ch['need']:
        for r in rdata:
          normR = r['all']
          if ch['count'] < ch['need']:
            for dt in r['data']:
              if ch['name_sp'] == dt['type'] and dt['count'] > 0:
                pr = float(dt['count'])/float(normR)
                res = 0.0
                if pr < 0.3:
                  res = float(dt['count']) * pr
                else:
                  res = float(dt['count']) * 0.2
                #print dt['type'], dt['count'], int(ceil(res))
                dt['count'] -= int(ceil(res))
                ch['count'] += int(ceil(res))
                r['count'] -= int(ceil(res))
                r[ch['name_sp']] -= int(ceil(res))
                if ch['count'] > ch['need']:
                  mi = ch['count'] - ch['need']
                  ch['count'] -= mi
                  dt['count'] += mi 
                  r['count'] += mi
                  r[ch['name_sp']] += mi
                  res -= mi
                d = dict((i['id'],i['count']) for i in ch['dis'])
                if r['id'] in d:
                  for el in ch['dis']:
                    if el['id'] == r['id']:
                      el['count'] += int(ceil(res)) 
                else:
                  ch['dis'].append({'id': r['id'],'name': r['name'], 'count': int(ceil(res))})
                arr.append(ch)
    if len(arr) > 0:
      self.rs(arr,rdata)
  def chPshefRs(self, chdata):
    for ch in chdata:
      pshf = []
      arr = []
      if ch['pshef'] != None:
        pshname = unicode(ch['pshname'],'cp1251').split(',')
        pshf = ch['pshef'].split(',')
        for idx,psel in enumerate(pshf):
          psel = psel.split('#')
          
          arr.append({'id': psel[0],'name': pshname[idx], 'count': int(psel[1])})
      ch['pshef'] = arr
    return chdata
  
  def chRs(self, chdata, rdata):
    chdata = self.chPshefRs(chdata)
    for ch in chdata:
      for psel in ch['pshef']:
        for r in rdata:
          if r['id'] == psel['id']:
            for el in r['data']:
              if el['type'] == ch['name_sp']:
                if ch['need'] < psel['count']:
                  r[ch['name_sp']] -= ch['need']

                  ch['count'] += ch['need']
                  el['count'] -= ch['need']
                  r['count'] -= ch['need']
                  ch['dis'].append({'id': psel['id'],'name': psel['name'], 'count': ch['need']})
                else:
                  r[ch['name_sp']] -= psel['count']

                  ch['count'] += psel['count']
                  el['count'] -= psel['count']
                  r['count'] -= psel['count']
                  ch['dis'].append({'id': psel['id'],'name': psel['name'], 'count': psel['count']})




        
class DB():
  def __init__(self):
    self.speaker = db.connect(host='127.0.0.1', user='postgres',password=1, dbname='W_16')
    self.talker = dbs.connect('test.db')
  def getChData(self):
    arr = []
    cur = self.speaker.cursor()
    cur.execute("SELECT oid, p302_g7,  r4054_g7, p102_all, psh_code, p113_g7, p049_g7, psh_text, p105_g7 FROM gsp07_n WHERE r4054_g7 <> '-'")
    res = cur.fetchall()
    for i in res:
      sh = False
      if i[4] != None:
        sh = True
      arr.append({'id': i[0],
                  'name': i[5],
                  'noteam': i[1], 
                  'nteam': i[6],
                  'count': 0, 
                  'need': i[3], 
                  'type': 'spec', 
                  'name_sp': i[2], 
                  'pshef': i[4],
                  'pshname': i[7],
                  'date': i[8],
                  'sh': sh,
                  'dis': []
                 })
    #pp.pprint(arr)
    return arr
  def getRData(self):
    arr = []
    cur = self.speaker.cursor()
    cur.execute("SELECT gsp11_n.r8012_g11,gsp11_n.p205_g11,gsp11_n.r4054_g11, gsp11_n.yr,r8012.p01  FROM gsp11_n, r8012 WHERE r8012.p00 = gsp11_n.r8012_g11 and gsp11_n.r4054_g11 <> '-' and gsp11_n.r8012_g11 <> '-' and gsp11_n.yr = '20161'")
    res = cur.fetchall()
    
    for i in res:
      if len(arr) == 0:
        arr.append({ 'id': i[0], 'name': unicode(i[4], 'cp1251'),'all': i[1], 'count': i[1],'data': []})
      else:
        d = dict((x['id'],it) for it,x in enumerate(arr))
        if i[0] in d:
          for el in arr:
            if el['id'] == i[0]:
              el['all'] += i[1]
              el['count'] += i[1]
        else:
          arr.append({ 'id': i[0], 'name': unicode(i[4], 'cp1251'),'all': i[1],'count': i[1],'data': []})
          
      for dt in arr:
        if i[0] == dt['id']: 
          if len(dt['data']) == 0:
            dt[i[2]] = i[1]
            dt['data'].append({ 'type': i[2], 'count': i[1], 'all': i[1] })
          else:
            dl = dict((x['type'], it) for it,x in enumerate(dt['data']))
            if i[2] in dl:
              for dtel in dt['data']:
                if dtel['type'] == i[2]:
                  dt[i[2]] += i[1]
                  #print i[1],i[2], dtel['count'], dt['id']
                  dtel['count'] += i[1]
                  dtel['all'] += i[1]
            else:
              dt[i[2]] = i[1]
              dt['data'].append({ 'type': i[2], 'count': i[1], 'all': i[1] })
      
    #pp.pprint(arr)
    return arr
  def getSpData(self):
    cur = self.speaker.cursor()
    cur.execute("SELECT DISTINCT r4054_g7 FROM gsp07_n WHERE r4054_g7 <> '-'")
    res = cur.fetchall()
    return res




  
  
  
'''
if __name__ == "__main__":
  dbC = DB()
  chData = dbC.getChData()
 
  rData = dbC.getRData()
  clrs = Rs()
  clrs.chRs(chData, rData)
  clrs.rs(chData, rData)
  pp.pprint(chData)
'''
