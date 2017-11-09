# /usr/bin/env python
# ! -*- coding=utf-8 -*-


import requests

today = 'https://www.shanbay.com/api/v1/bdc/stats/today'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75'
                  ' Safari/537.36'
}


def main():
    cj_dict = {}
    plain_cookie = open('cookies.txt').read()
    for p in plain_cookie.split(';'):
        li = p.strip().split('=', 1)
        cj_dict[li[0]] = li[1]
    cj = requests.utils.cookiejar_from_dict(cj_dict)
    s = requests.session()
    s.cookies = cj
    r = s.get(today, headers=headers)
    if r.status_code != 200:
        print 'error, status code:', r.status_code
    with open('review.json', 'wb') as fd:
        for chunk in r.iter_content(1024):
            fd.write(chunk)


if __name__ == '__main__':
    main()
