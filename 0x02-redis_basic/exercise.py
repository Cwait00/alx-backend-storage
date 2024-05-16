#!/usr/bin/env python3
import redis
import uuid
from typing import Union


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
