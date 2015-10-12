import logging.config
from hipshare.lib.util import load_json

logging.config.dictConfig(load_json('config.log.json'))
