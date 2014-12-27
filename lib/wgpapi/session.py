"""
Python library for using Wargaming PublicAPI
Copyright (C) 2014 VitaliyS <hetleven@yandex.ua>

based on: https://github.com/OpenWGPAPI

This code is covered by the standard Python License.
"""

import json
import time
import urllib
import urllib2

class Server:
  RU   = 'worldoftanks.ru'
  EU   = 'worldoftanks.eu'
  COM  = 'worldoftanks.com'
  SEA  = 'worldoftanks.asia'
  KR   = 'worldoftanks.kr'
  
class Error(Exception):
    pass

class Page(object):

    def __init__(self, url, num_retries=5, delay_seconds=5):

        self.url = url
        self.row_text = ''
        self.response_code = 0
        self.response_info = ()
        self.num_retries = num_retries
        self.delay_seconds = delay_seconds
  
    def fetch(self):
  
        last_exception = None
        count = 0
        is_ok = False
      
        while (not is_ok) and (count < self.num_retries):
      
            try:
                response = urllib2.urlopen(self.url, None, 30)
                is_ok = True
            except Exception as e:
                last_exception = e
                count += 1
                time.sleep(self.delay_seconds)
      
        if not is_ok:
            raise last_exception
      
        if response.getcode() > 200:
            raise Error("urlopen code: %d url: %s" % (response.getcode(), self.url))
      
        self.response_code = response.getcode()
        self.response_info = response.info()
        self.row_text = response.read()
        return self.row_text

class Session(object):

    def __init__(self, api_host, api_key, num_retries=5, delay_seconds=5):
        self.api_host = api_host
        self.api_key = api_key
        self.num_retries = num_retries
        self.delay_seconds = delay_seconds

    def fetch(self, url, params):
        page = Page("http://api.%s/%s/?application_id=%s&%s" % (self.api_host, url, self.api_key, params), self.num_retries, self.delay_seconds)
        resp = json.loads(page.fetch())
        if resp['status'] == 'ok':
            return resp['data']

        raise Error(repr(resp))
