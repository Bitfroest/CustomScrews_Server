-- Database: screws

-- DROP DATABASE screws;

CREATE DATABASE screws
  WITH OWNER = postgres
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'German_Germany.1252'
       LC_CTYPE = 'German_Germany.1252'
       CONNECTION LIMIT = -1;

-- Table: public.iso_4762

-- DROP TABLE public.iso_4762;

CREATE TABLE public.iso_4762
(
  id integer NOT NULL,
  name text,
  body_diameter real,
  head_diameter real,
  head_height real,
  hexagon_diameter real,
  hexagon_height real,
  thread_length real,
  body_length real,
  CONSTRAINT id PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.iso_4762
  OWNER TO postgres;
