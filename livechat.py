from pytchat import LiveChatAsync
import asyncio
import logging


class LiveChatProcessor:

    def __init__(self, videoid, msghandler, seektime=970):
        self.videoid = videoid
        self.msghandler = msghandler
        logging.info('videoid:'+videoid+' seektime:'+str(seektime))
        self.livechat = LiveChatAsync(
            video_id=videoid, callback=self.chatProcessor, seektime=seektime)

    # callback function (automatically called)
    async def chatProcessor(self, chatdata):
        logging.debug(f'[{self.videoid}]chatProcessor')
        for c in chatdata.items:
            # logging.debug('chatdata.items.c\ndatetime:'+c.datetime)
            if c.author.isChatModerator or c.author.isChatOwner:
                logging.info('Chat:'+c.author.name+'\n'+c.message)
                self.sendChat(self.chatRendererToJson(c))
            await chatdata.tick_async()

    def chatRendererToJson(self, c):
        return {'type': c.type, 'message': c.message, 'timestamp': c.timestamp, 'datetime': c.datetime,
                'author': {'name': c.author.name, 'channelId': c.author.channelId, 'imageUrl': c.author.imageUrl, 'isChatOwner': c.author.isChatOwner, 'isChatModerator': c.author.isChatModerator}}

    def sendChat(self, msg):
        self.msghandler.send_message(msg)

    def terminate(self):
        if not self.livechat is None:
            self.livechat.terminate()


def test_chat():
    chat = LiveChatProcessor('eoQPSpbl5bY', seektime=565)
    asyncio.get_event_loop().run_until_complete(chat.getchat())
    logging.debug('运行完毕')
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    LOG_FORMAT = "%(asctime)s[%(levelname)s]%(threadName)s--%(name)s>%(message)s"
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    print(channelId2videoId('UCC0i9nECi4Gz7TU63xZwodg'))
