create table menber(
    menberID       int             auto_increment,
    first_name     nvarchar(20)    NOT NULL,
    family_name    nvarchar(20)    NOT NULL,
    pass_word       varchar(30)    NOT NULL,
    primary key(menberID)
);

create table kinds(
    kindID           int,
    kind_name        nvarchar(50)     NOT NULL,
    primary key(kindID)
);

create table schedules(
    scheduleID      int              auto_increment,
    kindID          int              NOT NULL,
    menberID        int              NOT NULL,
    schedule_name    nvarchar(100)   NOT NULL,
    primary key(scheduleID),
    foreign key(kindID) references kinds(kindID),
    foreign key(menberID) references menber(menberID)
);



create table calender(
    date_ID       int     auto_increment,
    days          date    NOT NULL,
    scheduleID    int     NOT NULL,
    primary key(date_ID),
    foreign key(scheduleID) references schedules(scheduleID)
); 

insert into kinds(kindID, kind_name) values (1, '学校');
insert into kinds(kindID, kind_name) values (2, '試験');
insert into kinds(kindID, kind_name) values (3, '課題');
insert into kinds(kindID, kind_name) values (4, '行事');
insert into kinds(kindID, kind_name) values (5, '就活');
insert into kinds(kindID, kind_name) values (6, 'アルバイト');
insert into kinds(kindID, kind_name) values (7, '旅行');

