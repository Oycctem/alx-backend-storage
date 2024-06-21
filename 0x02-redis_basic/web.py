#!/usr/bin/env python3
'''A module for request caching and tracking.'''
import redis
import requests
from datetime import timedelta
from functools import wraps

redis_store = redis.Redis()


def cache_page(func):
    '''Decorator to cache the result of a
    URL request and track the access count.'''
    @wraps(func)
    def wrapper(url: str) -> str:
        res_key = f'result:{url}'
        req_key = f'count:{url}'
        result = redis_store.get(res_key)
        if result is not None:
            redis_store.incr(req_key)
            return result.decode('utf-8')
        result = func(url)
        redis_store.setex(res_key, timedelta(seconds=10), result)
        redis_store.incr(req_key)
        return result
    return wrapper


@cache_page
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the response and tracking.'''
    response = requests.get(url)
    return response.content.decode('utf-8')


if __name__ == "__main__":
    url = ("http://slowwly.robertomurray.co.uk/delay/5000/"
           "url/http://www.google.com")
    print(get_page(url))
