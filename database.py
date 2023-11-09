import psycopg2 
from environment_manager import Manager

class DB:

    def __init__(self) -> None:
        psql_credentials = Manager.get_database_credentails('psycopg2')
        self.conn = psycopg2.connect(**psql_credentials)
        self.cursor = self.conn.cursor()

    def select(self, sql, data=(), fetchone=False, flat=False, format=False):
        self.cursor.execute(sql, data)
        result = self.cursor.fetchall()
        
        if fetchone:
            result = self.cursor.fetchone() 
        
        if flat:
            return [col[0] for col in result]
        
        if format:
            result = [
                {col[0]: row[i] for i, col in enumerate(self.cursor.description)} 
                for row in result
            ]

        return result 
    
    def insert(self, sql, data=()):
        self.cursor.execute(sql, data)
        self.conn.commit()

    def get_item_ids_types(self, **kwargs):
        sql = '''
        SELECT item_id, item_type
        FROM "App_item";
        '''
        return self.select(sql,** kwargs)
    
    def insert_price(self, data):
        sql = '''
        INSERT INTO "App_price"(item_id, date, price_new, qty_new, price_used, qty_used)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (item_id, date) DO NOTHING
        '''
        self.insert(sql, data)

if __name__ == '__main__':
    a = DB().get_item_ids_types()
    print(a)
