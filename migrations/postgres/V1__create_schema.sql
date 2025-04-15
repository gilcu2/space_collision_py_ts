CREATE TABLE IF NOT EXISTS payloads (
    id SERIAL PRIMARY KEY,
    data JSONB
);

CREATE INDEX payload_by_data ON payloads USING GIN (data);