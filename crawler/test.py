# -*- coding: utf-8 -*-
import socket

import requests
# import re2
import datetime
import re


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


# def parse_url(url):
#     m = re.search("([12]\d{3}(0[1-9]|1[0-2]))", url)
#     return m.group(0)

def dfdfd(date_str):
    list = [date_str]
    now = datetime.datetime.now()
    date = datetime.datetime.strptime(date_str, '%Y%m%d')
    dd = (now - date).days

    for x in range(dd):
        date = date + datetime.timedelta(days=1)
        list.append(date.strftime('%Y%m%d'))

    return list


if __name__ == '__main__':

    match = re.search("([\.0-9a-zA-Z_-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}", "fdsa@fffff.com")

    print(bool(match))



    # url = 'http://v.media.daum.net/v/20120113190307478'
    # date_str = '20180101'
    # test = dfdfd(date_str)
    #
    # print(test)
    # now = datetime.datetime.now()
    # print(now)
    # date = datetime.datetime.strptime(date_str, '%Y%m%d')
    #
    # dd = (now - date).days
    # print(dd)
    #
    # for x in range(0, dd):
    #     date = date + datetime.timedelta(days=1)
    #     jjj = date.strftime('%Y%m%d')
    #     print(type(jjj))
    #     print(jjj)

    # tomorrow = now + datetime.timedelta(days=1)

    # print(type((now - date).days))

    # print(datetime.datetime.strptime(date_str, '%Y-%m-%d'))

    # date = parse_url(url)
    # print(url)
    # print(date)
    # response = get_html(url)
    # if not response.__eq__('-1'):
    #     soup = BeautifulSoup(response, 'html.parser')
