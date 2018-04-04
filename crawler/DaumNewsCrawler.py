# -*- coding: utf-8 -*-
import time
import requests
import datetime
import argparse
from bs4 import BeautifulSoup


def make_seed_url_list(seed_url, start_page, end_page):
    seed_list = []
    for i in range(start_page, end_page + 1):
        seed_list.append(seed_url + str(i))

    return seed_list


def extract_news_url(html):
    ext_url_list = []
    soup = BeautifulSoup(html, 'html.parser')
    selected_atag = soup.select('ul.list_news2 > li > a')

    for atag in selected_atag:
        ext_url_list.append(atag.get('href'))

    return ext_url_list


def news_data_store(category, html):
    title_tag = 'h3.tit_view'
    summary_tag = 'div.news_view > .summary_view'
    document_tag = 'div.article_view'

    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one(title_tag).text.strip().replace('\n', ' ')
    summary = ''
    try:
        summary = soup.select_one(summary_tag).text.strip().replace('\n', ' ')
    except AttributeError:
        print('not exist summary')
        return

    document = soup.select_one(document_tag).text.strip().replace('\n', ' ')

    line = "{}\t{}\t{}\t{}\n"

    current = datetime.datetime.now()
    file_name = '../data/' + category + '/' + current.strftime('%Y-%m-%d') + '.csv'
    with open(file_name, 'a') as fd:
        fd.write(line.format(category, title, document, summary))
    print((line.format(category, title, document, summary)))


def crawl(category, seed_list, interval):
    for seed in seed_list:
        news_url_list = extract_news_url(requests.get(seed).text)
        for news_url in news_url_list:
            print("crawl url : {}".format(news_url))
            html = requests.get(news_url).text
            news_data_store(category, html)
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
    args = parser.parse_args()
    category = args.category
    print(category)
    # category = 'society'
    seed_url = 'http://media.daum.net/breakingnews/' + category + '?page='
    interval = 2
    start_page = 1
    end_page = 100000;

    seed_list = make_seed_url_list(seed_url, start_page, end_page)
    crawl(category, seed_list, interval)
    print(seed_url + ' : complete')
