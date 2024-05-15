#!/usr/bin/env python3

import redis
from typing import Callable
from functools import wraps
import uuid


"""Module for implementing a call history decorator using Redis."""


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a function.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    @wraps(method)
    def wrapper(*args, **kwargs):
        r = redis.Redis(
            host='localhost', port=6379, db=0
        )
        input_args = str(args)
        inputs_key = "{}:inputs".format(method.__qualname__)
        r.rpush(inputs_key, input_args)
        output = method(*args, **kwargs)
        outputs_key = "{}:outputs".format(method.__qualname__)
        r.rpush(outputs_key, output)
        return output
    return wrapper


class Cache:
    """Class representing a cache with call history."""
    def __init__(self):
        self._redis: redis.Redis = redis.Redis(
            host='localhost', port=6379, db=0
        )

    @call_history
    def store(self, data: str) -> str:
        """Store data in the cache.

        Args:
            data: The data to be stored.

        Returns:
            str: A unique identifier for the stored data.
        """
        return str(uuid.uuid4())


if __name__ == "__main__":
    cache = Cache()
    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("second")
    print(s2)
    s3 = cache.store("third")
    print(s3)
    inputs_key = "{}:inputs".format(cache.store.__qualname__)
    outputs_key = "{}:outputs".format(cache.store.__qualname__)
    inputs = cache._redis.lrange(inputs_key, 0, -1)
    outputs = cache._redis.lrange(outputs_key, 0, -1)
    print("inputs:", [inp.decode() for inp in inputs])
    print("outputs:", [out.decode() for out in outputs])
