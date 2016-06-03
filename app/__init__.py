import tornado.web
from tornado.ioloop import PeriodicCallback

# Sqlalchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from pyee import EventEmitter

import config
import handlers as app_handlers


class Application(tornado.web.Application):
    def __init__(self):
        handlers = app_handlers.get_all()

        tornado.web.Application.__init__(self, handlers)

        engine = create_engine(config.SQLALCHEMY_DATABASE_URI, convert_unicode=True, echo=config.DEBUG)
        models.init_db(engine)
        self.db = scoped_session(sessionmaker(bind=engine))
        self.db_ee = EventEmitter()

        # test
        heartbeat = PeriodicCallback(lambda: self.db_ee.emit('event', {'type': 'heartbeat'}), 1000.)
        heartbeat.start()
