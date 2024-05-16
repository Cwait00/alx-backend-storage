#!/usr/bin/env python3
import redis
import uuid
from typing import Any, Callable, Optional, Union


class Cache:
    """Cache class to store data in Redis."""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return the key.

        :param data: Data to be stored in Redis.
        :type data: str, bytes, int or float
        :return: Random key associated with the stored data.
        :rtype: str
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[bytes], Any]] = None) -> Any:
        """
        Retrieve data from Redis and apply optional conversion function.

        :param key: Key associated with the stored data.
        :type key: str
        :param fn: Optional conversion function to apply on the retrieved data.
        :type fn: callable, optional
        :return: Retrieved data, optionally converted using the
        provided function.
        :rtype: Any
        """
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieve data from Redis and decode it as a UTF-8 string.

        :param key: Key associated with the stored data.
        :type key: str
        :return: Retrieved data decoded as a UTF-8 string.
        :rtype: str
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieve data from Redis and convert it to an integer.

        :param key: Key associated with the stored data.
        :type key: str
        :return: Retrieved data converted to an integer.
        :rtype: int
        """
        return self.get(key, int)
