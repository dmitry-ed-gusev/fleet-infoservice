create table dv.t_ship_hs (
    ship_id         integer not null,
    valid_from      timestamp not null,
    valid_to        timestamp,
    flag            varchar(100),
    main_name       varchar(255),
    secondary_name  varchar(255),
    home_port       varchar(255),
    call_sign       varchar(50),
    row_hash        varchar(50) not null,
    load_dttm       timestamp not null
);

alter table dv.t_ship_hs add constraint t_ship_hs_pk primary key ( ship_id,
                                                                valid_from );