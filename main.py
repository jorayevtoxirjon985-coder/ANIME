import logging
import sqlite3
from aiogram import Bot, Dispatcher, executor, types

# Bot tokeningizni kiriting
API_TOKEN = 'BOT_TOKENINGIZ'
ADMIN_ID = 12345678  # O'zingizning Telegram ID'ngizni kiriting

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Ma'lumotlar bazasini sozlash
conn = sqlite3.connect('anime_bot.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS anime 
                  (code TEXT PRIMARY KEY, file_id TEXT)''')
conn.commit()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Anime kodini yuboring va men sizga videoni topib beraman.")

# Admin uchun anime qo'shish funksiyasi (Format: kod + video yuboriladi)
@dp.message_handler(content_types=['video', 'document'], user_id=ADMIN_ID)
async def add_anime(message: types.Message):
    if message.caption:
        code = message.caption.strip()
        file_id = message.video.file_id if message.video else message.document.file_id
        
        try:
            cursor.execute("INSERT OR REPLACE INTO anime (code, file_id) VALUES (?, ?)", (code, file_id))
            conn.commit()
            await message.answer(f"✅ Tayyor! Kod: {code} saqlandi.")
        except Exception as e:
            await message.answer(f"Xatolik: {e}")
    else:
        await message.answer("Iltimos, videoni tagiga kodni yozib yuboring!")

# Foydalanuvchi kod yozganda qidirish
@dp.message_handler()
async def search_anime(message: types.Message):
    code = message.text.strip()
    cursor.execute("SELECT file_id FROM anime WHERE code=?", (code,))
    result = cursor.fetchone()
    
    if result:
        await bot.send_video(message.chat.id, result[0], caption=f"Kodingiz bo'yicha anime: {code}")
    else:
        await message.answer("❌ Afsuski, bu kod bo'yicha hech narsa topilmadi.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
