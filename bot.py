import logging
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

# --- CONFIGURAÇÕES ---
TOKEN = "8200201915:AAHxipR8nov2PSAJ3oJLIZDqplOnxhHYRUc"
logging.basicConfig(level=logging.INFO)

# --- TEXTOS MULTILÍNGUES ---
languages = {
    "en": "🇬🇧 English",
    "pt": "🇧🇷 Português",
    "es": "🇪🇸 Español",
    "ru": "🇷🇺 Русский"
}

security_messages = {
    "en": "🔒 Welcome to SafeJob!\nEvery job opportunity shared here is carefully reviewed by our team.\nWe make sure all openings are safe, transparent, and real — to help you find stable work, save money, and enjoy your life with peace of mind.",
    "pt": "🔒 Bem-vindo ao SafeJob!\nTodas as vagas publicadas aqui são cuidadosamente analisadas pela nossa equipe.\nGarantimos que todas sejam seguras, transparentes e reais — para te ajudar a encontrar um trabalho estável, guardar seu dinheiro e aproveitar a vida com tranquilidade.",
    "es": "🔒 ¡Bienvenido a SafeJob!\nTodas las ofertas publicadas aquí son revisadas cuidadosamente por nuestro equipo.\nGarantizamos que todas sean seguras, transparentes y reales, para ayudarte a encontrar un trabajo estable, ahorrar dinero y disfrutar tu vida con tranquilidad.",
    "ru": "🔒 Добро пожаловать в SafeJob!\nВсе вакансии, размещённые здесь, тщательно проверяются нашей командой.\nМы гарантируем, что все они безопасны, прозрачны и реальны — чтобы помочь вам найти стабильную работу, накопить деньги и спокойно наслаждаться жизнью."
}

fill_carefully = {
    "en": "📝 Please fill out your information carefully so our support team can find the best possible job for you.",
    "pt": "📝 Preencha suas informações com cuidado para que nossa equipe de apoio possa encontrar a melhor vaga possível para você.",
    "es": "📝 Complete su información con cuidado para que nuestro equipo de apoyo pueda encontrar el mejor trabajo posible para usted.",
    "ru": "📝 Пожалуйста, заполните свои данные внимательно, чтобы наша команда поддержки могла найти для вас лучшую возможную работу."
}

ask_model = {
    "en": "📸 Are you a model? If yes, please send at least 4 photos of yourself.",
    "pt": "📸 Você é modelo? Se sim, envie pelo menos 4 fotos suas.",
    "es": "📸 ¿Eres modelo? Si es así, envía al menos 4 fotos tuyas.",
    "ru": "📸 Вы модель? Если да, отправьте не менее 4 своих фотографий."
}

# --- INÍCIO ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(lang, callback_data=f"lang_{code}")]
        for code, lang in languages.items()
    ]
    await update.message.reply_text(
        "🌍 Please select your language / Por favor, selecione seu idioma:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- ESCOLHA DE IDIOMA ---
async def language_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[1]
    context.user_data["lang"] = lang

    await query.edit_message_text(security_messages[lang])

    await query.message.reply_text(fill_carefully[lang])

    keyboard = [
        [InlineKeyboardButton("✅ Yes / Sim", callback_data="model_yes"),
         InlineKeyboardButton("❌ No / Não", callback_data="model_no")],
        [InlineKeyboardButton("🔁 Restart / Reiniciar", callback_data="restart_chat")]
    ]
    await query.message.reply_text(ask_model[lang], reply_markup=InlineKeyboardMarkup(keyboard))

# --- MODELO ---
async def model_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lang = context.user_data.get("lang", "en")
    await query.answer()

    if query.data == "model_yes":
        await query.edit_message_text("📷 Please send 4 or more model photos now.")
    elif query.data == "model_no":
        await query.edit_message_text("✅ Great! Let's continue with your registration.")
    elif query.data == "restart_chat":
        await start(update, context)

# --- FOTOS ---
async def handle_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    photos = context.user_data.get("photos", [])
    photos.append(update.message.photo[-1].file_id)
    context.user_data["photos"] = photos

    if len(photos) < 4:
        await update.message.reply_text(f"📸 {len(photos)} photo(s) received. Please send {4 - len(photos)} more.")
    else:
        await update.message.reply_text("✅ Thank you! Your photos have been received successfully.")

# --- EXECUÇÃO ---
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(language_selected, pattern="^lang_"))
app.add_handler(CallbackQueryHandler(model_response, pattern="^(model_yes|model_no|restart_chat)$"))
app.add_handler(MessageHandler(filters.PHOTO, handle_photos))

print("🤖 SafeJob Bot is running...")
app.run_polling()


