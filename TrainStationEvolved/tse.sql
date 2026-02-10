create database TSE;
use TSE;

drop database TSE;

show tables;

select * from user;
select * from typeloco;
select * from locomotive;
select * from wagon;
select * from passengerwagon;
select * from cargowagon;

drop table locomotive, userloco, train;
drop table wagon, wagonuser;
drop table user;

update user set gold = 1200 where nickname = 'Meow Tarifa';