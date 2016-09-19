# -*- coding: utf-8 -*-

from .redisinfo import RedisInfo

__all__ = ['RedisInfo']

version_info = (0, 0, 1)
__version__ = ".".join([str(v) for v in version_info])
