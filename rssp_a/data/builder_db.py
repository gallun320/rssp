#! /usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2 as db


class BuilderDB():
  def __init__(self):
    self.speaker = db.connect(host='127.0.0.1', user='postgres',password=1, dbname='rsSp')

  def bld_q(self, adm, hlt, sp):
    cur = self.speaker.cursor()
    q = '''
      select 
        district.dis_id, 
        district.type, 
        sum({1}.{0}),
        (select sum(a1.first_adm + a1.second_adm + a1.third_adm + a1.without_adm + 
          a2.first_adm + a2.second_adm + a2.third_adm + a2.without_adm +
          b3.first_adm + b3.second_adm + b3.third_adm + b3.without_adm +
          b4.first_adm + b4.second_adm + b4.third_adm + b4.without_adm) from district
        join health on health.id = district.health_id
        join a1 on health.a1_id = a1.id
        join a2 on health.a2_id = a2.id
        join b3 on health.b3_id = b3.id
        join b4 on health.b4_id = b4.id)
        from district inner join health on district.health_id = health.id 
        inner join {1} on health.{1}_id = {1}.id
        where district.type = {2} group by district.dis_id,district.type;
    '''.format(adm, hlt, sp)

    cur.execute(q)
    
    res = cur.fetchall()

    res = [{'id': el[0], 
            'type': el[1],
            'count': el[2],
            'all': el[3]} for el in res]
    cur.close()
    return res