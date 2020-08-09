import asyncio
import logging
import tornado
import sys,os,inspect
sys.path.append(os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe()))))
import wsserver
import livechat

routes = [
    (r'/.*', wsserver.wsserver)
]


def run_server():
    host, port = ('0.0.0.0', 8085)
    app = tornado.web.Application(
        routes,
        websocket_ping_interval=10,
        debug=True,
        autoreload=False
    )
    try:
        app.listen(port, host)
    except OSError:
        logger.warning('Address is used %s:%d', host, port)
        return
    logging.info('Server started: %s:%d', host, port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    LOG_FORMAT = "%(asctime)s[%(levelname)s]%(threadName)s--%(name)s>%(message)s"
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    run_server()
