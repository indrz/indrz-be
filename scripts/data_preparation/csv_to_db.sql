create table geodata.tu_buildings
(
	id serial
		constraint tu_buildings_pk
			primary key,
	campus varchar,
	wing varchar,
	wing_description varchar,
	address varchar,
	plz varchar,
	city varchar,
	floor_name varchar
);
alter table geodata.tu_buildings owner to tu;


create table geodata.tu_roomdata
(
	id serial not null
		constraint tu_roomdata_pk
			primary key,
	roomcode varchar,
	description varchar
);

alter table geodata.tu_roomdata owner to tu;



