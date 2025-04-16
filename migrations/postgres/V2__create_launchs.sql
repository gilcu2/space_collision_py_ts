CREATE TABLE IF NOT EXISTS launches (
    id SERIAL PRIMARY KEY,
    epoch DATE,
    data JSONB
);

CREATE INDEX launches_by_data ON launches (epoch);