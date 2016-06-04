from base import BaseHandler
from .. import models

class HelloHandler(BaseHandler):
    def get(self):
        self.render('index.html')

default_handlers = [
    (r"/?", HelloHandler)
]
