# https://docs.python.org/3/library/logging.html#logrecord-attributes

import json
import logging.config
import os

logger = logging.getLogger("smartEdge")

def setup_logging(config_path, log_path=None, level=None):
    with open(config_path, 'r') as config_file:
        config_dict = json.load(config_file)

    if log_path:
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        for handler in config_dict.get("handlers", {}).values():
            if "filename" in handler:
                handler["filename"] = log_path

    if level:
        # Override the level in the main logger
        if "loggers" in config_dict and "smartEdge" in config_dict["loggers"]:
            config_dict["loggers"]["smartEdge"]["level"] = level
        # Also override root or specific handlers if needed
        for handler in config_dict.get("handlers", {}).values():
            if "level" in handler:
                handler["level"] = level

    logging.config.dictConfig(config_dict)
    return logger