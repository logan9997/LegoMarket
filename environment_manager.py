import os
from dotenv import load_dotenv

class Manager:
    load_dotenv()

    def get_database_credentails(conn_type:str):
        '''
        Return dict for database connection credentials for either django 
        settings or for psycopg2.connect kwargs
        - conn_type: str - "psycopg2" / "settings"
        '''
        if conn_type == 'psycopg2':
            return {
                'dbname': os.environ.get('DB_NAME'),
                'user': os.environ.get('DB_USER'),
                'password': os.environ.get('DB_PASSWORD'),
                'host': os.environ.get('DB_HOST'),
                'port': os.environ.get('DB_PORT'),
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
        else:
            raise Exception(f'Invalid conn_type - ({conn_type}). conn_type must equal "psycopg2" or "settings"') 