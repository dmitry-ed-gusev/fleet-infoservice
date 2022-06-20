/*
    Scraper SQLite DB init sql script.

    Created:  Dmitrii Gusev, 20.06.2022
    Modified: 
*/

-- scraper executions table
CREATE TABLE IF NOT EXISTS scraper_executions (
    id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    start_timestamp TEXT NOT NULL,
    end_timestamp   TEXT NOT NULL,
    duration        INTEGER NOT NULL
);
