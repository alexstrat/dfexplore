from tornado import httpserver
from tornado import gen
import tornado.web

# Sqlalchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import config
import models

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

class MainHandler(BaseHandler):
    def get(self):
        ws = self.db.query(models.Workspace).first()
        self.write('Hello, world %s' % ws.name)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/?", MainHandler)
        ]
        tornado.web.Application.__init__(self, handlers)

        engine = create_engine(config.SQLALCHEMY_DATABASE_URI, convert_unicode=True, echo=config.DEBUG)
        models.init_db(engine)
        self.db = scoped_session(sessionmaker(bind=engine))
