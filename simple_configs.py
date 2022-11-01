from os import environ

class Config(object):
    TG_API_ID = int(environ['API_ID'])
    TG_API_HASH = environ['API_HASH']
    TG_BOT_TOKEN = environ['BOT_TOKEN']

class Bots(object):
    BOT_ID = int(environ.get('BOT_ID', None))
    BOT_NAME = environ.get('BOT_NAME', 'Lucifer')
    BOT_USERNAME = environ.get('BOT_USERNAME', 'Midukki_RoboT')
