import psycopg2 
from environment_manager import Manager

class DB:

    def __init__(self) -> None:
        psql_credentials = Manager.get_database_credentails('psycopg2')
        self.conn = psycopg2.connect(**psql_credentials)
        self.cursor = self.conn.cursor()

    def select(self, sql, data=(), fetchone=False, flat=False):
        self.cursor.execute(sql, data)
        if fetchone:
            return self.cursor.fetchone() 
        
        result = self.cursor.fetchall()
        if flat:
            return [col[0] for col in result]
        return result 


    def test(self):
        sql = '''
        select * from "App_item"
        where item_name = %s 
        '''
        data = ('Anakin',)
        return self.select(sql, data=data)


if __name__ == '__main__':
    test = DB().test()
    print(test)
