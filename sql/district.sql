CREATE TABLE district (
  id serial PRIMARY KEY,
  dis_id int default 0 not null,
  health_id int default 0 not null,
  type int default 0 not null,
  foreign key (health_id) references health (id)
)