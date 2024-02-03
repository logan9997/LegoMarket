import os
import dotenv
from dotenv import load_dotenv

class Manager:
    load_dotenv()

    def get_database_credentails(conn_type:str) -> dict[str, str]:
        from LegoMarket.settings import DEVELOPMENT 
        '''
        Return dict for database connection credentials for either django 
        settings or for psycopg2.connect kwargs
        - conn_type: str - "psycopg2" / "settings"
        '''
        if conn_type == 'psycopg2':
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
                    'user': os.environ.get('PROD_DB_NAME'),
                    'password': os.environ.get('PROD_DB_NAME'),
                    'host': os.environ.get('PROD_DB_NAME'),
                    'port': os.environ.get('PROD_DB_NAME'),                
                }
        elif conn_type == 'settings':
            return {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('PROD_DB_NAME'),
                'USER': os.environ.get('PROD_DB_USER'),
                'PASSWORD': os.environ.get('PROD_DB_PASSWORD'),
                'HOST': os.environ.get('PROD_DB_HOST'),
                'PORT': os.environ.get('PROD_DB_PORT'),
            }
        else:
            raise Exception(f'Invalid conn_type - ({conn_type}). conn_type must equal "psycopg2" or "settings"') 
        
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