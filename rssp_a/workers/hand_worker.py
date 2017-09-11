

class HandWorker():
  def __init__(self, teams, districts):
    self.teams = list(teams)
    self.districts = dict(districts)
    
    self.mtx = self.set_mtx()
    
  def set_mtx(self):
    mtx = []
    
    teams = list(self.teams)
    districts = self.districts.items()
    
    for idx, team in enumerate(teams):
      mtx.insert(idx, [])
      for jdx, dis in enumerate(districts):
        mtx[idx].insert(jdx, 0)
        t = team
        d = dis
        ddc = 0
        if len(t.get('dis_dt')) != 0 and  t.get('dis_dt').get(d[0],'') != '':
          ddc = t.get('dis_dt').get(d[0])
          
        mtx[idx][jdx] = (idx, jdx, d[0], ddc)
    
    return mtx
  
  def get_mtx(self):
    return self.mtx
  
  def set_mtx_item(self, row, col, dt):
    self.mtx[row][col] = (row, col, self.mtx[row][col][2], dt)
        