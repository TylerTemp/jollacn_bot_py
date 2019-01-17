#!/usr/bin/env python3
import time

import bs4
import pika
import requests
import html2text
from bs4 import BeautifulSoup

from jollacn_bot_py.util.mini_six import fake_urllib as urllib

EXCEPTIONS = (
    requests.exceptions.Timeout,
    requests.exceptions.ConnectTimeout,
    requests.exceptions.ReadTimeout,
)


def fetch(url, proxies=None, timeout=20):
    fetch_start_time = time.time()
    if proxies is None:
        proxies = {}

    resp = requests.get(url, proxies=proxies, timeout=timeout)
    # print(resp.text)
    # print(resp.status_code)
    soup = BeautifulSoup(resp.content, 'html5lib')
    # print(soup.title)
    # print(soup.h1.text.strip())
    # print(soup.h2.text.strip())
    h1 = soup.h1
    if h1 is None:
        return False, 'failed to find titie'
    h1_hidden_part = h1.find(class_='u-hiddenVisually')
    if h1_hidden_part:
        h1_hidden_part.decompose()
    name = h1.text.strip()
    at_raw = soup.h2.text.strip()
    at = at_raw[1:]
    # if not at_raw.startswith('@'):
    #     return False, 'failed to extract at: {}'.format(at_raw)

    item_container = soup.find(id='stream-items-id')
    # if item_container is None:
    #     return False, 'failed to get item container'
    items = item_container.find_all('li', recursive=False)
    index = None
    items_parsed = []
    for index, item in enumerate(items):

        fullname = item.find(class_='fullname').text.strip()
        username = item.find(class_='username').text.strip().replace('@', '')

        is_retweet = item.find(class_='js-retweet-text') is not None

        # link
        a_link = item.find('a', class_=['twitter-timeline-link', 'u-hidden'])
        link = a_link.get('href')
        a_link.decompose()

        # time
        time_node = item.find(lambda tag: 'data-time-ms' in tag.attrs)
        timestamp_ms = int(time_node.get('data-time-ms'))

        # hashtag
        for hashtag in item.find_all('a', class_='twitter-hashtag'):
            hash_text = hashtag.text.strip()
            hash_relative_href = hashtag.get('href')
            hash_link = urllib.parse.urljoin(
                'http://twitter.com/', hash_relative_href)

            new_tag = soup.new_tag('a', href=hash_link,
                                   target='_blank', rel='noopener')
            new_tag.string = hash_text

            hashtag.replace_with(new_tag)

        # emoji
        for emoji_img in item.find_all('img', class_=('Emoji', 'Emoji--forText')):
            alt = emoji_img.get('alt')
            if alt:
                text_tag = bs4.NavigableString(alt)
                emoji_img.replace_with(text_tag)

        # atreply
        for atreply in item.find_all('a', class_='twitter-atreply'):
            href = atreply.get('href')
            reply_link = urllib.parse.urljoin('http://twitter.com/', href)
            reply_text = atreply.text.strip()

            new_tag = soup.new_tag('a', href=reply_link,
                                   target='_blank', rel='noopener')
            new_tag.string = reply_text

            atreply.replace_with(new_tag)

        text_container = item.find(class_='js-tweet-text-container')
        content = str(text_container)
        content_md = html2text.html2text(content, bodywidth=0).rstrip()
        items_parsed.append({
            'id': link.split('/')[-1],
            'name': fullname,
            'at': username,
            'timestamp_ms': timestamp_ms,
            'content_md': content_md,
            'content': content,
            'link': link,
            'retweet': is_retweet,
        })

    fetch_end_time = time.time()
    fetch_duration = fetch_end_time - fetch_start_time
    return {
        'url': url,
        'name': name,
        'at': at,
        'items': items_parsed,
        '_fetch_start_time': fetch_start_time,
        '_fetch_end_time': fetch_end_time,
        '_fetch_duration': fetch_duration,
    }


if __name__ == '__main__':
    # from pprint import pprint
    import json
    print(json.dumps(fetch('https://twitter.com/jollahq', proxies={
        'http': 'socks5h://127.0.0.1:1080',
        'https': 'socks5h://127.0.0.1:1080',
    }), ensure_ascii=False, indent=2))
