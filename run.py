from tornado.ioloop import IOLoop
from app import Application

app = Application()
app.listen(8080)
IOLoop.instance().start()