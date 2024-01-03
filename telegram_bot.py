import telegram
import asyncio
import secret

bot = telegram.Bot(token=secret.token)


async def getUpdate() :
    msg = await bot.getUpdates()
    for data in msg :
        print(data)


asyncio.run(getUpdate())