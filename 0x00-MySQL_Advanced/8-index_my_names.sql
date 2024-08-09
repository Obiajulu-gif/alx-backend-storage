-- 8-index_my_names.sql

-- create an index on the first letter of the `name` column
CREATE INDEX idx_name ON names(name(1));
