# WS server example

import asyncio
import websockets
import livechat
import youtube_util
import logging
import json


async def wsserver(websocket, path):
    try:
        chat=None
        logging.info('wsserver已启动:'+str(websocket.remote_address)+path)
        roomid = await websocket.recv()
        while True:# 此处需要重构
            if websocket.closed:
                raise websockets.ConnectionClosedError(1002,'websockets.ConnectionClosedError')
            videoid = await youtube_util.getLiveVideoId(roomid)
            if videoid is None:
                await asyncio.sleep(10)
                continue
            else:
                break
        chat = livechat.LiveChatProcessor(videoid)
        while not websocket.closed:
            msgjson = await chat.getchat()
            if msgjson is None:
                await asyncio.sleep(0.1)
                continue
            logging.info('websocket.text:'+str(msgjson))
            await websocket.send(json.dumps(msgjson, ensure_ascii=False))
    except websockets.ConnectionClosed as e:
        logging.error("err:"+'websockets.ConnectionClosed')
    except BaseException as e:
        logging.error("err:"+str(e))
    finally:
        if not websocket.closed:
            websocket.close()
        if not chat is None:
            chat.terminate()
            logging.info('chat已关闭')

start_server = websockets.serve(wsserver, "0.0.0.0", 8085)
