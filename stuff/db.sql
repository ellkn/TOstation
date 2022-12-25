CREATE DATABASE "TO"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

BEGIN;

CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    email text,
    password text,
    lastname text,
    firstname text,
    phone text,
    role integer,
    PRIMARY KEY (id),
    CONSTRAINT email UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS public.roles
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    role text,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.goods
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    name text,
    price money,
    type integer,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.status
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    status text,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.services
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    name text,
    price money,
    type integer,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.shop
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    user_id integer,
    good_id integer,
    datetime timestamp without time zone,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.serviceshop
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    employees_id integer,
    user_id integer,
    service_id integer,
    datein timestamp without time zone,
    dateout timestamp without time zone,
    status integer,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.types
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    type name,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.servicetypes
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    type text,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.users
    ADD CONSTRAINT role FOREIGN KEY (role)
    REFERENCES public.roles (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.goods
    ADD CONSTRAINT type FOREIGN KEY (type)
    REFERENCES public.types (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.services
    ADD CONSTRAINT type FOREIGN KEY (type)
    REFERENCES public.servicetypes (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.shop
    ADD CONSTRAINT user_id FOREIGN KEY (user_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.shop
    ADD CONSTRAINT good_id FOREIGN KEY (good_id)
    REFERENCES public.goods (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.serviceshop
    ADD CONSTRAINT employees_id FOREIGN KEY (employees_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.serviceshop
    ADD CONSTRAINT user_id FOREIGN KEY (user_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.serviceshop
    ADD CONSTRAINT service_id FOREIGN KEY (service_id)
    REFERENCES public.services (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.serviceshop
    ADD CONSTRAINT status FOREIGN KEY (status)
    REFERENCES public.status (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;


INSERT INTO public.roles (role) VALUES ('USER'::text) returning id;
INSERT INTO public.roles (role) VALUES ('ADMIN'::text) returning id;
INSERT INTO public.roles (role) VALUES ('EMPLOYEE'::text) returning id;

INSERT INTO public.status (status) VALUES ('OPEN'::text) returning id;
INSERT INTO public.status (status) VALUES ('CLOSED'::text) returning id;
INSERT INTO public.status (status) VALUES ('CANCELED'::text) returning id;

INSERT INTO public.servicetypes (type) VALUES ('Двигатель'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Передняя подвеска'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Задняя подвеска'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Сцепление'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Трансмиссия'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Тормозная система'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Задний мост'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Выхлопная система'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Арматурные работы'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Топливная система'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Электротехнические работы'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Система охлаждения'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Карданные валы'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Смазочно-заправочные работы'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Система выпуска газа'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Шиномонтаж'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Рулевое управление'::text) returning id;
INSERT INTO public.servicetypes (type) VALUES ('Контрольно-диагностические работы'::text) returning id;


INSERT INTO public.types (type) VALUES ('Аксессуары'::name) returning id;
INSERT INTO public.types (type) VALUES ('Запчасти для ТО'::name) returning id;
INSERT INTO public.types (type) VALUES ('Масла моторные'::name) returning id;
INSERT INTO public.types (type) VALUES ('Жидкости для омывателя стекла'::name) returning id;
INSERT INTO public.types (type) VALUES ('Жидкости тормозные'::name) returning id;
INSERT INTO public.types (type) VALUES ('Жидкости охлаждающие'::name) returning id;
INSERT INTO public.types (type) VALUES ('Шины летние'::name) returning id;
INSERT INTO public.types (type) VALUES ('Шины зимние'::name) returning id;
INSERT INTO public.types (type) VALUES ('Диски колесные, литые'::name) returning id;
INSERT INTO public.types (type) VALUES ('Диски колесные, штампованные'::name) returning id;
INSERT INTO public.types (type) VALUES ('Шины мотоциклетные'::name) returning id;
INSERT INTO public.types (type) VALUES ('Лампы'::name) returning id;
INSERT INTO public.types (type) VALUES ('Аккумуляторы'::name) returning id;
INSERT INTO public.types (type) VALUES ('Камеры заднего вида'::name) returning id;
INSERT INTO public.types (type) VALUES ('Предохранители'::name) returning id;
INSERT INTO public.types (type) VALUES ('Парковочные радары'::name) returning id;
INSERT INTO public.types (type) VALUES ('Электрооборудование'::name) returning id;
INSERT INTO public.types (type) VALUES ('Инструмент'::name) returning id;
INSERT INTO public.types (type) VALUES ('Щётки стеклоочистителя'::name) returning id;
INSERT INTO public.types (type) VALUES ('Охранные системы'::name) returning id;
INSERT INTO public.types (type) VALUES ('Автоакустика'::name) returning id;
