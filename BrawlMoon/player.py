import re


from .basis import BrawlType
from .enums import URLS
from .brawler import Brawler


class BrawlPlayer(BrawlType):
    '''
    A Handler for Brawl Stars Player
    call coroutine update to update the cache
    '''

    def __init__(self, client, tag):
        super().__init__(client)
        self.tag = tag
        self.updated = False

    def __repr__(self):
        return self.name

    async def update(self, data=None):
        '''
        Updates the cached attributes
        '''
        self.updated = True
        if not data:
            hook = await self.request(
                str(URLS.PLAYERS.value) + str(self.tag)
                )

            data = hook.json

        async def camel_to_snake(name):
            name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
   
        self.club_tag = data.pop('club').get('tag')
        self.icon_id = data.pop('icon').get('id')

        my_brawlers = []

        for brawler in data.pop('brawlers'):
            my_brawlers.append(Brawler(brawler))

        self.brawlers = my_brawlers

        for k in data.keys():
            snake = await camel_to_snake(k)
            setattr(self, snake, data[k])
        return
        