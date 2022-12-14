from os import getenv

TESTING = True
ENVIRONMENT = getenv('ENV')
DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')

if getenv('GAE_ENV') == 'standard':
    SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///db.sqlite3'
else:
    SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///db.sqlite3'
    '''
    SQLALCHEMY_DTABASE_URL = f'mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@localhost/pythonista
    SQLALCHEMY_DTABASE_URL = f'postgresql+aiopg://{DB_USER}:{DB_PASSWORD}@localhost/py261-2207'
    '''