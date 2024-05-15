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


def replay(func):
    """Display the history of calls of a particular function.

    Args:
        func (Callable): The function whose history of calls needs to
        be displayed.
    """
    inputs_key = "{}:inputs".format(func.__qualname__)
    outputs_key = "{}:outputs".format(func.__qualname__)

    # Retrieve inputs and outputs from Redis
    inputs = cache._redis.lrange(inputs_key, 0, -1)
    outputs = cache._redis.lrange(outputs_key, 0, -1)

    # Display the history of calls
    print("{} was called {} times:".format(func.__qualname__, len(inputs)))
    for inp, out in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(
            func.__qualname__, inp.decode(), out.decode()
        ))


if __name__ == "__main__":
    # Example usage
    cache = Cache()
    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    replay(cache.store)
