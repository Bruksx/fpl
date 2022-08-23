from bot import FantasyBot
import asyncio
import json

bot = FantasyBot()

async def get_page(page):
    return await bot.get_overall_standings(page)

def checkjson():
    with open("json/overall.json")as f:
        data = json.loads(f.read())
    print(len(data))


print(asyncio.run(bot.get_player_history(6209589)))

#print(asyncio.run(get_page(2)))
#print(checkjson())