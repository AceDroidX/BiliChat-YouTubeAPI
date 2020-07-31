from pytchat import LiveChatAsync
import time
import asyncio
import logging


class LiveChatProcessor:
    def __init__(self, roomid, seektime=0):
        logging.info('roomid:'+roomid+' seektime:'+str(seektime))
        self.queue = asyncio.Queue()
        self.livechat = LiveChatAsync(
            video_id=roomid, callback=self.chatProcessor, seektime=seektime)

    # callback function (automatically called)
    async def chatProcessor(self, chatdata):
        logging.debug('chatProcessor')
        for c in chatdata.items:
            logging.debug('chatdata.items.c\ndatetime:'+c.datetime)
            if c.author.isChatModerator or c.author.isChatOwner:
                logging.info('Chat:'+c.author.name+'\n'+c.message)
                msgjson = self.chatRendererToJson(c)
                await self.queue.put(msgjson)
            await chatdata.tick_async()

    def chatRendererToJson(self, c):
        return {'type': c.type, 'message': c.message, 'timestamp': c.timestamp, 'datetime': c.datetime,
         'author': {'name': c.author.name, 'channelId': c.author.channelId, 'imageUrl': c.author.imageUrl, 'isChatOwner': c.author.isChatOwner, 'isChatModerator': c.author.isChatModerator}}

    async def getchat(self):
        if self.queue.qsize()==0:
            return None
        msgjson = await self.queue.get()
        logging.debug('getchat:'+str(msgjson))
        return msgjson

    def terminate(self):
        self.livechat.terminate()

if __name__ == '__main__':
    LOG_FORMAT = "[%(asctime)s]%(levelname)s > %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    chat = LiveChatProcessor('eoQPSpbl5bY', seektime=565)
    asyncio.get_event_loop().run_until_complete(chat.getchat())
    logging.debug('运行完毕')
    asyncio.get_event_loop().run_forever()
