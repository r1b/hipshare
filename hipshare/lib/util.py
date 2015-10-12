import json
import logging
import sys

log = logging.getLogger(__name__)

def die(s):
    log.error(s)
    sys.exit(-1)

def load_json(path):
    try:
        fp = open(path)
    except OSError as err:
        die("Could not open {}: {}".format(path, str(err)))

    try:
        value = json.load(fp)
    except ValueError as err:
        die("Invalid JSON in {}: {}".format(path, str(err)))

    return value

def load_jsons(*paths):
    return [load_json(path) for path in paths]

def merge_dicts(a, b):
    c = a.copy()
    c.update(b)
    return c

def usage():
    log.error("usage: hipshare <strategy>")
    sys.exit(-1)
