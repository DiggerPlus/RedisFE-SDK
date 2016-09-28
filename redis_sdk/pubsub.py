# -*- coding: utf-8 -*-

import redis
import threading


class Listener(threading.Thread):

    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.psubscribe(channels)

    def work(self, item):
        print item['channel'], ": ", item['data']

    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == 'KILL':
                self.pubsub.unsubscribe()
                print self, 'unsubscribeed and finished'
                break
            else:
                self.work(item)


if __name__ == '__main__':
    r = redis.Redis()
    client = Listener(r, ['test', 'test-*'])
    client.start()

    # the publish method returns the number matching channel and pattern
    # subscriptions. 'test-*' matches both 'test' subscription and the
    # 'test-*' pattern subscription, so this message willl be delivered to 2
    # channles/patterns
    r.publish('test-kiven', 'test-* patterns')
    r.publish('test', 'test channel')
    r.publish('test', 'KILL')
