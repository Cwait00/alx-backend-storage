#!/usr/bin/env python3
import functools
import redis
import uuid
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union

T = TypeVar("T")


def call_history(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator to store the history of inputs and outputs for a function.

    :param func: Function to decorate.
    :type func: callable
    :return: Wrapped function that stores input and output history.
    :rtype: callable
    """
    @functools.wraps(func)
    def wrapper(self: "Cache", *args: Any, **kwargs: Any) -> T:
        key = func.__qualname__
        input_key = f"{key}:inputs"
        output_key = f"{key}:outputs"

        # Store input arguments as a string representation
        input_args = str(args)
        self._redis.rpush(input_key, input_args)

        # Execute the function to get the output
        output = func(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(output_key, output)

        return output

    return wrapper


class Cache:
    """Cache class to store data in Redis."""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
        :return: Retrieved data, optionally converted using the provided function.
        :rtype: Any
        """
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def replay(self, func: Callable[..., T]) -> None:
        """
        Replay the history of calls for a function.

        :param func: Function to replay the history for.
        :type func: callable
        """
        key = func.__qualname__
        input_key = f"{key}:inputs"
        output_key = f"{key}:outputs"

        inputs = self._redis.lrange(input_key, 0, -1)
        outputs = self._redis.lrange(output_key, 0, -1)

        print(f"{func.__name__} was called {len(inputs)} times:")
        for input_args, output in zip(inputs, outputs):
            print(f"{func.__name__}(*{input_args}) -> {output}")
