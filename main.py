import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import google.generativeai as genai

# --- SOZLAMALAR ---
TOKEN = os.getenv("BOT_TOKEN")
AI_KEY = os.getenv("GOOGLE_API_KEY")

# Gemini AI ni sozlash
genai.configure(api_key=AI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# --- ASOSIY MENYU (Barcha 11 ta tugma) ---
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    # Tugmalarni tartib bilan qo'shish
    markup.add(KeyboardButton("🧠 AI bilan suhbat"))
    markup.add(KeyboardButton("📊 Byudjet rejasi"), KeyboardButton("📈 Investitsiya"))
    markup.add(KeyboardButton("🧮 Kalkulyatorlar"), KeyboardButton("📉 Kurslar"))
    markup.add(KeyboardButton("🏆 Bilimingizni sinang"), KeyboardButton("💹 Valyuta kurslari"))
    markup.add(KeyboardButton("💰 Balans"), KeyboardButton("🥇 Reyting"))
    markup.add(KeyboardButton("📈 Statistika"), KeyboardButton("📅 Kunlik reja"))
    
    return markup

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}! 👋\n\n"
        "**FinEduPay Smart AI** platformasiga xush kelibsiz!\n"
        "Men sizning shaxsiy moliyaviy yordamchingizman. "
        "Kerakli bo'limni tanlang:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

# --- TUGMALAR UCHUN MANTIQ ---
@dp.message_handler(lambda message: message.text in [
    "📊 Byudjet rejasi", "📈 Investitsiya", "🧮 Kalkulyatorlar", 
    "📉 Kurslar", "🏆 Bilimingizni sinang", "💰 Balans", 
    "💹 Valyuta kurslari", "🥇 Reyting", "📈 Statistika", "📅 Kunlik reja"
])
async def menu_handler(message: types.Message):
    text = message.text
    
    if text == "💰 Balans":
        await message.answer("💳 **Sizning balansingiz:**\n\nAsosiy hisob: 0.00 so'm\nBonuslar: 5,000 ball", parse_mode="Markdown")
    elif text == "💹 Valyuta kurslari":
        await message.answer("🏦 **Markaziy Bank kursi (Bugun):**\n\n🇺🇸 1 USD = 12,950 so'm\n🇪🇺 1 EUR = 13,820 so'm", parse_mode="Markdown")
    elif text == "🥇 Reyting":
        await message.answer("🏆 **Top foydalanuvchilar:**\n1. Rasulovich - 1500 ball\n2. SmartInvestor - 1200 ball\n3. Siz - 500 ball", parse_mode="Markdown")
    elif text == "📅 Kunlik reja":
        await message.answer("📝 **Bugungi moliyaviy rejangiz:**\n1. Xarajatlarni yozib boring\n2. Kunlik limit: 50,000 so'm\n3. 1 ta moliyaviy maqola o'qing", parse_mode="Markdown")
    elif text == "📈 Statistika":
        await message.answer("📊 **Sizning statistikangiz:**\n\nJamg'arma: 10%\nXarajatlar: 70%\nInvestitsiya: 20%", parse_mode="Markdown")
    else:
        await message.answer(f"🚀 **{text}** bo'limi hozirda AI tahlili ostida. Batafsil ma'lumot olish uchun '🧠 AI bilan suhbat' tugmasini bosing.")

# --- AI BILAN MULOQOT (Gemini) ---
@dp.message_handler()
async def chat_handler(message: types.Message):
    if message.text == "🧠 AI bilan suhbat":
        await message.answer("Siz AI rejimidasiz! ✨\nMenga xohlagan moliyaviy savolingizni bering (masalan: 'Qanday qilib pul jamg'arsam bo'ladi?')")
        return

    # Foydalanuvchi savol yozsa, Gemini javob beradi
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    try:
        # AI ga professional moliyaviy ko'rsatma beramiz
        instruction = "Sen FinEduPay AI moliyaviy ekspertisan. Faqat moliya va iqtisod haqida o'zbek tilida javob ber. "
        response = model.generate_content(f"{instruction} Savol: {message.text}")
        await message.answer(response.text, parse_mode="Markdown")
    except Exception as e:
        print(f"Xatolik: {e}")
        await message.answer("⚠️ AI hozirda band. Iltimos, bir ozdan so'ng savol bering.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
