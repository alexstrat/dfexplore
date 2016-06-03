from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.queues import Queue

from base import BaseHandler

class EventsHandler(BaseHandler):

    def initialize(self):
        self.data_queue = Queue()
        self.db_ee.on('event', self.add_to_data_queue)

        self.set_header('content-type', 'text/event-stream')
        self.set_header('cache-control', 'no-cache')

    def add_to_data_queue(self, data):
        self.data_queue.put(data)

    @gen.coroutine
    def publish(self, data):
        try:
            self.write('{}\n'.format(data))
            yield self.flush()
        except StreamClosedError:
            pass

    def on_connection_close(self):
        self.db_ee.remove_listener('event', self.add_to_data_queue)

    @gen.coroutine
    def get(self):
        while not self.request.connection.stream.closed():
            data = yield self.data_queue.get()
            yield self.publish(data)

default_handlers = [
    (r"/events", EventsHandler)
]
