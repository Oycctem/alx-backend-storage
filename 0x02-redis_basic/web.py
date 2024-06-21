#!/usr/bin/env python3
'''A module with tools for request caching and tracking.'''
import redis
import requests
from datetime import timedelta


def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the response and tracking.'''
    if url is None or len(url.strip()) == 0:
        return ''
    redis_store = redis.Redis()
    res_key = f'result:{url}'
    req_key = f'count:{url}'
    result = redis_store.get(res_key)
    if result is not None:
        redis_store.incr(req_key)
        return result.decode('utf-8')
    result = requests.get(url).content.decode('utf-8')
    redis_store.setex(res_key, timedelta(seconds=10), result)
    return result
