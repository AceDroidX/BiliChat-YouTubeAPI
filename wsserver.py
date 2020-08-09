import asyncio
import logging
import json
import time
import tornado.websocket
import sys,os,inspect
sys.path.append(os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe()))))
import livechat
import ChatManager


class wsserver(tornado.websocket.WebSocketHandler):
    chat = None

    def set_chat(self, chat):
        self.chat = chat
        self.videoid = chat.videoid

    def open(self):
        logging.info(
            f'wsserver已启动:{self.request.remote_ip}{self.request.path}')

    def on_message(self, message):
        if self.chat is None:
            asyncio.ensure_future(manager.add(message, self))

    def on_close(self):
        # if not websocket.closed:
        #     websocket.close()
        if not self.chat is None:
            manager.terminate(self.chat.videoid, self)

    def send_message(self, message):
        try:
            self.write_message(message)
        except tornado.websocket.WebSocketClosedError:
            self.on_close()

    def check_origin(self, origin):
        return True


manager = ChatManager.LiveChatManager()
