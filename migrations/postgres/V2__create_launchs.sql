CREATE TABLE IF NOT EXISTS launches (
    id SERIAL PRIMARY KEY,
    data JSONB
);

CREATE INDEX launches_by_data ON launches (((data->>'epoch')::date));