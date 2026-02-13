create database TSE;
use TSE;

drop database TSE;

show tables;

select * from user;
select * from typeloco;
select * from locomotive;
select * from wagon;
select * from wagonuser;
select * from passengerwagon;
select * from cargowagon;
select * from material;
select * from rawmaterial;
select * from facmaterial;
select * from material;
select * from MaterialUser;

drop table locomotive, userloco, train;
drop table wagon, wagonuser;
drop table user;

update user set gold = 1200 where nickname = 'Meow Tarifa';