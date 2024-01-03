import telegram
import asyncio
import secret

bot = telegram.Bot(token=secret.token)

# async def getUpdate() :
#     msg = await bot.getUpdates()
#     for data in msg :
#         print(data)

# asyncio.run(getUpdate())

async def send() :
    await bot.sendMessage(chat_id=secret.chat_id, text="테스트임")


event = asyncio.get_event_loop()
event.run_until_complete(send())
event.close()