# -*- coding: utf-8 -*-

import gevent


class Event(object):
    """Event Object"""

    def __init__(self, func, stop_event):
        self.func = func
        self.stop_event = stop_event
        self.is_running = False

    @property
    def name(self):
        return self.func.__name__

    def trigger(self):
        if self.is_running:
            return
        if callable(self.func):
            self.g = gevent.spawn(self.func, self.stop_event)
            if self.g.started:
                self.is_running = True

    def stop(self):
        if hasattr(self, 'g') and self.is_running:
            gevent.kill(self.g)
            self.is_running = False


class EventManager(object):
    """Events manager

    Example:

        from redis_sdk.event_manager import event_manager

        def task(stop_event):
            while not stop_event.is_set():
                do_stuff()

        event_manager.clear_event()  # clear all events already exists
        event_manager.register(task)
        event_manager.trigger(task)  # or `event_manager.trigger_all()`

        # here is gunicorn's main loop...
        # After some condition you want to stop *task* event, just do:
        event_manager.shutdown(task) # or `event_manager.set_events()` to stop
        all events

    Generally, all events will stop after gunicorn master stop.

    Note:
      In *task* func, there must be IO operation or `gevent.sleep()` explicitly
      to switch greenlet.

    """

    def __init__(self):
        """Events manager.
        Initialize a global *gevent.event.Event* to manager all greenlets.
        Initialize a dict to store all events registered.
        """
        self.stop_event = gevent.event.Event()
        self.events = {}

    def register(self, func):
        """Same function only register once.
        Rather than following situation:

          class Parent(object):
              def __init__(self):
                  event_manager.register(self.task)

              def task(self):
                  do_stuff()

          class Child(Parent):
              pass

        This will register two events:
          ``Bound method Parent.task of <xx.xx>``
          ``Bound method Child.task of <xx.xx>``
        """
        if func not in self.events:
            self.events[func] = Event(func, self.stop_event)

    def trigger(self, func):
        """Trigger given func to run as a greenlet"""
        self.events[func].trigger()

    def trigger_all(self):
        """Trigger all func in manager to run"""
        for func in self.events:
            self.trigger(func)

    def clear(self):
        """Clear events in manager"""
        self.events.clear()

    def clear_event(self):
        """Set *gevent.event.Event* False"""
        self.stop_event.clear()

    def shutdown(self, func):
        """Stop given func event"""
        self.events[func].stop()

    def set_events(self):
        """Stop all events"""
        if not self.stop_event.is_set():
            self.stop_event.set()  # set event True

event_manager = EventManager()
