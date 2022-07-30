/*
    Scraper SQLite DB schema init sql script.

    Created:  Dmitrii Gusev, 20.06.2022
    Modified: Dmitrii Gusev, 30.07.2022
*/

-- scraper executions table
CREATE TABLE IF NOT EXISTS scraper_executions (
    id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    start_timestamp TEXT NOT NULL,
    end_timestamp   TEXT NOT NULL,
    duration        REAL NOT NULL,
    parameters      TEXT NOT NULL
);
