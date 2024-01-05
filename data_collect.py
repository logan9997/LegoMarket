from response import Response
from database import DB
from utils import item_type_convert, clean_html_codes, timer
from datetime import datetime
from config import DATE_FORMAT
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os

db = DB()
response = Response()

class DataCollect:

    def update_prices(self) -> None:
        items:list[dict] = db.get_item_ids_types(format=True)
        updated_ids = db.get_updated_prices()
        for item in items:
            item_id = item['item_id']

            if item_id in updated_ids:
                continue

            date = datetime.today().strftime(DATE_FORMAT)
            
            data = [item_id, date]
            conditions = ['N', 'U']

            print(f'\n{item_id}', end='\r')

            for condition in conditions:
                item_type = item_type_convert(item['item_type'])

                request_url = f'items/{item_type}/{item_id}/price?new_or_used={condition}'
                response_data = response.get_response(request_url)
                
                price = float(response_data.get('avg_price', -1))
                qty = int(response_data.get('total_quantity', -1))

                data.append(price)
                data.append(qty)

            db.insert_price(data)

    def update_items(self) -> None:
        item_types = ['M', 'S']
        stored_items = db.get_item_ids()
        for item_type in item_types:
            scraper = Scrape(item_type)
            scraper.scrape_items()
            item_ids = scraper.get_item_ids()

            for item_id in  item_ids:
                if item_id in stored_items:
                    continue

                sub_url = f'items/{item_type_convert(item_type)}/{item_id}'
                response_data = response.get_response(sub_url)

                item_name = response_data.get('name')
                item_name = clean_html_codes(item_name)
                year_released = response_data.get('year_released')

                data = [item_id, item_name, item_type, year_released]
                db.insert_item(data)
        scraper.driver.quit()    

    def download_images(self) -> None:
        items = db.get_item_ids_types(format=True)
        save_path = 'App/static/App/images'
        downloaded_images = os.listdir(save_path)
        for item in items:
            if item + '.png' in downloaded_images:
                continue
            
            item_type = item.get('item_type')
            item_id = item.get('item_id')
            
            image_url = f'https://img.bricklink.com/ItemImage/{item_type}N/0/{item_id}.png'
            image = requests.get(image_url).content
            full_path = os.path.join(save_path, item_id + '.png')
            
            with open(full_path, 'wb') as write_file:
                write_file.write(image) 

class Scrape:

    def __init__(self, item_type:str) -> None:
        self.driver = webdriver.Firefox()
        self.items_per_page = 50
        self.item_type = item_type
        self.item_ids = []

    def get_url(self, page) -> str:
        return f'https://www.bricklink.com/catalogList.asp?pg={page}&catString=65&catType={self.item_type}'

    def click_cookies(self) -> None:
        cookies_accept_button = self.driver.find_element(
            By.XPATH,
            '/html/body/div[3]/div/section/div/div[2]/div/section[1]/div[2]/div/button[2]'
        )
        cookies_accept_button.click()

    def scrape_items(self) -> None:
        url = self.get_url('1')
        self.driver.get(url)
        time.sleep(3)
        self.click_cookies()
        
        pages = self.driver.find_element(
            By.XPATH, 
            '/html/body/div[2]/center/table/tbody/tr/td/table/tbody/tr[3]/td/div/div[2]/div[2]/b[3]'
        ) 
        pages = int(pages.text)

        total_items = self.driver.find_element(
            By.XPATH,
            '/html/body/div[2]/center/table/tbody/tr/td/table/tbody/tr[3]/td/div/div[2]/div[2]/b[1]'
        )
        total_items = int(total_items.text)
        
        for page in range(pages+1):
            items = 50
            if page == pages:
                items = total_items % self.items_per_page
            for item in range(items):
                item_container = self.driver.find_element(
                    By.XPATH,
                    f'/html/body/div[2]/center/table/tbody/tr/td/div/form/table[1]/tbody/tr/td/table/tbody/tr[{item+2}]'
                )
                item_id = item_container.find_element(By.TAG_NAME, 'a').text
                self.item_ids.append(item_id)

            url = self.get_url(page+1)
            self.driver.get(url)

    def get_item_ids(self) -> list[str]:
        return self.item_ids
            

@timer
def main():
    valid_methods = [method for method in dir(DataCollect) if method[0] != '_']
    method = input('Call a method: ')

    while True:
        if method in valid_methods:
            getattr(DataCollect(), method)()
            break
 
        valid_methods_formatted = "\n".join(valid_methods)
        print(f'Invalid method, Valid Methods below;\n{valid_methods_formatted}')

        method = input('\nCall a method: ')

if __name__ == '__main__':
    main()