create table health (
  id serial primary key,
  a1_id int default 0 not null references a1 (id),
  a2_id int default 0 not null references a2 (id),
  b3_id int default 0 not null references b3 (id),
  b4_id int default 0 not null references b4 (id)
)