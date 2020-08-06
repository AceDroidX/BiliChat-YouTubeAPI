# WS server example

import asyncio
import websockets
import livechat
import youtube_util
import logging
import json
import ChatManager
import time


async def wsserver(websocket, path):
    try:
        chat = None
        logging.info('wsserver已启动:'+str(websocket.remote_address)+path)
        roomid = await websocket.recv()
        while True:  # 此处需要重构
            if websocket.closed:
                raise websockets.ConnectionClosedError(
                    1002, 'websockets.ConnectionClosedError')
            videoid = await youtube_util.getLiveVideoId(roomid) #debug
            if videoid is None:
                await asyncio.sleep(10)
                continue
            else:
                break
        chat = manager.get(videoid)
        msgtemp = None
        while not websocket.closed:
            msgjson = await chat.getchat()
            if msgjson is None or msgjson == msgtemp:
                await asyncio.sleep(0.1)
                continue
            if time.time()-msgjson['timestamp'] > 1:
                await asyncio.sleep(0.1)
                continue
            msgtemp = msgjson
            logging.info('websocket.text:'+str(msgjson))
            await websocket.send(json.dumps(msgjson, ensure_ascii=False))
    except websockets.ConnectionClosed as e:
        logging.error("err:"+'websockets.ConnectionClosed', exc_info=True)
    except BaseException as e:
        logging.error("err:"+str(e), exc_info=True)
    finally:
        if not websocket.closed:
            websocket.close()
        if not chat is None:
            manager.terminate(videoid)

manager = ChatManager.LiveChatManager()
start_server = websockets.serve(wsserver, "0.0.0.0", 8085)
