from os import environ

class Config(object):
    TG_API_ID = int(environ['API_ID'])
    TG_API_HASH = environ['API_HASH']
    TG_BOT_TOKEN = environ['BOT_TOKEN']
