from local_config_db.core import LocalConfig

test_config = {
    "mode": "production",
    "debug": False,
    "version": "1.2.3",
    "feature_flags": {
        "enable_all": True,
        "flags": ["flag_a", "flag_b", "flag_c", "flag_d", "flag_e"]
    },
    "security": {
        "2fa_required": True,
        "allowed_ips": [
            "192.168.1.0/24",
            "10.0.0.0/8"
        ],
        "encryption": "AES256"
    },
    "ui_preferences": {
        "theme": "dark",
        "font_size": 14,
        "show_help_tooltips": False
    },
    "module_config": {
        "mod_a": {"enabled": True, "threshold": 0.75},
        "mod_b": {"enabled": False, "threshold": 0.50},
        "mod_c": {"enabled": True, "threshold": 0.95}
    }
}

config = LocalConfig()
config.set("env", test_config)
