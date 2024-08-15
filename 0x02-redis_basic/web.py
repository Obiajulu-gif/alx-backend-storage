#!/usr/bin/env python3
""" Web module """

import requests
import redis
from functools import wraps
from typing import Callable

r = redis.Redis()


def count_calls(method: Callable) -> Callable:

    @wraps(method)
    def wrapper(url: str) -> str:
        count_key = "count:{}".format(url)
        cache_key = "cache:{}".format(url)
        # Increment the URL access count
        r.incr(count_key)
        # Check if the URL's content is already cached
        cached_content = r.get(cache_key)
        if cached_content:
            return cached_content.decode('utf-8')
        # If not cached, fetch the content and cache it
        content = method(url)
        r.setex(cache_key, 10, content)  # Cache with expiration of 10 seconds
        return content
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """Fetch the HTML content of the specified URL."""
    response = requests.get(url)
    return response.text
