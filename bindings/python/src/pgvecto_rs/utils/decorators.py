import numpy as np
from functools import wraps


def ignore_none(func):
    @wraps(func)
    def _func(value, *args, **kwargs):
        return value if value is None else func(value, *args, **kwargs)

    return _func


def ignore_ndarray(func):
    @wraps(func)
    def _func(value, *args, **kwargs):
        return value if isinstance(value, np.ndarray) else func(value, *args, **kwargs)

    return _func


def validate_ndarray(func):
    """Validate ndarray data type for vector"""

    @wraps(func)
    def _func(value: np.ndarray, *args, **kwargs):
        if isinstance(value, np.ndarray):
            if value.ndim != 1:
                raise ValueError("ndarray must be 1D for vector")
            if not np.issubdtype(value.dtype, np.number):
                raise ValueError("ndarray data type must be numeric for vector")
        return func(value, *args, **kwargs)

    return _func


def validate_builtin_list(func):
    """Validate list data type for vector and convert to ndarray"""

    @wraps(func)
    def _func(value: list, *args, **kwargs):
        if isinstance(value, list):
            if not all(isinstance(x, (int, float)) for x in value):
                raise ValueError("list data type must be numeric for vector")
            value = np.array(value, dtype=np.float32)
        return func(value, *args, **kwargs)

    return _func
