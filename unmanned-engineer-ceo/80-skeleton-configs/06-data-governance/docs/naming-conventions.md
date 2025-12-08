# Data Naming Conventions

## 資料庫命名

### 表名 (Table Names)
- **規則**: 複數形式,snake_case
- **範例**: `users`, `api_keys`, `project_members`

### 欄位名 (Column Names)
- **規則**: 單數形式,snake_case
- **範例**: `user_id`, `created_at`, `display_name`

### 外鍵 (Foreign Keys)
- **規則**: `<referenced_table_singular>_id`
- **範例**: `tenant_id`, `project_id`, `user_id`

### 索引 (Indexes)
- **規則**: `idx_<table>_<columns>`
- **範例**: `idx_users_email`, `idx_projects_tenant_id_status`

## Event Schema 命名

### Event Types
- **規則**: `<entity>.<action>` (過去式)
- **範例**: 
  - `user.created`
  - `project.updated`
  - `deployment.completed`
  - `agent.deleted`

### Event 欄位