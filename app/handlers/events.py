from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.concurrent import Future

from base import BaseHandler

class DataBuffer(object):
    def __init__(self, ee):
        self.ee = ee
        self.ee.on('event', self.new_data)

        self.waiters = set()

    def wait_for_data(self):
        # Construct a Future to return to our caller.  This allows
        # wait_for_messages to be yielded from a coroutine even though
        # it is not a coroutine itself.  We will set the result of the
        # Future when results are available.
        result_future = Future()
        self.waiters.add(result_future)
        return result_future

    def cancel_wait(self, future):
        self.waiters.remove(future)
        # Set an empty result to unblock any coroutines waiting.
        future.set_result([])

    def new_data(self, data):
        for future in self.waiters:
            future.set_result(data)
        self.waiters = set()

    def close(self):
        for future in self.waiters.copy():
            self.cancel_wait(future)
        self.ee.remove_listener('event', self.new_data)

class EventsHandler(BaseHandler):

    def initialize(self):
        self.buffer = DataBuffer(self.db_ee)

        self.set_header('content-type', 'text/event-stream')
        self.set_header('cache-control', 'no-cache')

    @gen.coroutine
    def publish(self, data):
        try:
            self.write('{}\n'.format(data))
            yield self.flush()
        except StreamClosedError:
            pass

    def on_connection_close(self):
        self.buffer.close()

    @gen.coroutine
    def get(self):
        while not self.request.connection.stream.closed():
            self.future = self.buffer.wait_for_data()
            data = yield self.future
            yield self.publish(data)

default_handlers = [
    (r"/events", EventsHandler)
]
