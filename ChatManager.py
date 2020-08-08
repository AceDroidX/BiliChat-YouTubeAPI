import asyncio
import logging
import livechat
import youtube_util


class LiveChatManager:
    chatList = {}

    def __init__(self):
        pass

    async def add(self, id, wsserver):
        logging.debug(f'LiveChatManager.add.id:{id}')
        while True:
            videoid = await youtube_util.getLiveVideoId(id)  # debug
            if videoid is None:
                await asyncio.sleep(10)
                continue
            else:
                break
        chat = self.getChat(videoid, wsserver)
        wsserver.set_chat(chat)

    def getChat(self, videoid, msghandler):
        if videoid in self.chatList:
            self.chatList[videoid]['using'] += 1
            return self.chatList[videoid]['chat']
        self.chatList[videoid] = {
            'chat': livechat.LiveChatProcessor(videoid, msghandler), 'using': 1}
        return self.chatList[videoid]['chat']

    def terminate(self, videoid):
        if videoid in self.chatList:
            self.chatList[videoid]['using'] -= 1
            if self.chatList[videoid]['using'] <= 0:
                self.chatList[videoid]['chat'].terminate()
                self.chatList.pop(videoid)
                logging.info(f'[{videoid}]chat已关闭')
            return True
        return False
