from ScrapeItem import NaverShoppingScraper
import json, time
import pandas as pd
from datetime import datetime, timedelta
from tqdm import trange

class Application():
    def __init__(self, query, delay):
        self.query = query
        self.delay = delay
        self.app = NaverShoppingScraper()
        self.items = self.app.scraped_items
        self.now = datetime.now()
        self.date_before_3months = self.now - timedelta(days=90)
    
    def start_process(self):
        p = 1
        while True:
            url = self.app.get_query_link(p, self.query, sort_option="review")
            json_data = self.app.get_query_json(url)
            self.app.get_item_info(json_data)
            p = p + 1
            if self.items[-1]['리뷰수'] <=500:
                break
        result = self.filter_items(self.items)
        if len(result) == 0:
            with open('output/none_keyword.txt', 'a') as f:
                f.write(self.query+'\n')
        else:
            df = pd.DataFrame(data=result)
            df.to_csv('output/input.csv', index=False, mode='a', header=False, encoding='utf-8-sig')
        time.sleep(self.delay)
        return len(result)
    
    def filter_items(self, items):
        filtered = []
        for item in items:
            # condition
            if 'https://smartstore.naver.com/' in item['링크']:
                if len(filtered) <=7 and item['리뷰수'] >= 1000:
                    filtered.append({'keyword':self.query, 'names': item['쇼핑몰명'], 'link': item['링크']})
                elif item['리뷰수'] >= 500 and item['날짜'] > self.date_before_3months.date():
                    filtered.append({'keyword':self.query, 'names': item['쇼핑몰명'], 'link': item['링크']})
        # try:
        #     filtered = filtered[:7]
        # except IndexError:
        #     pass
        return filtered

