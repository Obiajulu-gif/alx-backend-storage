import redis
from typing import Union, Optional, Callable
import uuid

# Assuming the decorator 'count_calls' needs to be defined or imported


def count_calls(func):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


class Cache:
    def __init__(self):
        """Initialize the cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the input data in Redis using a random key"""
        key = str(uuid.uuid4())
        # Ensure data is stored as a string
        self._redis.set(key, str(data))
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str,
                                                    bytes,
                                                    int,
                                                    float,
                                                    None]:
        """Retrieve data from Redis and convert it using the
        provided function"""
        value = self._redis.get(key)
        if value is not None and fn is not None:
            # Apply the conversion function if value is not None and fn is
            # provided
            return fn(value)
        return value
