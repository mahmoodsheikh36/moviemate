import json

def load_config():
    with open('config.json') as config_file:
        config_dict = json.loads(config_file.read())
        Config.omdb_apikey = config_dict['omdb_apikey']

class Config:
    omdb_apikey = None

load_config()
