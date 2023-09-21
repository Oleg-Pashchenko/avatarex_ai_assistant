import asyncio
import logging
import os

import db
import openai_api
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
import dotenv

dotenv.load_dotenv()
dp = Dispatcher()


@dp.message(CommandStart())
async def on_start(message: types.Message):
    await message.answer("Привет!\nНапишите ваш запрос, он должен включать следующую информацию:"
                         "\n1) Количество метров"
                         "\n2) Количество спален"
                         "\n3) Бюджет"
                         "\n4) Локацию (город)"
                         "\n5) Тип (вилла или апарт)"
                         "\n\nПример: Я хочу виллу в Altıntaş с 4 спальнями стоимостью до 500000$ на 50 метров")


@dp.message()
async def on_all_messages(message: types.Message):
    openai_response = openai_api.get_keywords_values(message.text)
    if not openai_response['is_ok']:
        return await message.answer(f'{message.from_user.first_name}, ваш запрос не был обработан.\n'
                                    f'К сожалению мы не смогли точно разобрать критерии вашего поиска.\nПожалуйста,'
                                    f'напишите запрос подробнее и согласно критериям.')
    await message.answer(f'[Debug data] Openai Response:\n{openai_response}')
    location, bedrooms = openai_response['args']['location'], openai_response['args']['bedrooms']
    price = openai_response['args']['price']
    meters, obj_type = openai_response['args']['meters'], openai_response['args']['type']
    location = location.replace('Antalia', 'Antalya')
    db_response = db.get_apartment_offers(location, price, bedrooms, meters, 'is_building_ready', obj_type)
    if not db_response['is_ok']:
        return await message.answer(f'{message.from_user.first_name}, ваш запрос не был обработан.\n'
                                    f'К сожалению мы не смогли точно разобрать город.\nПожалуйста,'
                                    f'напишите запрос подробнее и согласно критериям.')
    args = db_response['obj']
    response_text = f"{message.from_user.first_name}, по вашему запросу было найдено {len(args)} результатов."
    if len(args) == 0:
        return await message.answer(response_text)
    for a in args:
        response_text += f"\nhttps://tolerance-homes.ru/objects/{a[0]}"
    await message.answer(response_text)


async def main():
    bot = Bot(os.getenv('TELEGRAM_TOKEN'), parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
