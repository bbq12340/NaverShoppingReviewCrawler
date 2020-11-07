import requests, bs4
from bs4 import BeautifulSoup
import json, re

class SmartStoreReviewScraper:

    def __init__(self):
        self.user_agent = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        self.API_url = 'https://smartstore.naver.com/i/v1/reviews/paged-reviews'
        self.scraped_reviews = []
        # self.store_data = self.get_store_data(link) #스토어 정보 --- 스토어 번호, 물품 번호
        # self.json_review = self.get_review_json(self.store_data['merchant_no'], self.store_data['product_no'], 1) #리뷰페이지 정보
        # self.total_pages = self.get_review_data(self.json_review)['totalPages'] #총 페이지
        # self.total_elements = self.get_review_data(self.json_review)['totalElements'] #총 아이템

    def get_store_data(self, link):
        r = requests.get(link, headers=self.user_agent)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text,'html.parser').find('body').find('script').string[27:]
            json_dict=json.loads(str(soup))
            merchant_no = json_dict['smartStore']['channel']['payReferenceKey']
            product_no = json_dict['product']['A']['productNo']
            data = {
                'merchant_no': merchant_no,
                'product_no': product_no
            }
        else:
            print("네트워크 에러 발생-------------------스토어 링크 확인 필요")
            with open('output/bug_report.txt', 'a') as f:
                f.write(f"스토어 사이트 에러\t{link}\n")
        return data
    
    def get_review_json(self, merchant_no, product_no, page):
        payload = {
            'page': page,
            'pageSize': '20',
            'merchantNo': merchant_no,
            'originProductNo': product_no,
            'sortType': 'REVIEW_RANKING'
        }
        r = requests.get(self.API_url, params=payload, headers=self.user_agent)
        if r.status_code == 200:
            json = r.json(encoding='utf-8')
        else:
            print(f"네트워크 에러 발생-------------------페이지 {page} 확인 필요.")
            with open('output/bug_report.txt', 'a') as f:
                f.write(f"리뷰 페이지 에러\t{r.url}\n")
        return json
    
    def get_review_content(self, review):
        content = review['contents']
        return content
    
    def get_review_data(self, review):
        total_pages = review['totalPages']
        total_elements = review['totalElements']
        data = {
            'totalPages': total_pages,
            'totalElements': total_elements
        }
        return data
    
    def scrape_review_contents(self, REVIEWS, review_content):
        for review in review_content:
            data = {
                    '평점': review['reviewScore'], #평점
                    '아이디': review['writerMemberId'], #아이디
                    '구매날짜': review['createDate'].replace('T', ' ').split('.')[0], #구매날짜   
                    '리뷰내용': review['reviewContent'].replace(',',' ').replace('~',' ').replace('\n',' ') #리뷰내용
                }
            if 'productOptionContent' in review:
                data['구매한옵션'] = review['productOptionContent'].replace(',',' ') #구매한옵션            
            else:
                data['구매한옵션'] = None
            REVIEWS.append(data)
        return REVIEWS
