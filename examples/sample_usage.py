from local_config_db.core import LocalConfig

config = LocalConfig()

config.set("env", {
    "mode": "test",
    "debug": True,
    "feature_flags": {
        "enable_all": False,
        "flags": ["a", "b", "c"]
    }
})

# Simulate update with toggle logic
env = config.get("env")

if env["feature_flags"]["enable_all"]:
    env["feature_flags"]["flags"] = ["a", "b", "c", "d", "e"]

config.set("env", env)
