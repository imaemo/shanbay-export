# /usr/bin/env python
# ! -*- coding=utf-8 -*-


import requests
import os
from jinja2 import Environment, FileSystemLoader

today = 'https://www.shanbay.com/api/v1/bdc/stats/today'
word_base_url = 'https://www.shanbay.com/api/v1/bdc/library/today/?page='

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75'
                  ' Safari/537.36'
}


def main():
    result = {}
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
    __data = r.json()['data']
    print __data
    result['num_passed'] = __data['num_passed']
    result['num_total'] = __data['num_total']
    result['used_minutes'] = __data['used_minutes']
    with open('review.json', 'wb') as fd:
        for chunk in r.iter_content(1024):
            fd.write(chunk)

    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')
    j2_env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)

    total_page = 1
    word_list = []
    word_url = word_base_url + str(total_page)

    r = s.get(word_url, headers=headers)
    if r.status_code != 200:
        print 'status code:', r.status_code
    else:
        __data = r.json()
        for w in __data['data']['objects']:
            word = {'content': w['content'], 'pron': w['pron'], 'definition': w['definition'], 'audio': w['audio']}
            word_list.append(word)
        total_page = __data['data']['total'] / __data['data']['ipp']
        for curr_page in range(2, total_page + 1):
            if curr_page == 5:
                break
            word_url = word_base_url + str(curr_page)
            r = s.get(word_url, headers=headers)
            if r.status_code != 200:
                print 'status code:', r.status_code
            else:
                __data = r.json()
                for w in __data['data']['objects']:
                    word = {'content': w['content'], 'pron': w['pron'], 'definition': w['definition'],
                            'audio': w['audio']}
                    word_list.append(word)
    result['words'] = word_list

    j2_env.get_template('wordList.html').stream(result).dump('wordList.html')


if __name__ == '__main__':
    main()
