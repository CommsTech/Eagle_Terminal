"""This module provides a simple in-memory caching mechanism with time-to-live
(TTL) and maximum size limit.

The Cache class can be used to store and retrieve key-value pairs with
automatic expiration and size management.
"""

import time
from functools import wraps


class Cache:
    """A simple in-memory cache with time-to-live (TTL) and maximum size limit.

    Attributes:
        cache (dict): The internal dictionary to store cached items.
        max_size (int): The maximum number of items the cache can hold.
        ttl (int): The time-to-live for cached items in seconds.
    """

    def __init__(self, max_size=1000, ttl=3600):
        """Initialize the Cache object.

        Args:
            max_size (int, optional): The maximum number of items the cache can hold.
                Defaults to 1000.
            ttl (int, optional): The time-to-live for cached items in seconds.
                Defaults to 3600 (1 hour).
        """
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl

    def get(self, key):
        """Retrieve a value from the cache.

        Args:
            key: The key to look up in the cache.

        Returns:
            The cached value if it exists and hasn't expired, otherwise None.
        """
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
        return None

    def set(self, key, value):
        """Set a value in the cache.

        If the cache is at maximum capacity, the oldest item is removed before adding the new one.

        Args:
            key: The key to store the value under.
            value: The value to be stored in the cache.
        """
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache, key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        self.cache[key] = (value, time.time())

    @staticmethod
    def cached(func):
        """A decorator that caches the results of a method.

        The cache is stored in the instance's `cache` attribute, which should be an instance of
        the Cache class.

        Args:
            func: The method to be cached.

        Returns:
            A wrapped version of the input function that caches its results.
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            key = str(args) + str(kwargs)
            result = self.cache.get(key)
            if result is None:
                result = func(self, *args, **kwargs)
                self.cache.set(key, result)
            return result

        return wrapper
