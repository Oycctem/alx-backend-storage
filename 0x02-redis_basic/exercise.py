#!/usr/bin/env python3
""" Interacting with Redis: storing, retrieving, counting, call history """
from typing import Union, Callable, Optional
import redis
import uuid
from functools import wraps


def call_history(method: Callable) -> Callable:
    """Store history of inputs and outputs for a function."""
    key = method.__qualname__
    inputs = f"{key}:inputs"
    outputs = f"{key}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Record inputs and outputs to Redis."""
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(result))
        return result

    return wrapper


def count_calls(method: Callable) -> Callable:
    """Count how many times a method is called."""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Increment call count in Redis."""
        self._redis.incr(key)
        return method(self, *args, **kwds)

    return wrapper


class Cache:
    """Cache class interfacing with Redis."""

    def __init__(self):
        """Initialize Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with a random key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        """Get data from Redis by key and apply an optional function."""
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Get data from Redis and decode as UTF-8 string."""
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """Get data from Redis, decode as UTF-8 string, convert to int."""
        data = self._redis.get(key)
        try:
            return int(data.decode("utf-8"))
        except (ValueError, AttributeError):
            return 0


def replay(method: Callable):
    """Display the history of calls to a function."""
    key = method.__qualname__
    inputs = f"{key}:inputs"
    outputs = f"{key}:outputs"
    redis = method.__self__._redis
    count = redis.get(key).decode("utf-8")
    print(f"{key} was called {count} times:")
    input_list = redis.lrange(inputs, 0, -1)
    output_list = redis.lrange(outputs, 0, -1)
    for inp, out in zip(input_list, output_list):
        input_str = inp.decode("utf-8")
        output_str = out.decode("utf-8")
        print(f"{key}(*{input_str}) -> {output_str}")
