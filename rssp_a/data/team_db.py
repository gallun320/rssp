import psycopg2 as db


class TeamDB():
  def __init__(self):
    self.speaker = db.connect(host='127.0.0.1', user='postgres',password=1, dbname='W_16')
    
  def get_team_data(self):
    arr = []
    
    cur = self.speaker.cursor()
    
    cur.execute("select p302_g7, p049_g7, p105_g7, p113_g7, r4054_g7, r1016_g7, r4076_g7, r7147_g7, p4040_g7, psh_code, p102_res, p102_all from gsp07_n where p049_g7 <> '-'")
    
    res = cur.fetchall()
    
    for el in res:
      pod = [] if el[9] == None else [dict([(x.split('#')[0],x.split('#')[1])]) for x in el[9].split(',')]
      arr.append({
        "n_ocr": el[0],
        "n_team": el[1],
        "tm": el[2],
        "st": el[3],
        "need_desc": {
          "tm": el[2],
          "mil_spec": el[4],
          "gov_spec": el[5],
          "adm": el[6],
          "hlt": str(el[7]) + str(el[8]),
          "str_code": el[4:9]
        },
        "pod": pod,
        "count": el[10],
        "need": el[11],
        "dis_dt": {},
        
      })
    
    return arr
  
  def getSpData(self):
    cur = self.speaker.cursor()
    cur.execute("SELECT DISTINCT r4054_g7 FROM gsp07_n WHERE r4054_g7 <> '-'")
    res = cur.fetchall()
    return res
  

if __name__ == "__main__":
  t = TeamDB()
  
  t.get_team_data()