ALTER TABLE cron
    ADD COLUMN metadata JSONB NOT NULL DEFAULT '{}';
