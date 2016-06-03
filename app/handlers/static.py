import os
import tornado.web

import config

static_path = os.path.join(config.BASE_DIR, 'app/static')

default_handlers = [
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": static_path})
]
