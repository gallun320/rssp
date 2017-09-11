import psycopg2 as db



class Api():
  def __init__(self):
    self.speaker = db.connect(host='127.0.0.1', user='postgres',password=1, dbname='rsSp')
    
  def get_sp(self, sp):
    cur = self.speaker.cursor()
    
    cur.execute("select name from spec_class where idx = %s",[sp])
    
    res = cur.fetchall()[0][0]
    
    return res
  
  def get_count_gov_health(self, hlt_n, sp):
    cur = self.speaker.cursor()
    
    q = '''select 
        COALESCE(count( (select first_adm from {0} where id = health.{0}_id)),0) +  
        COALESCE(count( (select second_adm from {0} where id = health.{0}_id)),0) + 
        COALESCE(count( (select third_adm from {0} where id = health.{0}_id)),0) +  
        COALESCE(count( (select without_adm from {0} where id = health.{0}_id)),0) 
        
        from district,health where health.id = district.health_id  and district.type = {1} '''.format(hlt_n, sp)
    
    cur.execute(q)
    
    return int(cur.fetchall()[0][0])
