import config as cf
from aiogram import Bot, Dispatcher,types, executor
import logging
bot = Bot(token=cf.TOKEN_BOT)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler()
async def any_text_message(message:types.Message):
    print(message)
    await message.answer(f'Hi Pidor')









if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)