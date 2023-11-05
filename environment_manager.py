import os
from dotenv import load_dotenv

class Manager:
    load_dotenv()

    def get_database_credentails(conn_type:str):
        if conn_type == 'postgres':
            return {
                'dbname': os.environ.get('DB_NAME'),
                'user': os.environ.get('DB_USER'),
                'password': os.environ.get('DB_USER'),
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
            raise Exception(f'Invalid conn_type - ({conn_type}). conn_type must equal "postgres" or "settings"') 