# -*- coding: utf-8 -*-

import gevent
import gevent.event
from gevent.queue import Queue

from redis_sdk.event_manager import event_manager


LOCAL_STACK = []
Q = Queue()


def fake_test(stop_event):
    while not stop_event.is_set():
        gevent.sleep(1)
        LOCAL_STACK.append(1)


def queue_test1(stop_event):
    while not stop_event.is_set():
        gevent.sleep(1)
        Q.put('1')


def queue_test2(stop_event):
    while not stop_event.is_set():
        gevent.sleep(1)
        Q.put('2')


def test_one_event_manager():
    event_manager.register(fake_test)
    event_manager.trigger_all()
    for _ in range(5):
        gevent.sleep(1)
    event_manager.set_events()

    assert 4 <= len(LOCAL_STACK) <= 6


def test_multi_event_manager():
    event_manager.clear_event()
    event_manager.register(queue_test1)
    event_manager.register(queue_test2)
    event_manager.trigger_all()
    gevent.sleep(5)
    event_manager.set_events()

    assert 8 <= Q.qsize() <= 12
