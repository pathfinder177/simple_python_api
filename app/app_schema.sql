DROP TABLE IF EXISTS configs;

CREATE TABLE configs (
  name     TEXT PRIMARY KEY,
  metadata TEXT NOT NULL
);