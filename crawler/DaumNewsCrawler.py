# -*- coding: utf-8 -*-
import argparse
import datetime
import re
import socket
import time

import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return '-1'

    except socket.timeout as e:
        print(e)
        return '-1'
    except Exception as e:
        print(e)
        return '-1'


def get_date(url):
    m = re.search("([12]\d{3}(0[1-9]|1[0-2]))", url)
    return m.group(0)


def make_seed_url_list(seed_url, start_page, end_page):
    seed_list = []
    for i in range(start_page, end_page + 1):
        seed_list.append(seed_url + str(i))
        print(seed_url + str(i))

    return seed_list


def extract_news_url(html: object) -> object:
    ext_url_list = []
    soup = BeautifulSoup(html, 'html.parser')
    selected_atag = soup.select('ul.list_news2 > li > a')

    for atag in selected_atag:
        ext_url_list.append(atag.get('href'))

    return ext_url_list


def news_data_store(category, html, parsed_date):
    title_tag = 'h3.tit_view'
    summary_tag = 'div.news_view > .summary_view'
    document_tag = 'div.article_view'

    soup = BeautifulSoup(html, 'html.parser')

    summary = ''
    try:
        summary = soup.select_one(summary_tag).text.strip().replace('\n', ' ')
    except AttributeError:
        print('not exist summary')
        return

    title = soup.select_one(title_tag).text.strip().replace('\n', ' ')
    document = soup.select_one(document_tag).text.strip().replace('\n', ' ')
    line = "{}\t{}\t{}\t{}\n"

    file_name = '../data/' + category + '/' + parsed_date + '_' + category + '.csv'

    with open(file_name, 'a') as fd:
        fd.write(line.format(category, title, document, summary))
    print((line.format(category, title, document, summary)))


def crawl(category, seed_list, interval):
    for seed in seed_list:
        response = get_html(seed)
        if not response.__eq__('-1'):
            news_url_list = extract_news_url(response)
            for news_url in news_url_list:
                print("crawl url : {}".format(news_url))
                parsed_date = get_date(news_url)
                html = get_html(news_url)
                if not response.__eq__('-1'):
                    news_data_store(category, html, parsed_date)
                time.sleep(interval)


'''
    seed_url : 각각 카테고리의 paging url을 아래와 같이 넣어 주면 됨 
    start_page : 시작 page number 입력
    end_page : 마지막 page number 입력
    interval : request interval 초단위 입력 
    file_name : 수집 저장 파일 위치 + file name 
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Category')

    parser.add_argument('-c', '--category')
    parser.add_argument('-d', '--date')
    args = parser.parse_args()
    category = args.category
    date = args.date
    seed_url = 'http://media.daum.net/breakingnews/' + category + '?regDate=' + date + '&page='
    interval = 1
    start_page = 1
    end_page = 500

    seed_list = make_seed_url_list(seed_url, start_page, end_page)
    crawl(category, seed_list, interval)
    print(seed_url + ' : complete')
