import httpx
import json
import time
import asyncio

def timed(func):
    async def wrapper(*args, **kwargs):
        start = time.time()
        await func(*args, **kwargs)
        stop = time.time() - start
        print(f"time taken {stop}")
    return wrapper

class FantasyBot:
    def __init__(self):
        self.base_url = "https://fantasy.premierleague.com/api/"
        self.standings = "{}leagues-classic/{}/standings/"
    
    async def get_overall_standings(self, page):
        print(f"geting page {page}")
        params = {"page":page}
        async with httpx.AsyncClient() as client:
            data = await client.get(self.standings.format(self.base_url, 314), params=params)
            #data = json.dumps(data, indent=4)
            print(data)
        return data
    
    @timed
    async def get_all_pages_overall_standings(self):
        data = await asyncio.gather(*map(self.get_overall_standings, range(1,21)))
        return data



if __name__ == "__main__":
    asyncio.run(FantasyBot().get_all_pages_overall_standings())