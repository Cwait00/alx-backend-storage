#!/usr/bin/env python3
import functools
import redis
import uuid
from typing import Callable, Optional, TypeVar, Union

T = TypeVar("T")


def count_calls(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator to count the number of times a method is called.

    :param func: Method to decorate.
    :type func: callable
    :return: Wrapped function that increments the call count.
    :rtype: callable
    """
    call_count_key = f"{func.__module__}.{func.__qualname__}.calls"

    @functools.wraps(func)
    def wrapper(self: "Cache", *args: Any, **kwargs: Any) -> T:
        self._redis.incr(call_count_key)
        return func(self, *args, **kwargs)

    return wrapper


class Cache:
    """Cache class to store data in Redis."""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
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
