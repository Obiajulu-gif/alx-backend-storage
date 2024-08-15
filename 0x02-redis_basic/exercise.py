#!/usr/bin/env python3
"""
Exercise file
"""

import redis
import uuid
import functools
from typing import Union, Callable, Optional


def call_history(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        # Store the input arguments
        self._redis.rpush(inputs_key, str(args))

        # Execute the wrapped function and store its output
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(result))

        return result
    return wrapper


def count_calls(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Create a key based on the qualified name of the method
        key = "count:{}".format(method.__qualname__)
        # Increment the count in Redis
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self):
        """Initialize the cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the input data in Redis using a random key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str,
                                                    bytes,
                                                    int,
                                                    float,
                                                    None]:
        """ Retrieve data from Redis and convert it using the
        provided function"""
        value = self._redis.get(key)
        if value is not None and fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a string from Redis."""
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integer from Redis"""
        value = self.get(key)
        return int(value) if value is not None else None

    def replay(func: Callable) -> None:
        cache_instance = func.__self__  # Get the instance of Cache class
        method_name = func.__qualname__
        inputs_key = "{}:inputs".format(method_name)
        outputs_key = "{}:outputs".format(method_name)

        # Retrieve the history of inputs and outputs from Redis
        inputs = cache_instance._redis.lrange(inputs_key, 0, -1)
        outputs = cache_instance._redis.lrange(outputs_key, 0, -1)

        # Count how many times the function was called
        call_count = cache_instance._redis.get("count:{}".format(method_name))
        print("{} was called {} times:".format(
            method_name, call_count.decode('utf-8')))
        # Loop over inputs and outputs and print them
        for input_str, output_str in zip(inputs, outputs):
            print("{}(*{}) -> {}".format(
                method_name,
                input_str.decode('utf-8'),
                output_str.decode('utf-8')))
