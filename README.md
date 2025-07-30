# Local Config DB

A lightweight, dependency-free Python library to manage structured config files locally with human-readable diffs.

## Features

- Namespace-based config management (e.g., `env`, `user`, etc.)
- JSON storage in `~/.local_config_db`
- Unified diffs on config updates
- Zero dependencies

## Usage

```python
from local_config_db.core import LocalConfig

cfg = LocalConfig()
cfg.set("env", {"debug": True})
print(cfg.get("env"))
cfg.update("env", {"debug": False})
```

## License

MIT

## Command Line Interface

```bash
# Show config
python cli.py get env

# Replace config with contents of file.json (shows diff by default)
python cli.py set env file.json

# Show diff between current config and file
python cli.py diff env file.json

# Update config by merging in a JSON patch (with confirmation)
python cli.py update env patch.json

# Delete a config namespace (with confirmation)
python cli.py delete env
```
