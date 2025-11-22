import requests
import os
import argparse


from urllib.parse import urlparse
from dotenv import load_dotenv


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('url')
    return parser


def shorten_link(vk_token, url):
    param = {
        'access_token' : vk_token,
        'url' : url,
        'v' : 5.199
    }
    url = 'https://api.vk.com/method/utils.getShortLink'
    response = requests.post(url, params = param)
    response.raise_for_status()
    return response.json()['response']['short_url']


def count_clicks(vk_token, parsed_url):
    param = {
        'access_token' : vk_token,
        'key' : parsed_url.path[1:],
        'interval' : 'forever',
        'v' : 5.199
    }
    url = 'https://api.vk.com/method/utils.getLinkStats'
    response = requests.post(url, params = param)
    response.raise_for_status()
    return response.json()['response']['stats'][0]['views']
      

def is_shorten_link(vk_token, parsed_url):
    param = {
        'access_token' : vk_token,
        'key' : parsed_url.path[1:],
        'interval' : 'forever',
        'v' : 5.199
    }
    url = 'https://api.vk.com/method/utils.getLinkStats'
    response = requests.post(url, params = param)
    response.raise_for_status()
    is_short_link = response.json()
    return'error' not in is_short_link


def main():
    load_dotenv()
    parser = createParser()
    namespace = parser.parse_args()
    url = namespace.url
    parsed_url = urlparse(url)
    vk_token = os.environ['VK_TOKEN']
    if is_shorten_link(vk_token, parsed_url):
        try:
            print('Колличество кликов: ', count_clicks(vk_token, parsed_url))
        except requests.exceptions.HTTPError:
            print("Вы ввели неправильную ссылку или неверный токен.")
    else:
        try:
            print('Сокращенная ссылка: ', shorten_link(vk_token, url))
        except requests.exceptions.HTTPError:
            print("Вы ввели неправильную ссылку или неверный токен.")


if __name__ == '__main__':
    main()