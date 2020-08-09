import asyncio
import logging
import sys,os,inspect
sys.path.append(os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe()))))
import youtube_util
import livechat
class LiveChatManager:
    chatList = {}

    def __init__(self):
        pass

    async def add(self, id, wsserver):
        logging.debug(f'LiveChatManager.add.id:{id}')
        # videoid = id  # debug
        while True:
            videoid = await youtube_util.getLiveVideoId(id)  # debug
            if videoid is None:
                await asyncio.sleep(10)
                continue
            else:
                break
        chat = self.getChat(videoid)
        self.addwsserver(videoid, wsserver)
        wsserver.set_chat(chat)

    def addwsserver(self, videoid, wsserver):
        if not 'wsserver' in self.chatList[videoid]:
            self.chatList[videoid]['wsserver'] = []
        self.chatList[videoid]['wsserver'].append(wsserver)

    def getChat(self, videoid):
        if videoid in self.chatList:
            self.chatList[videoid]['using'] += 1
            return self.chatList[videoid]['chat']
        self.chatList[videoid] = {
            'chat': livechat.LiveChatProcessor(videoid, self), 'using': 1}
        return self.chatList[videoid]['chat']

    def send_message(self, msg, videoid):
        if videoid in self.chatList:
            for wsserver in self.chatList[videoid]['wsserver']:
                wsserver.send_message(msg)
        else:
            logging.warning(
                f'LiveChatManager.send_message:videoid not in self.chatList')

    def terminate(self, videoid, wsserver):
        if videoid in self.chatList:
            self.chatList[videoid]['wsserver'].remove(wsserver)
            self.chatList[videoid]['using'] -= 1
            if self.chatList[videoid]['using'] <= 0:
                self.chatList[videoid]['chat'].terminate()
                self.chatList.pop(videoid)
                logging.info(f'[{videoid}]chat已关闭')
            return True
        return False
