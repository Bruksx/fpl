import httpx
import json
import time
import asyncio

sem = asyncio.Semaphore(10)

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
        self.detailed_data = "{}entry/{}/"
        self.history = "{}entry/{}/history/"
        self.gameweek_history = "entry/{}/event/{}/picks/"
        self.limits = httpx.Limits(max_keepalive_connections=1, max_connections=1)
    
    async def get_overall_standings(self, page):
        print(f"geting page {page}")
        with open("json/overall.json") as f:
            fetched = json.loads(f.read())
        page_found = False
        for p in fetched:
            if p["standings"]["page"] == page:
                page_found = True
        if not page_found:
            print(f"geting {page}")
            params = {"page_standings":page}
            async with sem:
                async with httpx.AsyncClient() as client:
                    data = await client.get(self.standings.format(self.base_url, 314), params=params, timeout=None)
                    data = data.json()
            return data
    
    #@timed
    async def get_all_pages_overall_standings(self):
        data = await asyncio.gather(*map(self.get_overall_standings, range(1,201)))
        data = [i for i in data if i != None]
        with open("json/overall.json", "r") as f:
            old_data = json.loads(f.read())
        print(data + old_data)
        with open("json/overall.json", "w") as f:
            f.write(json.dumps(old_data + data, indent=4))
        return data
    
    async def get_player_history(self, id):
        async with sem:
            async with httpx.AsyncClient() as client:
                try:
                    data = await client.get(self.history.format(self.base_url, id), timeout=None)
                    history = data.json()["past"]
                    return history
                except httpx.ConnectError:
                    print("connect error, sleeping")
                    time.sleep(10)
                    await self.get_player_history(id)
    
    async def get_average_rank_previous_seasons(self, id):
        seasons = 4
        print(f"geting history of {id}")
        history = await self.get_player_history(id)
        print(f"fetched history of {id}")
        try:
            length = len(history)
        except TypeError:
            length = 0
        if length >= seasons:
            last_4_seasons = history[-seasons:]
            ranks = [seasons["rank"] for seasons in last_4_seasons]
            average = int(sum(ranks)/seasons)
        else:
            average = None
        return average
    
    def get_ids_from_file(self):
        with open("json/overall.json") as f:
            data = json.loads(f.read())
        ids = []
        for page in data:
            results = page["standings"]["results"]
            for player in results:
                ids.append(player["entry"])
        return ids
    
    @timed
    async def get_all_average_rank_of_previous_seasons(self):
        ids = self.get_ids_from_file()
        data = {}
        average_rank = await asyncio.gather(*map(self.get_average_rank_previous_seasons,ids[:1001]))
        li = list(average_rank)
        ranked = [i for i in li if i != None]
        data["none"] = li.count(None)
        data["average_rank"] = int(sum(ranked)/len(ranked))
        print(data)
        #return data

    


if __name__ == "__main__":
    bot = FantasyBot()
    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #print(asyncio.run(bot.get_average_rank_previous_seasons(34566, 5)))
    #print(asyncio.run(bot.get_all_pages_overall_standings()))
    #print(bot.get_ids_from_file())
    print(asyncio.run(bot.get_all_average_rank_of_previous_seasons()))
