import asyncio
import logging
import livechat


class LiveChatManager:
    chatList = {}

    def __init__(self):
        pass

    def get(self, videoid):
        if videoid in self.chatList:
            self.chatList[videoid]['using']+=1
            return self.chatList[videoid]['chat']
        self.chatList[videoid] = {
            'chat': livechat.LiveChatProcessor(videoid), 'using': 1}
        return self.chatList[videoid]['chat']

    def terminate(self, videoid):
        if videoid in self.chatList:
            self.chatList[videoid]['using']-=1
            if self.chatList[videoid]['using']<=0:
                self.chatList[videoid]['chat'].terminate()
                self.chatList.pop(videoid)
                logging.info(f'[{videoid}]chat已关闭')
            return True
        return False
