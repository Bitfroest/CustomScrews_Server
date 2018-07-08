-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.1-beta
-- PostgreSQL version: 10.0
-- Project Site: pgmodeler.io
-- Model Author: ---


-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: screws | type: DATABASE --
-- -- DROP DATABASE IF EXISTS screws;
-- CREATE DATABASE screws
-- 	ENCODING = 'UTF8'
-- 	LC_COLLATE = 'German_Germany.1252'
-- 	LC_CTYPE = 'German_Germany.1252'
-- 	TABLESPACE = pg_default
-- 	OWNER = postgres
-- ;
-- -- ddl-end --
-- 

-- object: public.iso_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.iso_id_seq CASCADE;
CREATE SEQUENCE public.iso_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;
-- ddl-end --
ALTER SEQUENCE public.iso_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.length_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.length_id_seq CASCADE;
CREATE SEQUENCE public.length_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;
-- ddl-end --
ALTER SEQUENCE public.length_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.iso_4762 | type: TABLE --
-- DROP TABLE IF EXISTS public.iso_4762 CASCADE;
CREATE TABLE public.iso_4762(
	id integer NOT NULL DEFAULT nextval('public.iso_id_seq'::regclass),
	name text,
	body_diameter real,
	head_diameter real,
	head_height real,
	hexagon_diameter real,
	hexagon_height real,
	created timestamp,
	user_id_user text,
	CONSTRAINT id PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.iso_4762 OWNER TO postgres;
-- ddl-end --

-- object: public.iso_4762_length | type: TABLE --
-- DROP TABLE IF EXISTS public.iso_4762_length CASCADE;
CREATE TABLE public.iso_4762_length(
	id integer NOT NULL DEFAULT nextval('public.length_id_seq'::regclass),
	thread_length real,
	body_length real,
	sid integer NOT NULL,
	CONSTRAINT iso_4762_length_pkey PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.iso_4762_length OWNER TO postgres;
-- ddl-end --

-- object: public."user" | type: TABLE --
-- DROP TABLE IF EXISTS public."user" CASCADE;
CREATE TABLE public."user"(
	id text NOT NULL,
	email text,
	display_name text,
	name text,
	CONSTRAINT user_pk PRIMARY KEY (id)

);
-- ddl-end --

-- object: user_fk | type: CONSTRAINT --
-- ALTER TABLE public.iso_4762 DROP CONSTRAINT IF EXISTS user_fk CASCADE;
ALTER TABLE public.iso_4762 ADD CONSTRAINT user_fk FOREIGN KEY (user_id_user)
REFERENCES public."user" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: screwfk | type: CONSTRAINT --
-- ALTER TABLE public.iso_4762_length DROP CONSTRAINT IF EXISTS screwfk CASCADE;
ALTER TABLE public.iso_4762_length ADD CONSTRAINT screwfk FOREIGN KEY (sid)
REFERENCES public.iso_4762 (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --


