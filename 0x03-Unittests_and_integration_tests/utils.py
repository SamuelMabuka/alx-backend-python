#!/usr/bin/env python3
"""
Utility functions for nested map access, HTTP JSON fetch, and memoization.
"""

from typing import Any, Mapping, Sequence
import requests


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access a value in a nested map using a sequence of keys.
    Raises KeyError if a key is not found or path is invalid.
    """
    current = nested_map
    for key in path:
        if not isinstance(current, Mapping):
            raise KeyError(key)
        current = current[key]
    return current


def get_json(url: str) -> Any:
    """
    Fetch JSON content from a given URL.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        Any: The JSON response.
    """
    response = requests.get(url)
    return response.json()


def memoize(method):
    """
    Decorator to cache the result of a method.

    Args:
        method: The method to be memoized.

    Returns:
        Callable: The memoized method.
    """
    attr_name = f"_memoized_{method.__name__}"

    @property
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper



