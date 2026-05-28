# https://docs.python.org/3/library/logging.html#logrecord-attributes

import json
import logging.config

logger = logging.getLogger("smartEdge")

def setup_logging(config_path):
    config_file = open(config_path, 'r')
    with open(config_path, 'r') as config_file:
        config_dict = json.load(config_file)
        
    logging.config.dictConfig(config_dict)