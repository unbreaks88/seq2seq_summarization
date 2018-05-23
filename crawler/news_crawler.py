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
        # print(seed_url + str(i))

    return seed_list


def extract_news_url(html: object) -> object:
    ext_url_list = []
    soup = BeautifulSoup(html, 'html.parser')
    selected_atag = soup.select('ul.list_news2 > li > a')

    for atag in selected_atag:
        ext_url_list.append(atag.get('href'))

    return ext_url_list


def news_data_store(news_url, html, date):
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

    category = soup.find('h2', {'id': 'kakaoBody'}).text.strip().replace('\n', ' ')
    title = soup.select_one(title_tag).text.strip().replace('\n', ' ')
    document = soup.select_one(document_tag).text.strip().replace('\n', ' ')
    line = "{}\t{}\t{}\t{}\t{}\n"

    file_name = 'data/' + date + '.csv'

    with open(file_name, 'a') as fd:
        fd.write(line.format(news_url, category, title, document, summary))
    print((line.format(news_url, category, title, document, summary)))


def crawl(seed_list, interval, date):
    for seed in seed_list:
        response = get_html(seed)
        print(seed)
        if not response.__eq__('-1'):
            news_url_list = extract_news_url(response)
            for news_url in news_url_list:
                print("crawl url : {}".format(news_url))
                html = get_html(news_url)
                if not response.__eq__('-1'):
                    news_data_store(news_url, html, date)
                time.sleep(interval)


def get_range_date(start_date_str):
    date_list = [start_date_str]
    now = datetime.datetime.now()
    start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d')
    date_diff = (now - start_date).days

    for x in range(date_diff):
        start_date = start_date + datetime.timedelta(days=1)
        date_list.append(start_date.strftime('%Y%m%d'))

    return date_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Category')

    parser.add_argument('-i', '--interval')
    parser.add_argument('-d', '--date')
    args = parser.parse_args()

    interval = float(args.interval)
    print(type(interval))
    print(interval)
    start_page = 1
    end_page = 200

    start_date = args.date
    date_list = get_range_date(start_date)
    category_list = ['society', 'politics', 'economic', 'culture', 'digital']
    for date in date_list:
        for category in category_list:
            seed_url = 'http://media.daum.net/breakingnews/' + category + '?regDate=' + date + '&page='
            seed_list = make_seed_url_list(seed_url, start_page, end_page)
            crawl(seed_list, interval, date)
            print(seed_url + ' : complete')
