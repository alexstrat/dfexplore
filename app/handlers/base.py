import tornado.web
import json

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def write_json(self, response):
        self.set_header('Content-Type', 'application/json')
        output = json.dumps(response)
        self.write(output)