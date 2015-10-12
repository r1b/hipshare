import os

from jsonschema import validate

from hipshare.lib.util import die, merge_dicts, load_jsons

class Config(object):
    def __init__(self, strategy):
        default_options = {
            "shell": "/bin/bash",
            "ttl": 60
        }
        default_strategy = {
            "people": [],
            "rooms": []
        }

        config, schema = load_jsons('config.json', 'config.schema.json')
        validate(config, schema)

        # Get strategy
        try:
            config['strategy'] = config['strategies'][strategy]
        except KeyError:
            die("No such strategy: {}".format(strategy))

        # Get password from environment
        try:
            password_env = config['strategy']['password_env']
            config['strategy']['password'] = os.environ[password_env]
        except KeyError:
            die("Missing required environment variable: {}".format(password_env))

        self.__dict__.update(**{
            "options": merge_dicts(default_options, config['options']),
            "strategy": merge_dicts(default_strategy, config['strategy'])
        })
