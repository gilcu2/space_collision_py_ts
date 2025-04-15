CREATE TABLE IF NOT EXISTS reentries (
    id SERIAL PRIMARY KEY,
    data JSONB
);

CREATE INDEX reentries_by_date ON reentries (((data->>'epoch')::date));