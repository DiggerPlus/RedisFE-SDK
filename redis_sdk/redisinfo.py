# -*- coding: utf-8 -*-

import urlparse
import redis


class RedisInfo(object):
    """Redis info object.

        >>> from redis_sdk import RedisInfo
        >>> redis_client = RedisInfo('redis://localhost:6379/0')
        >>> redis_info = redis_client.info
        >>> redis_info
        RedisInfo<host=localhost,port=6379,db=0>
        >>> redis_info.redis_version
        3.0.7

    """

    def __init__(self, dsn, password=None, **redis_connection_kwargs):
        self.dsn = urlparse.urlparse(dsn)
        self.password = password
        self.redis_connection_kwargs = redis_connection_kwargs
        self.client = None

    @property
    def host(self):
        return self.dsn.hostname

    @property
    def port(self):
        return self.dsn.port

    @property
    def db(self):
        try:
            return int(self.dsn.path[-1])
        except (IndexError, ValueError):
            return 0
        except Exception:
            raise

    @property
    def info(self):
        if self.client is None:
            self.client = redis.StrictRedis(
                host=self.host, port=self.port, db=self.db,
                password=self.password, **self.redis_connection_kwargs)
        info = self.client.info()
        for key in info:
            setattr(self, key, info[key])
        return self

    def __repr__(self):
        return "RedisInfo<host=%s,port=%s,db=%d>" % (
            self.host, self.port, self.db)
