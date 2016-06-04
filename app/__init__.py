import os

import tornado.web
from tornado.ioloop import PeriodicCallback

# Sqlalchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import pyee

import config
import handlers as app_handlers



class EventEmitter(pyee.EventEmitter):
    def emit(self, event, *args, **kwargs):
        super(EventEmitter, self).emit(event, *args, **kwargs)
        super(EventEmitter, self).emit('*', event, *args, **kwargs)


TEMPLATE_PATH = os.path.join(config.BASE_DIR, 'app/templates')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = app_handlers.get_all()

        tornado.web.Application.__init__(self,
            handlers,
            template_path = TEMPLATE_PATH,
            debug = config.DEBUG
        )

        engine = create_engine(config.SQLALCHEMY_DATABASE_URI, convert_unicode=True, echo=config.DEBUG)
        models.init_db(engine)
        self.db = scoped_session(sessionmaker(bind=engine))
        self.db_ee = EventEmitter()

        # test
        heartbeat = PeriodicCallback(lambda: self.db_ee.emit('heartbeat'), 1000.)
        heartbeat.start()
