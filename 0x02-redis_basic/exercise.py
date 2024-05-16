#!/usr/bin/env python3
"""
Cache class for storing data in Redis.
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class for storing data in Redis.
    """
    def __init__(self) -> None:
        """
        Initialize the Cache with a Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a randomly generated key.

        Args:
            data: The data to store in Redis. Can be str, bytes, int, or float.

        Returns:
            The randomly generated key used for storing the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


# Example usage
if __name__ == "__main__":
    cache = Cache()
    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
