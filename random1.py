import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# 🔐 Токен твоего бота
API_TOKEN = "7860631728:AAEvQBS0DXvp-F0Xor7PLorjEp5uMZETk0w"
OWNER_ID = 6697710886  # Замени на свой Telegram ID

# Переменная для одноразового скрытого числа
one_time_number = None

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Получение имени/юзернейма отправителя
def format_user(user: types.User) -> str:
    return f"@{user.username}" if user.username else user.first_name

# Команда /random
@dp.message(Command("random"))
async def send_random(msg: types.Message):
    global one_time_number

    user_info = format_user(msg.from_user)
    number = one_time_number if one_time_number is not None else random.randint(1, 100)
    one_time_number = None  # сброс

    text = f"Պատահական Թիվ: {number}\nՀրամանը ուղարկեց՝ {user_info}"
    await msg.answer(text)

# Установка скрытого числа (только для владельца)
@dp.message()
async def set_hidden(msg: types.Message):
    global one_time_number
    if msg.from_user.id == OWNER_ID:
        try:
            number = int(msg.text)
            if 1 <= number <= 100:
                one_time_number = number
                await msg.answer("Թիվը պահպանված է։ Կցուցադրվի հաջորդ /random հրամանից")
        except:
            pass

# Запуск бота
async def main():
    # Устанавливаем доступные команды в Telegram
    await bot.set_my_commands([
        types.BotCommand(command="random", description="Պատահական թիվ 1-ից 100")
    ])
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())