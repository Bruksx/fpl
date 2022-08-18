from bot import FantasyBot
import asyncio

bot = FantasyBot()

async def get_page(page):
    return await bot.get_overall_standings(page)

print(asyncio.run(get_page(2)))