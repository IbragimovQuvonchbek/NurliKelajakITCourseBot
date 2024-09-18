import asyncio
import logging
import os
import sys
from uuid import uuid4
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from aiogram import Bot, Dispatcher, F, html
from aiogram import types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ContentType
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
from functionsapi import get_student_info
from aiogram.types import FSInputFile


load_dotenv()

TOKEN = os.getenv("TOKEN")
dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(f"{html.bold("Assalomu Aleykum!\nO'quvchining natijasni bilish uchun ID raqamini jo'nating")}")


@dp.message(F.content_type == ContentType.TEXT)
async def handler_name(message: types.Message) -> None:
    text = message.text.upper()
    data = await get_student_info(text)
    if not data and data.get('error'):
        await message.reply(data['error'])
    else:
        student_info = (f"Ism: {data[0]['student']['first_name']}\n"
                        f"Familiya: {data[0]['student']['last_name']}\n"
                        f"Sinf: {data[0]['student']['grade']}\n"
                        f"Gruh: {data[0]['student']['group']}\n"
                        f"ID: {data[0]['student']['id_unique']}")
        builder = InlineKeyboardBuilder()
        keys = []
        builder.button(text="Jami",
                       callback_data=f"result_{"Jami"}_{text}")
        for result in data:
            if result['month'] not in keys:
                keys.append(result['month'])
                builder.button(text=result['month'],
                               callback_data=f"result_{result['month']}_{text}")
        await message.answer(student_info, reply_markup=builder.as_markup())

@dp.callback_query(lambda callback: callback.data.startswith('result_'))
async def options_test_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    text = callback.data.split('_')
    data = await get_student_info(text[-1].upper())
    month = text[1]
    response = ""
    total_percentage = 0
    times = 0
    if month == "Jami":
        months_arr = dict()
        for result in data:
            if months_arr.get(result['month']):
                months_arr[result['month']] += f"{result['number_of_questions']}/{result['result']} --- {round(result['result']/result['number_of_questions']*100)}%\n"
            else:
                months_arr[result['month']] = f"{result['month']}\n"
                months_arr[result['month']] += f"{result['number_of_questions']}/{result['result']} --- {round(result['result']/result['number_of_questions']*100)}%\n"
            total_percentage += round(result['result'] / result['number_of_questions'] * 100)
            times += 1

        months_arr_keys = months_arr.keys()
        for key in months_arr_keys:
            await callback.message.answer(months_arr[key])

    else:
        x = []
        y = []
        for result in data:
            if result['month'] == month:
                total_percentage += round(result['result']/result['number_of_questions']*100)
                y.append(round(result['result']/result['number_of_questions']*100))
                times += 1
                x.append(times)
                response += f"{result['number_of_questions']}/{result['result']} --- {round(result['result']/result['number_of_questions']*100)}%\n"
        await callback.message.answer(response)

        # try:
        #     plt.plot(x, y, marker='o', linestyle='-', color='b', label=f"{month} oyi o'zlashtirish natijasi")
        #
        #     plt.title(f"{month} oyi o'zlashtirish natijasi", fontsize=16)
        #     plt.xlabel('Test Tartib Raqami', fontsize=12)
        #     plt.ylabel('Foiz %', fontsize=12)
        #     plt.xticks(x, fontsize=10)
        #     plt.grid(True, which='both', linestyle='--', linewidth=0.7, alpha=0.7)
        #     file_name = uuid4()
        #     plt.savefig(f'linegraphs/{file_name}.png', dpi=300, bbox_inches='tight')
        #
        #     plt.close()
        #     photo = FSInputFile(f'linegraphs/{file_name}.png')
        #     await callback.message.answer_photo(photo, caption=f"{month} oyi o'zlashtirish natijasi")
        #     try:
        #         os.remove(f'linegraphs/{file_name}.png')
        #     except OSError as e:
        #         pass
        # except Exception as e:
        #     await callback.message.answer("Grafik chizishda xatolik")
        plt.plot(x, y, marker='o', linestyle='-', color='b', label=f"{month} oyi o'zlashtirish natijasi")

        plt.title(f"{month} oyi o'zlashtirish natijasi", fontsize=16)
        plt.xlabel('Test Tartib Raqami', fontsize=12)
        plt.ylabel('Foiz %', fontsize=12)
        plt.xticks(x, fontsize=10)
        plt.grid(True, which='both', linestyle='--', linewidth=0.7, alpha=0.7)
        file_name = uuid4()
        plt.savefig(f'linegraphs/{file_name}.png', dpi=300, bbox_inches='tight')

        plt.close()
        photo = FSInputFile(f'linegraphs/{file_name}.png')
        await callback.message.answer_photo(photo, caption=f"{month} oyi o'zlashtirish natijasi")
        try:
            os.remove(f'linegraphs/{file_name}.png')
        except OSError as e:
            pass

    await callback.message.answer(f"{month} -- {round(total_percentage/times, 2)}%")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())