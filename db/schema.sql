-- NEXUS Agent X — SQLite + sqlite-vec DDL (ULTRA spec §20)
-- WAL mode for concurrent orchestrator + agents
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

CREATE TABLE IF NOT EXISTS conversations (
  id TEXT PRIMARY KEY,
  project_id TEXT REFERENCES projects(id),
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

CREATE TABLE IF NOT EXISTS messages (
  id TEXT PRIMARY KEY,
  conv_id TEXT REFERENCES conversations(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('system','user','assistant','tool')),
  content TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

CREATE TABLE IF NOT EXISTS projects (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  goals TEXT,
  architecture TEXT,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

CREATE TABLE IF NOT EXISTS tasks (
  id TEXT PRIMARY KEY,
  project_id TEXT REFERENCES projects(id),
  title TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('PENDING','READY','RUNNING','BLOCKED','VERIFYING','DONE','FAILED')),
  priority INT NOT NULL DEFAULT 5,
  deps TEXT, -- JSON array of task ids
  agent TEXT,
  tools TEXT, -- JSON array
  estimate_minutes INT,
  risk TEXT CHECK (risk IN ('LOW','MED','HIGH')),
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

CREATE TABLE IF NOT EXISTS agents (
  id TEXT PRIMARY KEY,
  role TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('IDLE','THINKING','PLANNING','EXECUTING','OBSERVING','VERIFYING','LEARNING','COMPLETE','ERROR')),
  current_task TEXT REFERENCES tasks(id)
);

CREATE TABLE IF NOT EXISTS tools (
  name TEXT PRIMARY KEY,
  manifest TEXT NOT NULL -- JSON
);

CREATE TABLE IF NOT EXISTS skills (
  name TEXT PRIMARY KEY,
  version TEXT NOT NULL,
  manifest TEXT NOT NULL, -- YAML/JSON
  benchmarks TEXT -- JSON
);

CREATE TABLE IF NOT EXISTS memories (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL CHECK (type IN ('working','episodic','semantic','procedural','preference','project')),
  project_id TEXT REFERENCES projects(id),
  content TEXT NOT NULL,
  embedding BLOB,
  importance REAL NOT NULL DEFAULT 0.5,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
  version INT NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS events (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL, -- TASK_CREATED, TOOL_CALLED, etc.
  payload TEXT NOT NULL, -- JSON
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

CREATE TABLE IF NOT EXISTS permissions (
  capability TEXT PRIMARY KEY, -- READ_FILES, WRITE_FILES, etc.
  policy TEXT NOT NULL CHECK (policy IN ('allow','deny','ask'))
);

CREATE TABLE IF NOT EXISTS audit_logs (
  id TEXT PRIMARY KEY,
  timestamp TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
  agent TEXT,
  task_id TEXT REFERENCES tasks(id),
  tool TEXT,
  args_hash TEXT,
  result TEXT,
  permission TEXT,
  verification TEXT
);

-- Vector index (sqlite-vec). Requires sqlite-vec extension.
-- CREATE VIRTUAL TABLE IF NOT EXISTS memories_vec USING vec0(embedding float[768]);

-- Default permissions (ask for HIGH-risk, allow LOW)
INSERT OR IGNORE INTO permissions(capability, policy) VALUES
  ('READ_FILES','allow'),
  ('WRITE_FILES','ask'),
  ('DELETE_FILES','ask'),
  ('EXECUTE_COMMANDS','ask'),
  ('NETWORK_ACCESS','ask'),
  ('BROWSER_ACCESS','ask'),
  ('SYSTEM_CONTROL','ask'),
  ('INSTALL_SOFTWARE','ask'),
  ('ACCESS_SECRETS','ask');
