CREATE EXTENSION IF NOT EXISTS ltree;


ALTER TABLE store
    ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP;

-- For faster listing of namespaces & lookups by namespace with prefix/suffix matching
CREATE INDEX concurrently IF NOT EXISTS store_prefix_idx ON store USING btree (prefix text_pattern_ops);