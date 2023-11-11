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
    
    def insert(self, sql, data=()) -> None:
        self.cursor.execute(sql, data)
        self.conn.commit()

    def update(self, sql, data=()) -> None:
        self.cursor.execute(sql, data)
        self.conn.commit()

    def get_item_ids_types(self, **kwargs):
        '''SELECT item_id, item_type'''
        sql = '''
        SELECT item_id, item_type
        FROM "App_item";
        '''
        return self.select(sql,** kwargs)
    
    def get_item_ids(self):
        '''SELECT item_id'''
        sql = '''
        SELECT item_id
        FROM "App_item"
        '''
        return self.select(sql, flat=True)
    
    def insert_price(self, data) -> None:
        sql = '''
        INSERT INTO "App_price"(item_id, date, price_new, qty_new, price_used, qty_used)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (item_id, date) DO NOTHING
        '''
        self.insert(sql, data)

    def insert_item(self, data) -> None:
        sql = '''
        INSERT INTO "App_item"
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (item_id) DO NOTHING
        '''
        self.insert(sql, data)

if __name__ == '__main__':
    pass
