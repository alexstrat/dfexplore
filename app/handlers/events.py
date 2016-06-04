from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.queues import Queue
import json

from base import BaseHandler

class EventsHandler(BaseHandler):

    def initialize(self):
        self.data_queue = Queue()
        self.db_ee.on('*', self.add_event_to_queue)

        self.set_header('content-type', 'text/event-stream')
        self.set_header('cache-control', 'no-cache')

    def add_event_to_queue(self, event, data=None, *args, **kwargs):
        self.data_queue.put((event, data))

    @gen.coroutine
    def publish(self, event, data):
        try:
            self.write('event: {}\n'.format(event))
            self.write('data: {}\n'.format(json.dumps(data)))
            self.write('\n')
            yield self.flush()
        except StreamClosedError:
            pass

    def on_connection_close(self):
        self.db_ee.remove_listener('*', self.add_event_to_queue)

    @gen.coroutine
    def get(self):
        while not self.request.connection.stream.closed():
            event, data = yield self.data_queue.get()
            yield self.publish(event, data)

default_handlers = [
    (r"/events", EventsHandler)
]
