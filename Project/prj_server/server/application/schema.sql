CREATE TABLE IF NOT EXISTS machine_stats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  api_key TEXT NOT NULL,
  mac_address TEXT NOT NULL,
  machine_name TEXT NOT NULL,
  field INTEGER NOT NULL,
  data_point INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
  
);
r