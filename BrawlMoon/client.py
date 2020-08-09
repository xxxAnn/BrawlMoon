import asyncio
import json

import aiohttp

from .enums import URLS
from .resp import BrawlResponse
from .errors import APIError
from .player import BrawlPlayer
from .club import BrawlClub

class BrawlClient:
    '''
    Asynchronous client making requests to the Brawl Stars API
    '''
    
    def __init__(self, token, **kwargs):
        self.loop = kwargs.pop('loop', asyncio.get_event_loop())
        self._ratelimiting = kwargs.pop('ratelimit_handling', True)
        self.__authenticated = False
        self.lock = asyncio.Lock(loop=self.loop) if self._ratelimiting else None
        self.verbose = kwargs.pop('verbose', False)

        if kwargs:
            raise TypeError("unexpected keyword argument(s) %s" % list(kwargs.keys()))

        # Create the aiohttp.ClientSession
        self._session = aiohttp.ClientSession(loop=self.loop)

        # Create the headers
        self.__headers = {
            'Authorization': 'Bearer {}'.format(token),
            'User-Agent': 'BrawlMoon'
        }

    async def _request(self, method='GET', url=None):
        url = URLS.BASE.value + url
        if self.verbose:
            print("> Requesting '{}' <".format(url))
        async with self._session.request(method=method, url=url, headers=self.__headers) as resp:
            message = await resp.text()
            return BrawlResponse(status=resp.status, message=message)

    async def request(self, url):
        if self.lock:
            async with self.lock:
                await asyncio.sleep(.2)
                resp = await self._request(url=url)
        else:
            resp = await self._request(url=url)


        try:
            assert resp.status == 200
        except AssertionError:
            raise APIError(
                resp.status
                )
        return resp

    async def __verify_connection(self):
        resp = await self._request(url=URLS.BRAWLERS.value)
        try:
            assert resp.status == 200
        except AssertionError:
            raise APIError(
                resp.status
                )

        if self.verbose:
            print('> Successfully connected <')
        return True

    def run(self, callback=None):
        loop = self.loop
        async def start():
            _success = await self.__verify_connection()
            self.__authenticated = True
            if callback:
                try:
                    await callback()
                finally:
                    await self._session.close()

        def kill_loop(f):
            pass

        runner = asyncio.ensure_future(start(), loop=loop) 
        runner.add_done_callback(kill_loop)

        try:
            loop.run_forever()
        except:
            return
        finally:
            runner.remove_done_callback(kill_loop) # If we keep this it will be executed after the loop is stopped and raise an Error


    async def get_player(self, tag: str):
        if not isinstance(tag, str):
            raise TypeError(
                "Tag must be a str"
                )
        else:
            if not tag.startswith('#'):
                tag = "#" + tag
            tag = tag.replace('#', '%23')
            player = BrawlPlayer(client=self, tag=tag)
            await player.update()
            return player

    async def get_club(self, tag: str):
        if not isinstance(tag, str):
            raise TypeError(
                "Tag must be a str"
                )
        else:
            if not tag.startswith('#'):
                tag = "#" + tag
            tag = tag.replace('#', '%23')
            club = BrawlClub(client=self, tag=tag)
            await club.update()
            return club

    async def _nocacheplayer(self, tag: str):
        if not isinstance(tag, str):
            raise TypeError(
                "Tag must be a str"
                )
        else:
            if not tag.startswith('#'):
                tag = "#" + tag
            tag = tag.replace('#', '%23')
            return BrawlPlayer(client=self, tag=tag)
