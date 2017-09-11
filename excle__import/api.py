import psycopg2 as db


class Api():
  def __init__(self):
    self.speaker = db.connect(host='127.0.0.1', user='postgres',password=1, dbname='rsSp')
  
  def get_district(self):
    
    cur = self.speaker.cursor()
    
    cur.execute("SELECT idx, name from dis_class")
    
    res = cur.fetchall()
    
    return res