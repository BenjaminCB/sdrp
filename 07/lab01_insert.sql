--------------------------------------------------------------------------------
-- Inserts the spatial data for the first spatial lab
--------------------------------------------------------------------------------
insert into poi values
(0,  ST_GeomFromText('POINT(1.5 7)')),
(1,  ST_GeomFromText('POINT(3 10)')),
(2,  ST_GeomFromText('POINT(15 9.5)')),
(3,  ST_GeomFromText('POINT(19 1.5)')),
(4,  ST_GeomFromText('POINT(17 8)')),
(5,  ST_GeomFromText('POINT(6 10.5)')),
(6,  ST_GeomFromText('POINT(12 11)')),
(7,  ST_GeomFromText('POINT(14.5 6)')),
(8,  ST_GeomFromText('POINT(5 8.5)')),
(9,  ST_GeomFromText('POINT(4.5 6)')),
(10, ST_GeomFromText('POINT(3 4.5)')),
(11, ST_GeomFromText('POINT(14.5 2.5)')),
(12, ST_GeomFromText('POINT(7.5 6.5)')),
(13, ST_GeomFromText('POINT(17 11)')),
(14, ST_GeomFromText('POINT(7 4.5)')),
(15, ST_GeomFromText('POINT(10.5 2.5)'));

insert into forests values
(0, 'f1', ST_GeomFromText('POLYGON((1 1.5, 1.5 6, 4.5 7, 5.5 5, 4 3, 1 1.5), (2 5, 4 5.5, 3 6, 2 5), (1.5 3, 3.5 3.5, 3.5 4, 2.5 4, 1.5 3))')),
(1, 'f2', ST_GeomFromText('POLYGON((1 8.5, 4 8, 6 8.5, 6.5 9.5, 8 9.5, 9 11, 1.5 11, 1 8.5))')),
(2, 'f3', ST_GeomFromText('POLYGON((14.5 6.5, 14.5 11, 12 9, 14.5 6.5))')),
(3, 'f4', ST_GeomFromText('POLYGON((14.5 7.5, 19 7.5, 17 10, 14.5 10, 14.5 7.5))')),
(4, 'f5', ST_GeomFromText('POLYGON((8 2, 9.5 6.5, 11.5 6, 12.5 4, 12.5 2, 10.5 3, 8 2), (9.5 4.5, 10 4, 11 4, 11.5 5, 10.5 5.5, 9.5 4.5))'));
-- In interior
-- insert into forests values (5, 'f6', 'POLYGON((9.5 4.5, 10.5 5.5, 11 5, 10.5 4.5, 9.5 4.5))');

insert into roads values
(0, 'v1', ST_GeomFromText('LINESTRING(0 12, 0.5 11.5, 3.5 7.5)'),              'Elm Street'),
(1, 'v2', ST_GeomFromText('LINESTRING(20 9.5, 10.5 8, 7 7.5, 3.5 7.5)'),       'Peachtree'),
(2, 'v3', ST_GeomFromText('LINESTRING(7 12, 7 10, 7 7.5, 5 0)'),               'Sunset Boulevard'),
(3, 'v4', ST_GeomFromText('LINESTRING(6.5 5.5, 7.5 1, 15 1, 15 5.5, 20 5.5)'), 'One Way'),
(4, 'v5', ST_GeomFromText('LINESTRING(9.5 5, 10.5 8)'),                        'Forest Road'),
(5, 'v6', ST_GeomFromText('LINESTRING(15 5.5, 10.5 8, 10.5 12)'),              'Ocean Drive'),
(6, 'v7', ST_GeomFromText('LINESTRING(10.5 11.5, 7 11.5)'),                    'Park Lane');

