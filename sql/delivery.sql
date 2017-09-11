CREATE TABLE delivery (
 id serial PRIMARY KEY,
  date_delivery timestamp without time zone default now() not null,
  district_id int default 0 not null,
  foreign key (district_id) references district (id)
)