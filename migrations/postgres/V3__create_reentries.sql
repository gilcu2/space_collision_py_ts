CREATE TABLE IF NOT EXISTS reentries (
    id SERIAL PRIMARY KEY,
    epoch DATE,
    data JSONB
);

CREATE INDEX reentries_by_date ON reentries (epoch);