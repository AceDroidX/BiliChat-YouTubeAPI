# WS server example

import asyncio
import websockets
import livechat
import logging
import json


async def wsserver(websocket, path):
    logging.info('wsserver已启动:'+str(websocket.remote_address)+path)
    roomid = await websocket.recv()
    chat = livechat.LiveChatProcessor(roomid)
    try:
        while not websocket.closed:
            msgjson = await chat.getchat()
            logging.info('websocket.text:'+str(msgjson))
            await websocket.send(str(msgjson))
    except websockets.ConnectionClosed as e:
        logging.error("err:"+'websockets.ConnectionClosed')
    finally:
        logging.info('chat已关闭')
        chat.terminate()

start_server = websockets.serve(wsserver, "0.0.0.0", 8085)
