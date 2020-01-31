CREATE DATABASE IF NOT EXISTS musical_talent;

CREATE EXTENSION IF NOT EXISTS postgis;

DROP TABLE IF EXISTS musicians;
DROP TABLE IF EXISTS instruments;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS cantons;

CREATE TABLE cantons (
	gid integer NOT NULL PRIMARY KEY,
	kannum integer NOT NULL,
	name varchar NOT NULL,
	geom geometry
);

CREATE TABLE genres (
	id SERIAL PRIMARY KEY,
	name varchar
);

CREATE TABLE skills (
	id SERIAL PRIMARY KEY,
	name varchar
);

CREATE TABLE instruments (
	id SERIAL PRIMARY KEY,
	name varchar
);

CREATE TABLE musicians (
	id SERIAL PRIMARY KEY,
	name varchar,
	lastname varchar,
  email varchar,
  pt geometry,
	instrument_id integer REFERENCES instruments(id),
	skill_id1 integer REFERENCES skills(id),
	skill_id2 integer REFERENCES skills(id),
	skill_id3 integer REFERENCES skills(id),
  skill_id4 integer REFERENCES skills(id),
  genre_id1 integer REFERENCES genres(id),
  genre_id2 integer REFERENCES genres(id),
  genre_id3 integer REFERENCES genres(id),
  genre_id4 integer REFERENCES genres(id),
  genre_id5 integer REFERENCES genres(id)
);

-- in terminal with directory "../data/shp":
-- psql musical_talent < psql.sql

-- INSERT INTO cantons
-- SELECT gid, kantonsnum, name, geom
-- FROM plz;

CREATE INDEX musicians_gix ON musicians USING GIST (pt);
CREATE INDEX cantons_gix ON cantons USING GIST (geom);
