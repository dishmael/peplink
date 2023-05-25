drop table if exists tmobile.status;

create table if not exists status (
    id mediumint not null auto_increment,
    network varchar(6),
    name varchar(64),
    level smallint,
    rssi decimal(5,2),
    sinr decimal(5,2),
    rsrp decimal(5,2),
    rsrq decimal(5,2),
    created timestamp NOT NULL default current_timestamp,
    updated timestamp NOT NULL default now() on update now(),
    primary key (id)
);
