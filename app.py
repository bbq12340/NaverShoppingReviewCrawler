from ScrapeItem import NaverShoppingScraper
import json, time
import pandas as pd
from datetime import datetime, timedelta
from tqdm import trange

class Application():
    def __init__(self, query):
        self.query = query
        self.app = NaverShoppingScraper()
        self.items = self.app.scraped_items
        self.now = datetime.now()
        self.date_before_3months = self.now - timedelta(days=90)
    
    def start_process(self):
        # scrape 3 pages sorted by 'review'
        # sort --> ScrapeItem.py
        for i in range(1,4):
            url = self.app.get_query_link(i, self.query)
            json_data = self.app.get_query_json(url)
            self.app.get_item_info(json_data)
        result = self.filter_items(self.items)
        if len(result) == 0:
            with open('output/none_keyword.txt', 'a') as f:
                f.write(self.query+'\n')
        else:
            df = pd.DataFrame(data=result)
            df.to_csv('output/input.csv', index=False, mode='a', header=False, encoding='utf-8-sig')
        return len(result)
    
    def filter_items(self, items):
        filtered = []
        for item in items:
            # condition
            if item['리뷰수'] >= 1000 and 'https://smartstore.naver.com/' in item['링크'] and item['날짜'] > self.date_before_3months.date():
                filtered.append({'names': item['상품명'], 'link': item['링크']})
        try:
            filtered = filtered[:7]
        except IndexError:
            pass
        return filtered

