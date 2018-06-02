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
        print(e.strerror)
        return '-1'
    except Exception as e:
        print(e)
        return '-1'


def make_seed_url_list(seed_url, start_page, end_page):
    seed_list = []
    for i in range(start_page, end_page + 1):
        seed_list.append(seed_url + str(i))

    return seed_list


def extract_news_url(html: object) -> object:
    ext_url_list = []
    soup = BeautifulSoup(html, 'html.parser')
    selected_atag = soup.select('ul.list_news2 > li > a')

    for atag in selected_atag:
        ext_url_list.append(atag.get('href'))

    return ext_url_list


def check_email(document):
    match = re.search("([\.0-9a-zA-Z_-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}", document)
    return (bool(match))


def get_document(documents):
    document_list = []
    documents_len = len(documents.find_all('p'))
    for i, d in enumerate(documents.find_all('p')):
        _d = d.get_text()
        if len(_d) == 0:
            continue
        if check_email(_d):
            if i == (documents_len - 1):
                continue

        document_list.append(_d.strip())

    return ' '.join(document_list)


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
    documents = soup.select_one(document_tag)

    document = get_document(documents)
    line = "{}\t{}\t{}\t{}\t{}\n"

    file_name = 'data/' + date + '.csv'

    with open(file_name, 'a') as fd:
        fd.write(line.format(news_url, category, title, document, summary))
    print((line.format(news_url, category, title, document, summary)))


def crawl(seed_list, interval, date, use_interval):
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
                if use_interval:
                    time.sleep(interval)


def get_range_date(start_date_str, end_date_str):
    date_list = [start_date_str]
    start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d')
    end_date = datetime.datetime.strptime(end_date_str, '%Y%m%d')
    date_diff = (end_date - start_date).days

    for x in range(date_diff):
        start_date = start_date + datetime.timedelta(days=1)
        date_list.append(start_date.strftime('%Y%m%d'))

    return date_list


def test(url):
    html = get_html('http://v.media.daum.net/v/20180602113649756')
    news_data_store('http://v.media.daum.net/v/20180602113649756', html, 20150505)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--interval')
    parser.add_argument('-s', '--sdate')
    parser.add_argument('-e', '--edate')
    args = parser.parse_args()

    interval = float(args.interval)

    start_page = 1
    end_page = 1000

    start_date = args.sdate
    end_date = args.edate

    # html = get_html('http://v.media.daum.net/v/20180602113649756')
    # news_data_store('http://v.media.daum.net/v/20180602113649756', html, 20150505)

    date_list = get_range_date(start_date, end_date)
    category_list = ['society', 'politics', 'economic', 'culture', 'digital']
    for date in date_list:
        for category in category_list:
            seed_url = 'http://media.daum.net/breakingnews/' + category + '?regDate=' + date + '&page='
            seed_list = make_seed_url_list(seed_url, start_page, end_page)
            crawl(seed_list, interval, date, True)
            print(seed_url + ' : complete')
