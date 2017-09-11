import psycopg2 as db


class DisDB():
  """Get data about district"""

  def __init__(self):
        self.speaker = db.connect(
            host='127.0.0.1', user='postgres', password=1, dbname='rsSp')

  def get_district(self):
    cur = self.speaker.cursor()

    cur.execute('''
			select 
				district.dis_id, 
				district.type, 
				(select name from dis_class where district.dis_id = dis_class.idx),
				a1.first_adm,
				a1.second_adm,
				a1.third_adm,
				a1.without_adm,
				a2.first_adm,
				a2.second_adm,
				a2.third_adm,
				a2.without_adm,
				b3.first_adm,
				b3.second_adm,
				b3.third_adm,
				b3.without_adm,
				b4.first_adm,
				b4.second_adm,
				b4.third_adm,
				b4.without_adm,
				((a1.first_adm +
				a1.second_adm +
				a1.third_adm +
				a1.without_adm) + (a2.first_adm +
				a2.second_adm +
				a2.third_adm +
				a2.without_adm) + (b3.first_adm +
				b3.second_adm +
				b3.third_adm +
				b3.without_adm) + (b4.first_adm +
				b4.second_adm +
				b4.third_adm +
				b4.without_adm))
			from 
				district 
			inner join 
				health on health.id = district.health_id 
			inner join 
				a1 on a1.id = health.a1_id
			inner join 
				a2 on a2.id = health.a2_id
			inner join 
				b3 on b3.id = health.b3_id 
			inner join 
				b4 on b4.id = health.b4_id   
			''')

    res = cur.fetchall()

    cur.execute('''
					select idx from dis_class group by idx;
				''')

    dis = cur.fetchall()

    res = sorted(res, key=lambda x: x[0])

    dis = sorted(dis, key=lambda x: x[0])

    it = 0
    jt = 0

    dt = {}

    while True:
      if res[it][0] == dis[jt][0]:
        idx = res[it][0]
        dt.setdefault(idx, {})
        dt[idx].setdefault('name', res[it][2])
        dt[idx].setdefault('sp', {})
        dt[idx]['sp'][res[it][1]] = {
                    'a1': (res[it][3], res[it][4], res[it][5], res[it][6]),
                    'a2': (res[it][7], res[it][8], res[it][9], res[it][10]),
                    'b3': (res[it][11], res[it][12], res[it][13], res[it][14]),
                    'b4': (res[it][15], res[it][16], res[it][17], res[it][18])
                }
        dt[idx].setdefault('count', 0)
        dt[idx].setdefault('all', 0)
        dt[idx]['count'] += res[it][19]
        dt[idx]['all'] += res[it][19]
        it += 1
      else:
        jt += 1

      if jt > len(dis) - 1 or it > len(res) - 1:
        break
    return dt
