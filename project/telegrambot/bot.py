from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import threading
import aiohttp
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Укажите ваш токен из переменных окружения
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("Токен Telegram API не найден. Убедитесь, что переменная API_TOKEN установлена.")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# Определяем состояния для FSM
class WeatherStates(StatesGroup):
    waiting_for_cities = State()
    waiting_for_days = State()

# Абсолютный путь к каталогу с изображениями
IMAGE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "website", "image")
)

# Функция запуска локального веб-сервера
def start_local_server(directory, port=8000):
    try:
        os.chdir(directory)
        handler = SimpleHTTPRequestHandler
        httpd = TCPServer(("", port), handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        print(f"Локальный сервер запущен на http://localhost:{port}")
        return httpd
    except Exception as e:
        print(f"Ошибка при запуске сервера: {e}")
        raise

# Асинхронная функция для запроса к API
async def connection(cities, day):
    url = "http://127.0.0.1:5000/api/weather"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={'cities': cities, 'day': day}, timeout=10) as response:
                if response.status == 200:
                    return await response.json()
                return {"error": f"Ошибка сервера: {response.status}"}
    except asyncio.TimeoutError:
        return {"error": "Время ожидания ответа истекло. Повторите попытку."}
    except Exception as e:
        return {"error": f"Произошла ошибка: {e}"}

# Генерация и отправка результатов
async def send_weather_results(chat_id, cities, day):
    weather_data = await connection(cities, day)
    if "error" in weather_data:
        await bot.send_message(chat_id, f"Ошибка при запросе данных: {weather_data['error']}")
        return

    for city, data in weather_data.items():
        color_marker = {'red': '🔴', 'yellow': '🟡', 'green': '🟢'}.get(data['color'], '⚪')
        message = (
            f"🏙 {city} \n"
            f"{color_marker} - {data['message']}\n"
            f"{data['spec']}"
        )
        img_url = f"http://localhost:8000/{data['img1']}"

        # Отправляем сообщение с текстом и ссылкой на изображение
        await bot.send_message(chat_id, f"{message}\nСсылка на изображение: {img_url}")

# Команда /start
@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Добро пожаловать! Я помогу вам узнать прогноз погоды для вашего маршрута. "
        "Используйте команду /help, чтобы узнать, как со мной работать."
    )

# Команда /help
@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "/start - начать работу с ботом\n"
        "/help - справка по командам\n"
        "/weather - узнать прогноз погоды для маршрута\n"
    )

# Команда /weather
@router.message(Command("weather"))
async def start_weather_command(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Завершить", callback_data="finish_input")]
        ]
    )
    await message.answer(
        "Введите названия городов по одному. Когда закончите, нажмите 'Завершить'.",
        reply_markup=keyboard
    )
    await state.update_data(cities=[])  # Инициализируем список городов
    await state.set_state(WeatherStates.waiting_for_cities)

# Обработка ввода городов
@router.message(WeatherStates.waiting_for_cities)
async def handle_city_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cities = data.get("cities", [])
    cities.append(message.text)  # Добавляем город в список
    await state.update_data(cities=cities)
    await message.answer(f"Город '{message.text}' добавлен. Введите следующий город или нажмите 'Завершить'.")

# Обработка нажатия кнопки "Завершить"
@router.callback_query(F.data == "finish_input")
async def handle_finish_input(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cities = data.get("cities", [])
    await callback.message.edit_text(
        "Теперь выберите временной интервал (1 = сегодня, 2 = завтра, ...):",
        reply_markup=generate_number_keyboard()
    )
    await state.set_state(WeatherStates.waiting_for_days)

# Генерация инлайн-клавиатуры с числами от 1 до 5
def generate_number_keyboard():
    buttons = [
        [InlineKeyboardButton(text=str(i), callback_data=f"day_{i}")] for i in range(1, 6)
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Обработка выбора числа
@router.callback_query(F.data.startswith("day_"))
async def handle_day_selection(callback: CallbackQuery, state: FSMContext):
    day = int(callback.data.split("_")[1])  # Извлекаем выбранное число
    data = await state.get_data()
    cities = data.get("cities", [])

    # Отправляем результаты погоды
    await send_weather_results(callback.message.chat.id, cities, day)

    # Завершаем
    await state.clear()
    await callback.message.edit_text("Данные по погоде отправлены.")
    await callback.answer()  # Закрываем уведомление о нажатии кнопки

# Регистрация роутера
dp.include_router(router)

# Запуск бота
async def main():
    port = 8000
    server = start_local_server(IMAGE_DIR, port=port)  # Запускаем сервер при старте приложения
    try:
        await dp.start_polling(bot, port=8081)
    finally:
        server.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
