import yaml
import os

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")


def load_config(config_path=None):
    path = config_path or DEFAULT_CONFIG_PATH
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in config file: {e}")
