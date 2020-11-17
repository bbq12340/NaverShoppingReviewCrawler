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
        self.result = []
        self.now = datetime.now()
        self.date_before_3months = self.now - timedelta(days=90)
    
    def start_process(self):
        items = []
        for i in range(1,4):
            url = self.app.get_query_link(i, self.query, sort_option="rel")
            json_data = self.app.get_query_json(url)
            items.extend(self.app.get_item_info(json_data))
        self.result.extend(self.filter_items(items, 1))
        items=[]
        p = 1
        while True:
            url = self.app.get_query_link(p, self.query, sort_option="review")
            json_data = self.app.get_query_json(url)
            items.extend(self.app.get_item_info(json_data))
            p = p + 1
            if items[-1]['리뷰수'] <=500:
                break
        self.result.extend(self.filter_items(items, 2))
        self.result.extend(self.filter_items(items, 3))
        if len(self.result) == 0:
            with open('output/none_keyword.txt', 'a') as f:
                f.write(self.query+'\n')
        else:
            df = pd.DataFrame(data=self.result)
            df = df.drop_duplicates(subset=['keyword', 'names']) # 중복제거
            df.to_csv('output/input.csv', index=False, mode='a', header=False, encoding='utf-8-sig')
        time.sleep(self.delay)
        return len(df.index)
    
    def filter_items(self, items, filter_option):
        filtered = []
        if filter_option == 1:
            for item in items:
                # condition: 네이버 랭킹순 3페이지, 리뷰수 >= 2000
                if 'smartstore.naver.com/' in item['링크'] and item['리뷰수'] >= 2000:
                    filtered.append({'keyword':self.query, 'names': item['쇼핑몰명'], 'link': item['링크']})
            try:
                filtered = filtered[:5]
            except IndexError:
                pass

        elif filter_option == 2:
            for item in items:
                # condition: 리뷰순 페이지에서 리뷰수 >=500, 최근 3개월.
                if 'smartstore.naver.com/' in item['링크'] and item['리뷰수'] >= 500 and item['날짜'] > self.date_before_3months.date():
                    filtered.append({'keyword':self.query, 'names': item['쇼핑몰명'], 'link': item['링크']})
            try:
                filtered = filtered[:2]
            except IndexError:
                pass

        else:
            for item in items:
                # condition: 리뷰순 페이지에서 제일 많은 리뷰 2개.
                if 'smartstore.naver.com/' in item['링크']:
                    filtered.append({'keyword':self.query, 'names': item['쇼핑몰명'], 'link': item['링크']})
                    if len(filtered) >= 2:
                        break
        return filtered

