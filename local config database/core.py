import json
import os
from copy import deepcopy
from difflib import unified_diff

CONFIG_DIR = os.path.expanduser("~/.local_config_db")

def _ensure_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)

def _path(namespace):
    _ensure_dir()
    return os.path.join(CONFIG_DIR, f"{namespace}.json")

def _load(namespace):
    try:
        with open(_path(namespace), 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def _save(namespace, data):
    with open(_path(namespace), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def _diff_dicts(old, new):
    old_str = json.dumps(old, indent=2, sort_keys=True).splitlines(keepends=True)
    new_str = json.dumps(new, indent=2, sort_keys=True).splitlines(keepends=True)
    return ''.join(unified_diff(old_str, new_str, fromfile='old', tofile='new'))

class LocalConfig:
    def __init__(self):
        self.cache = {}

    def get(self, namespace):
        if namespace not in self.cache:
            self.cache[namespace] = _load(namespace)
        return deepcopy(self.cache[namespace])

    def set(self, namespace, new_data, show_diff=True):
        old_data = self.get(namespace)
        if show_diff:
            print(_diff_dicts(old_data, new_data))
        self.cache[namespace] = new_data
        _save(namespace, new_data)

    def update(self, namespace, patch: dict):
        data = self.get(namespace)
        data.update(patch)
        self.set(namespace, data)

    def delete(self, namespace):
        if os.path.exists(_path(namespace)):
            os.remove(_path(namespace))
        self.cache.pop(namespace, None)
