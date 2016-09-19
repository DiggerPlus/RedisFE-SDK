# -*- coding: utf-8 -*-

import urlparse
import redis


COMMANDS = ['get', 'set', 'mget', 'mset', 'pipline']


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
        self.connections = []

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
        """Redis server info"""
        connection = self._get_connection()
        info = connection.info()
        for key in info:
            setattr(self, key, info[key])
        self._put_connection_back(connection)
        return self

    def _produce_connection(self):
        connection = redis.StrictRedis(
            host=self.host, port=self.port, db=self.db,
            password=self.password, **self.redis_connection_kwargs)
        self.connections.append(connection)
        return connection

    def _get_connection(self):
        try:
            connection = self.connections.pop()
        except IndexError:
            connection = self._produce_connection()
        return connection

    def _put_connection_back(self, conn):
        assert isinstance(conn, redis.StrictRedis)
        self.connections.append(conn)

    def __repr__(self):
        return "RedisInfo<host=%s,port=%s,db=%d>" % (
            self.host, self.port, self.db)

    def __getattr__(self, name):
        """Execute redis commands filter by *COMMADNS* """
        if name not in COMMANDS:
            raise RuntimeError('Command {!r} not support'.format(name))
        connection = self._get_connection()
        return getattr(connection, name)
