import asyncio
from bot.bot import bot
import sys
import os

async def main():
    await bot.load_extension('bot.cogs.todo_cog')
    await bot.load_extension('bot.cogs.test_cog')
    await bot.load_extension('bot.cogs.study_cog')
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
