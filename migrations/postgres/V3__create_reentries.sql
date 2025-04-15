CREATE TABLE IF NOT EXISTS reentries (
    id SERIAL PRIMARY KEY,
    data JSONB
);

CREATE INDEX reentries_by_data ON reentries USING GIN (data);