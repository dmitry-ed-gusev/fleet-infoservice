create table dv.t_ship_h (
    ship_id    integer not null,
    imo_num    varchar(100),
    reg_num    varchar(100),
    src_nm     varchar(100) not null,
    load_dttm  timestamp
);

alter table dv.t_ship_h add constraint t_ship_h_pk primary key ( ship_id );
