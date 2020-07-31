import wsserver
import livechat
import asyncio
import logging


if __name__ == '__main__':
    LOG_FORMAT = "[%(asctime)s]%(levelname)s > %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    logging.info('eventloop已启动')
    asyncio.get_event_loop().run_until_complete(wsserver.start_server)
    asyncio.get_event_loop().run_forever()