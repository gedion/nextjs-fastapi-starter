create extension if not exists btree_gin;

create index concurrently if not exists thread_status_idx on thread(status, created_at desc);
create index concurrently if not exists thread_metadata_idx on thread using gin(metadata jsonb_path_ops);
create index concurrently if not exists run_metadata_idx on run using gin(thread_id, metadata jsonb_path_ops);
create index concurrently if not exists assistant_metadata_idx on assistant using gin(metadata jsonb_path_ops);
create index concurrently if not exists checkpoints_checkpoint_id_idx on checkpoints(thread_id, checkpoint_id desc);
