import os
import sys
from aiogram import Bot

# Railway Variables bo'limidan o'qiymiz
API_TOKEN = os.getenv('BOT_TOKEN')

# Xatolikni tekshirish uchun qo'shimcha qism
if not API_TOKEN:
    print("!!! DIQQAT: BOT_TOKEN topilmadi. Railway Variables bo'limini tekshiring !!!")
    sys.exit(1)

print(f"Token olindi: {API_TOKEN[:5]}...{API_TOKEN[-5:]}") # Xavfsiz tekshirish

try:
    bot = Bot(token=API_TOKEN)
except Exception as e:
    print(f"Token xatosi: {e}")
    sys.exit(1)
