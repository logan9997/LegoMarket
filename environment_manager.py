import os
import dotenv
from dotenv import load_dotenv

class Manager:
    load_dotenv()

    def get_database_credentails(conn_type:str) -> dict[str, str]:
        from LegoMarket.settings import PRODUCTION 
        '''
        Return dict for database connection credentials for either django 
        settings or for psycopg2.connect kwargs
        - conn_type: str - "psycopg2" / "settings"
        '''
        production_label = ''
        if PRODUCTION:
            production_label = 'PROD_'

        values = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']
        if conn_type == 'psycopg2':
<<<<<<< HEAD
            keys = ['dbname', 'user', 'password', 'host', 'port']
=======
            if DEVELOPMENT:
                return {
                    'dbname': os.environ.get('DB_NAME'),
                    'user': os.environ.get('DB_USER'),
                    'password': os.environ.get('DB_PASSWORD'),
                    'host': os.environ.get('DB_HOST'),
                    'port': os.environ.get('DB_PORT'),
                }
            else:
                return {
                    'dbname': os.environ.get('PROD_DB_NAME'),
                    'user': os.environ.get('PROD_DB_USER'),
                    'password': os.environ.get('PROD_DB_PASSWORD'),
                    'host': os.environ.get('PROD_DB_HOST'),
                    'port': os.environ.get('PROD_DB_PORT'),                
                }
        elif conn_type == 'settings':
            return {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('DB_NAME'),
                'USER': os.environ.get('DB_USER'),
                'PASSWORD': os.environ.get('DB_PASSWORD'),
                'HOST': os.environ.get('DB_HOST'),
                'PORT': os.environ.get('DB_PORT'),
            }
>>>>>>> parent of 8d1808fd (Revert ".")
        else:
            keys = ['NAME', 'USER', 'PASSWORD', 'HOST', 'PORT']

        credentials = {}
        for k, v in zip(keys, values):
            credentials[k] = os.environ.get(production_label + v)

        if conn_type == 'settings':
            credentials['ENGINE'] = 'django.db.backends.postgresql'
        return credentials
        
    def get_oauth_credentials() -> dict[str, str]:
        return {
            'CONSUMER_KEY': os.environ.get('CONSUMER_KEY'), 
            'CONSUMER_SECRET': os.environ.get('CONSUMER_SECRET'), 
            'TOKEN_VALUE': os.environ.get('TOKEN_VALUE'), 
            'TOKEN_SECRET': os.environ.get('TOKEN_SECRET')
        }
    
    def update_value(key, new_value):
        '''Update value of key inside .env file'''
        dotenv.set_key('.env', key, new_value)

    def get_value(key):
        '''Get value of key from .env file'''
        return os.environ.get(key)