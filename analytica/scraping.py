import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import re
import numpy as np
import os

from dotenv import load_dotenv

load_dotenv()


def extract_asin(url):
    # Regular expression to find the ASIN
    asin_pattern = r'/dp/([A-Z0-9]{10})|/product/([A-Z0-9]{10})'
    match = re.search(asin_pattern, url)
    if match:
        return match.group(1) if match.group(1) else match.group(2)
    else:
        return None
    
# '8ec02ed2-1a67-492e-8599-7a47141f2565'

api_key_1 = os.getenv('api_key_1')

def get_html_content_pos(asin, page_num=1):
    proxy_params = {
        'api_key': api_key_1,
        'url' : f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&sortBy=helpful&pageNumber={page_num}&filterByStar=positive",
        'render_js': True,
      }

    response = requests.get(
      url='https://proxy.scrapeops.io/v1/',
      params= urlencode(proxy_params),
      timeout=125,
    )
    
    return response


def get_html_content_neg(asin, page_num=1):
    proxy_params = {
        'api_key': api_key_1,
        'url' : f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&reviewerType=all_reviews&sortBy=helpful&pageNumber={page_num}&filterByStar=critical",
        'render_js': True,
      }

    response = requests.get(
      url='https://proxy.scrapeops.io/v1/',
      params= urlencode(proxy_params),
      timeout=125,
    )
    
    return response

def extract_review_title(review_tag):
    title = review_tag.find('a', attrs={"data-hook": "review-title"}).find_all('span')[-1].text.strip()
    return title


def extract_review_body(review_tag):
    text = review_tag.find('span', attrs={"data-hook": "review-body"}).find('span').text.strip()
    return text




def get_data(review_tag):
    return extract_review_title(review_tag) + ' ' + extract_review_body(review_tag)





def get_reviews_pos(asin):
    reviews_data = []
    page_num = 1
    while True: 
        response = get_html_content_pos(asin=asin, page_num=page_num)
        soup = BeautifulSoup(response.content, 'html.parser')

        review_tags = soup.find_all('div', attrs={"data-hook": "review"})

        if len(review_tags) == 0:
            break
        else:
            for review_tag in review_tags:
                review = get_data(review_tag)
                reviews_data.append(review)
        page_num+=1
        
        if page_num > 15:
            break
        
    return reviews_data


def get_reviews_neg(asin):
    reviews_data = []
    page_num = 1
    while True: 
        response = get_html_content_neg(asin=asin, page_num=page_num)
        soup = BeautifulSoup(response.content, 'html.parser')

        review_tags = soup.find_all('div', attrs={"data-hook": "review"})

        if len(review_tags) == 0:
            break
        else:
            for review_tag in review_tags:
                review = get_data(review_tag)
                reviews_data.append(review)
        page_num+=1
        
        if page_num > 10:
            break
        
    return reviews_data







def get_reviews(asin):
    pos_rev = get_reviews_pos(asin)
    neg_rev = get_reviews_neg(asin)


    return pos_rev, neg_rev
