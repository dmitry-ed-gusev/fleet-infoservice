CREATE TABLE DV.t_ship_hs (
    ship_id         INTEGER NOT NULL,
    valid_from      TIMESTAMP NOT NULL,
    valid_to        TIMESTAMP,
    flag            VARCHAR(100),
    main_name       VARCHAR(255),
    secondary_name  VARCHAR(255),
    home_port       VARCHAR(255),
    call_sign       VARCHAR(50),
    row_hash        VARCHAR(50) NOT NULL,
    load_dttm       TIMESTAMP NOT NULL
);

ALTER TABLE DV.t_ship_hs ADD CONSTRAINT t_ship_hs_pk PRIMARY KEY ( ship_id,
                                                                valid_from );