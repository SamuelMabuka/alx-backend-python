#!/usr/bin/env python3
"""
Utility functions for nested map access.
"""

from typing import Any, Mapping, Sequence


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access a value in a nested map using a sequence of keys.

    Args:
        nested_map (Mapping): The nested dictionary to access.
        path (Sequence): The sequence of keys to follow.

    Returns:
        Any: The value found at the end of the path.

    Raises:
        KeyError: If a key is not found in the map.
    """
    for key in path:
        nested_map = nested_map[key]
    return nested_map
