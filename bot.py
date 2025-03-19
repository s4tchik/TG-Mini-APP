import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import json

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Конфигурация бота
API_TOKEN = '1'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Команда /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Добро пожаловать! Используйте /miniapp для открытия MiniApp.")

# Команда /miniapp
@dp.message_handler(commands=['miniapp'])
async def open_miniapp(message: types.Message):
    await message.answer(
        "Откройте MiniApp:",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(
                "Открыть MiniApp",
                web_app=types.WebAppInfo(url="file:///C:Users/Sat/Desktop/BotMiniAPPTG/miniapp.html")  # Укажите путь к вашему miniapp.html
            )
        )
    )

# Обработка данных из MiniApp
@dp.message_handler(content_types=['web_app_data'])
async def handle_web_app_data(message: types.Message):
    data = message.web_app_data.data
    parsed_data = json.loads(data)

    if parsed_data['action'] == 'add_expense':
        amount = parsed_data['amount']
        description = parsed_data['description']
        await message.answer(f"Расход {amount} добавлен: {description}")
    else:
        await message.answer(f"Получены данные из MiniApp: {parsed_data}")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
