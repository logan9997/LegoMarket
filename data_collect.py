from response import Response
from database import DB
from utils import item_type_convert
from datetime import datetime
from config import DATE_FORMAT

db = DB()
response = Response()

class DataCollect:

    def __init__(self) -> None:
        pass

    def update_prices(self):
        items:list[dict] = db.get_item_ids_types(format=True)
        for item in items:
            item_id = item['item_id']
            date = datetime.today().strftime(DATE_FORMAT)
            
            data = [item_id, date]
            conditions = ['N', 'U']

            for condition in conditions:
                item_type = item_type_convert(item['item_type'])

                request_url = f'items/{item_type}/{item_id}/price?new_or_used={condition}'
                response_data = response.get_response(request_url)
                
                price = float(response_data.get('avg_price', -1))
                qty = int(response_data.get('total_quantity', -1))

                data.append(price)
                data.append(qty)

            print(data)
            db.insert_price(data)

if __name__ == '__main__':
    data_collect = DataCollect()
    valid_methods = [method for method in dir(data_collect) if method[0] != '_']

    method = input('Call a method: ')
    while True:
        if method in valid_methods:
            getattr(data_collect, method)()
            break
 
        valid_methods_formatted = "\n".join(valid_methods)
        print(f'Invalid method, Valid Methods below;\n{valid_methods_formatted}')

        method = input('\nCall a method: ')
