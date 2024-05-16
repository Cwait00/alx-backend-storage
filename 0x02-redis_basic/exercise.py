#!/usr/bin/env python3
"""
Cache class for storing data in Redis.
"""

import redis
import uuid
from typing import Union, Callable, Optional


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

    def get(self, key: str, fn: Optional[Callable[[bytes], Union[str, int, float]]] = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis using the provided key and optionally apply a conversion function.

        Args:
            key: The key used to retrieve data from Redis.
            fn: Optional callable to convert the retrieved data.

        Returns:
            The retrieved data, optionally converted using the provided function.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, bytes]:
        """
        Retrieve data from Redis using the provided key and convert it to a string.

        Args:
            key: The key used to retrieve data from Redis.

        Returns:
            The retrieved data as a string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, bytes]:
        """
        Retrieve data from Redis using the provided key and convert it to an integer.

        Args:
            key: The key used to retrieve data from Redis.

        Returns:
            The retrieved data as an integer.
        """
        return self.get(key, fn=int)


# Example usage
if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
