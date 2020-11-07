import requests, json, urllib, random, string
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from datetime import datetime
class NaverShoppingScraper:
    def __init__(self):
        self.API_url = "https://shopping.naver.com/search/all"
        self.user_agent = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
        self.scraped_items = []
        self.scraped_malls = []

    def get_query_link(self, page, query):
        payloads = {
            "sort": "review",
            "origQuery": query,
            "pagingIndex": page,
            "pagingSize": 80,
            "viewType": "list",
            "productSet": "total",
            "frm": "NVSHATC",
            "query": query
        }
        r = requests.get(self.API_url, params=payloads, headers=self.user_agent)
        return r.url

    def get_query_json(self, link):
        r = requests.get(link, headers=self.user_agent)
        soup = BeautifulSoup(r.text,'html.parser').find('script', {'id': "__NEXT_DATA__"}).string
        json_data = json.loads(soup)
        return json_data
    
    def get_item_info(self, data):
        product_list = data['props']['pageProps']['initialState']['products']['list']
        for product in product_list:
            item = product['item']
            output = {
                '상품명': item['productName'],
                '리뷰수': int(item['reviewCount']),
                '링크': item['mallProductUrl'],
                '날짜': datetime.strptime(item['openDate'][:-6], '%Y%m%d').date()
            }
            self.scraped_items.append(output)
        return self.scraped_items
    
    def get_mall_info(self, data):
        product_list = data['props']['pageProps']['initialState']['products']['list']
        for product in product_list:
            item = product['item']
            if 'mallInfoCache' in item:
                output = {
                    '쇼핑몰명': item['mallInfoCache']['name'],
                    '사업자등록번호': item['mallInfoCache']['businessNo'],
                    '링크': item['mallPcUrl'],
                    '상품수': item['mallInfoCache']['prodCnt'],
                    '주소': item['mallInfoCache']['bizplBaseAddr'],
                    '통신판매업신고': item['mallInfoCache']['onmktRegisterNo']
                }
                self.scraped_malls.append(output)
            else:
                pass
        return self.scraped_malls

    def get_images(self, products_list):
        for product in products_list:
            img = product['이미지링크']
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H_%M_%S")
            random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            product['이미지링크'] = f"{current_time}-{random_code}"
            try:
                urllib.request.urlretrieve(img, f'images/{product["이미지링크"]}.jpg')
            except HTTPError:
                with open('bug_report.txt' ,'a', encoding='utf-8') as f:
                    f.write(f'{product["상품명"]}\t이미지 에러\n')