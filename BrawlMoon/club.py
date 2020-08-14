import re

from .basis import BrawlType
from .enums import URLS

class BrawlClub(BrawlType):
    '''
    A Handler for Brawl Stars Club
    call coroutine update to update the cached attributes
    BrawlClub.updated: False if coroutine update was never called
    BrawlClub.request: shorthand for BrawlClub.client.request
    BrawlClub.__repr__: returns BrawlClub.name if update was fetched otherwise raises attribute error
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
                str(URLS.CLUBS.value) + str(self.tag)
                )

            data = hook.json

        async def camel_to_snake(name):
            name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

        list_members = data.pop('members')

        new_list_members = []

        for member in list_members:
            new_list_members.append(await self.client._nocacheplayer(member['tag']))

        self.members = new_list_members

        for k in data.keys():
            snake = await camel_to_snake(k)
            setattr(self, snake, data[k])

        return