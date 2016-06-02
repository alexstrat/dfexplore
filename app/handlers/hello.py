from base import BaseHandler
from .. import models

class HelloHandler(BaseHandler):
    def get(self):
        ws = self.db.query(models.Workspace).first()
        self.write('Hello, world %s' % ws.name)

default_handlers = [
    (r"/?", HelloHandler)
]
