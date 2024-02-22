--------------------------------------------------------------------------------
-- Creates the tables for the first spatial lab.
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- Create postgis extension
--------------------------------------------------------------------------------
create extension postgis;

--------------------------------------------------------------------------------
--
--------------------------------------------------------------------------------

drop table if exists roads;
drop table if exists poi;
drop table if exists forests;

create table poi (
    id    int        primary key,
    geom  geometry   not null
);

create table forests (
    id   int        primary key,
    sid  varchar(8) unique not null,
    geom geometry   not null
);

create table roads (
    id          int         primary key,
    sid         varchar(8)  unique not null,
    geom        geometry    not null,
    description varchar(60)
);


