#!/usr/bin/env python3
"""
Exercise file
"""

import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        """Initialize the cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the input data in Redis using a random key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
