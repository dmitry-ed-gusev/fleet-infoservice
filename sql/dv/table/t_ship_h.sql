CREATE TABLE DV.t_ship_h (
    ship_id    INTEGER NOT NULL,
    imo_num    VARCHAR(100),
    reg_num    VARCHAR(100),
    src_nm     VARCHAR(100) NOT NULL,
    load_dttm  TIMESTAMP
);

ALTER TABLE DV.t_ship_h ADD CONSTRAINT t_ship_h_pk PRIMARY KEY ( ship_id );
