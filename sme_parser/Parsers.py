from .BaseParser import BaseParser

import requests
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from typing import List, Dict, Optional
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from json.decoder import JSONDecodeError

class Buff(BaseParser):
    HOME_PAGE = ''
    MARKET_PAGE = ''
    MARKET_API_PAGE = ''


    def __init__(self, login: str, password: str, secret: str, proxies: List[str]) -> None:
        super().__init__(login, password, secret)
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/20.0 Chrome/106.0.5249.126 Safari/537.36'
        self.proxies = proxies

    def log_in(self) -> requests.Session:
        login_headers = {
        'user-agent': f'{self.user_agent}',
        'accept': '*/*',
        }
        temp_html = self.session.get('https://steamcommunity.com/openid/login?openid.mode=checkid_setup&openid.ns=http%3A%2F'
                            '%2Fspecs.openid.net%2Fauth%2F2.0&openid.realm=https%3A%2F%2Fbuff.163.com%2F&openid.sreg'
                            '.required=nickname%2Cemail%2Cfullname&openid.assoc_handle=None&openid.return_to=https%3A'
                            '%2F%2Fbuff.163.com%2Faccount%2Flogin%2Fsteam%2Fverification%3Fback_url%3D%252Faccount'
                            '%252Fsteam_bind%252Ffinish&openid.ns.sreg=http%3A%2F%2Fopenid.net%2Fextensions%2Fsreg'
                            '%2F1.1&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select'
                            '&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select',
                            headers=login_headers).content
        soup = BeautifulSoup(temp_html, features='html.parser')
        openid = {
            'action': (None, soup.find('input', {'id': 'actionInput'})['value']),
            'openid.mode': (None, soup.find('input', {'name': 'openid.mode'})['value']),
            'openidparams': (None, soup.find('input', {'name': 'openidparams'})['value']),
            'nonce': (None, soup.find('input', {'name': 'nonce'})['value'])
        }
        self.session.post('https://steamcommunity.com/openid/login', files=openid, headers=login_headers)
        
    @classmethod
    def max_pages(cls) -> int:
        mp_headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Mobile Safari/537.36',
        'accept': '*/*',
        'host': 'buff.163.com',
        'referer': 'https://buff.163.com/'
        }
        count = requests.get('https://buff.163.com/api/market/goods?game=csgo&page_num=1&use_suggestion=0&_=1680098328746',
                         headers=mp_headers).json()['data']['total_page']
        return count

    def request(self, page: int):
        request_header = {
            'user-agent': f'{self.user_agent}',
            'accept': '*/*',
            'host': 'buff.163.com',
            'referer': 'https://buff.163.com/'
            }
        
        response = self.session.get(
        url=f'https://buff.163.com/api/market/goods?game=csgo&page_num={page}&use_suggestion=0&_=1680170306951',
        headers=request_header)
        
        try:
            response = response.json()
        except JSONDecodeError as err:
            print(response.content)
        except Exception as err:
            self.session.proxies.update({'http': 'http://' + self.proxies.pop().replace('\n','')})
            response = self.request(self, page)
        

        try:
            for item in response["data"]["items"]:
                continue
        except TypeError:
            print(response)
            response = self.request(page)
        except KeyError:
            print(response)
            response = self.request(page)
        except JSONDecodeError as err:
            print(response.content)

        return response


    def parse(self, start_page, end_page, sleep_timer = 10) -> Dict[str, dict]:
        data: dict = {}
        for page in range(start_page, end_page):
            response = self.request(page=page)
            for item in response["data"]["items"]:
                data.update({f'{item["market_hash_name"]}': item})
            time.sleep(sleep_timer)
        return data
