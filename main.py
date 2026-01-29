import os
import logging
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import ValidationError

# Sozlamalarni Railway Variables'dan o'qiymiz
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID') # O'zingizning ID raqamingiz
CHANNELS = ["@SizningKanalingiz"] # Majburiy a'zolik kanali (agar kerak bo'lsa)

logging.basicConfig(level=logging.INFO)

try:
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)
except ValidationError:
    print("XATO: Bot tokeni noto'g'ri!")
    exit()

# Ma'lumotlar bazasini yaratish
db = sqlite3.connect("anime.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS files (code TEXT PRIMARY KEY, file_id TEXT)")
db.commit()

# Majburiy a'zolikni tekshirish funksiyasi
async def check_sub(user_id):
    # Agar kanal ulamasangiz buni o'chirib qo'yish mumkin
    # Hozircha bu oddiy True qaytaradi
    return True

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer(f"👋 Salom {message.from_user.full_name}!\n\nAnime ko'rish uchun kodni yuboring.\n\nMasalan: 001")

# ADMIN uchun: Video yuklash (Video tagiga kod yozib yuboring)
@dp.message_handler(content_types=['video', 'document'])
async def add_anime(message: types.Message):
    if str(message.from_user.id) == str(ADMIN_ID):
        if message.caption:
            code = message.caption.strip()
            file_id = message.video.file_id if message.video else message.document.file_id
            
            cursor.execute("INSERT OR REPLACE INTO files VALUES (?, ?)", (code, file_id))
            db.commit()
            await message.reply(f"✅ Saqlandi!\nKod: {code}\nID: {file_id}")
        else:
            await message.reply("⚠️ Xato! Videoning 'izoh' (caption) qismiga kod yozing.")
    else:
        await message.answer("Siz admin emassiz!")

# FOYDALANUVCHI uchun: Kodni tekshirish va videoni yuborish
@dp.message_handler()
async def get_anime(message: types.Message):
    code = message.text.strip()
    
    # Ma'lumotlar bazasidan qidirish
    cursor.execute("SELECT file_id FROM files WHERE code = ?", (code,))
    result = cursor.fetchone()
    
    if result:
        await message.answer("Topildi! Yuklanmoqda...")
        await bot.send_video(message.chat.id, result[0], caption=f"🎬 Anime kodi: {code}\n\n@SizningKanalingiz")
    else:
        await message.answer("❌ Bu kod bo'yicha anime topilmadi. Kodni to'g'ri yozganingizni tekshiring.")

if __name__ == '__main__':
    print("Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)
