-- 創建一次性連結 token 表
create table if not exists link_tokens (
  token uuid primary key default gen_random_uuid(),
  line_user_id text not null,
  expires_at timestamptz not null,
  used boolean not null default false,
  created_at timestamptz default now()
);

-- 創建索引以提升查詢效能
create index if not exists link_tokens_line_user_id_idx on link_tokens(line_user_id);
create index if not exists link_tokens_expires_at_idx on link_tokens(expires_at);
create index if not exists link_tokens_used_idx on link_tokens(used);

-- 添加註釋說明
comment on table link_tokens is '一次性連結 token 表，用於 LINE 帳號與網站登入綁定';
comment on column link_tokens.token is '一次性 UUID token';
comment on column link_tokens.line_user_id is 'LINE 用戶 ID';
comment on column link_tokens.expires_at is 'token 過期時間';
comment on column link_tokens.used is '是否已使用';
comment on column link_tokens.created_at is '創建時間';
