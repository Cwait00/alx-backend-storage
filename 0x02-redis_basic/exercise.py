#!/usr/bin/env python3

"""
Cache module for interacting with Redis.
"""

import redis
import uuid
from typing import Callable, Union


class Cache:
    """
    Cache class to interact with Redis.

    This class provides methods to store and retrieve data from Redis,
    as well as a decorator to track the history of method calls.
    """

    def __init__(self):
        """
        Initialize Cache instance.

        This initializes a Redis connection and flushes the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def call_history(method: Callable) -> Callable:
        """
        Decorator to store history of inputs and outputs for a function.

        Args:
            method (Callable): The method to decorate.

        Returns:
            Callable: The decorated method.
        """
        def wrapper(self, *args, **kwargs) -> Union[str, bytes, int, float]:
            """
            Wrapper function to store input and output history.

            Args:
                self: The Cache instance.
                *args: Positional arguments passed to the method.
                **kwargs: Keyword arguments passed to the method.

            Returns:
                Union[str, bytes, int, float]: The result of the method.
            """
            input_key = "{}:inputs".format(method.__qualname__)
            output_key = "{}:outputs".format(method.__qualname__)

            self._redis.rpush(input_key, str(args))
            result = method(self, *args, **kwargs)
            self._redis.rpush(output_key, result)

            return result
        return wrapper

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return the key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The key under which the data is stored in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[
            str, bytes, int, None]:
        """
        Get data from Redis by key and apply optional conversion function.

        Args:
            key (str): The key to retrieve data for.
            fn (Callable, optional): A function to apply to the retrieved data.

        Returns:
            Union[str, bytes, int, None]: The retrieved data.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Get string data from Redis by key.

        Args:
            key (str): The key to retrieve string data for.

        Returns:
            Union[str, None]: The retrieved string data.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Get integer data from Redis by key.

        Args:
            key (str): The key to retrieve integer data for.

        Returns:
            Union[int, None]: The retrieved integer data.
        """
        return self.get(key, fn=int)


if __name__ == "__main__":
    cache = Cache()

    s1 = cache.store("first")
    s2 = cache.store("second")
    s3 = cache.store("third")

    inputs = cache._redis.lrange(
        "{}:inputs".format(cache.store.__qualname__), 0, -1)
    outputs = cache._redis.lrange(
        "{}:outputs".format(cache.store.__qualname__), 0, -1)

    print("inputs: {}".format(inputs))
    print("outputs: {}".format(outputs))
