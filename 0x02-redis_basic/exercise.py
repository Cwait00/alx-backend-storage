#!/usr/bin/env python3
"""
Cache class for storing data in Redis.
"""


import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function in Redis.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store input and output history in Redis.
        """
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)

        # Store input
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)

        # Store output
        self._redis.rpush(output_key, output)

        return output

    return wrapper


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

    @call_history
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

    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("second")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
    outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

    print("inputs: {}".format(inputs))
    print("outputs: {}".format(outputs))
