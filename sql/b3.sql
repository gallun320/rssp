create table b3 (
  id serial primary key,
  first_adm int default 0 not null,
  second_adm int default 0 not null,
  third_adm int default 0 not null,
  without_adm int default 0 not null
)