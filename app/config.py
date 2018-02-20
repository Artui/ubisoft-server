from envparse import env
import os

HOST = env.str('HOST', default='0.0.0.0')

PORT = env.int('PORT', default=8080)

DEBUG = env.bool('DEBUG', default=True)

REDIS_HOST = env.str('REDIS_HOST', default='0.0.0.0')

REDIS_PORT = env.int('REDIS_PORT', default=6379)

REDIS_DB = env.int('REDIS_DB', default=0)

BASE_DIR = os.path.dirname(__file__)

FIXTURE_DIR_NAME = 'tools'

FIXTURES_PATH = os.path.join(BASE_DIR, FIXTURE_DIR_NAME)

CLEAR_DB = env.bool('CLEAR_DB', default=True)

