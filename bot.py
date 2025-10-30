from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# =========================
# CONFIGURAÇÕES DO BOT
# =========================
TOKEN = "8200201915:AAHxipR8nov2PSAJ3oJLIZDqplOnxhHYRUc"
GROUP_ID = "-5014344988"  # ID do grupo SafeJob

# Idiomas disponíveis
LANGUAGES = {
    "en": "🇬🇧 English",
    "pt": "🇧🇷 Português",
    "es": "🇪🇸 Español",
    "ru": "🇷🇺 Русский"
}

# Mensagem de segurança multilíngue
SECURITY_MSG = {
    "en": "🔒 Welcome to SafeJob!\nEvery job opportunity shared here is carefully reviewed by our team.\nPlease fill your information carefully so our support team can find the best position for you.",
    "pt": "🔒 Bem-vindo ao SafeJob!\nTodas as vagas publicadas aqui são cuidadosamente analisadas pela nossa equipe.\nPor favor, preencha suas informações com cuidado para que a equipe encontre a melhor vaga para você.",
    "es": "🔒 ¡Bienvenido a SafeJob!\nTodas las ofertas publicadas aquí son revisadas cuidadosamente por nuestro equipo.\nPor favor, completa tu información con cuidado para que el equipo encuentre la mejor vacante para ti.",
    "ru": "🔒 Добро пожаловать в SafeJob!\nВсе вакансии тщательно проверяются нашей командой.\nПожалуйста, заполняйте информацию внимательно, чтобы команда могла подобрать лучшую работу для вас."
}

# Perguntas multilíngues com emojis
QUESTIONS = {
    "en": [
        "👤 What's your full name?",
        "🎂 How old are you?",
        "🏳️ What's your nationality?",
        "💼 Tell us about your professional experiences.",
        "🌐 What languages do you speak?",
        "📍 Where are you currently located?",
        "⚠️ Do you have any fines to pay? (Yes/No)",
        "🛂 Do you have a valid work visa? (Yes/No)",
        "🚚 Are you available to relocate? (Yes/No)",
        "📸 Are you a model and want to provide photos? (Yes/No) – optional",
        "🎥 Send a short presentation video (up to 1 min)",
        "📝 Any additional notes?"
    ],
    "pt": [
        "👤 Qual é o seu nome completo?",
        "🎂 Quantos anos você tem?",
        "🏳️ Qual é a sua nacionalidade?",
        "💼 Fale sobre suas experiências profissionais.",
        "🌐 Quais idiomas você fala?",
        "📍 Onde você está localizado atualmente?",
        "⚠️ Você possui multas para pagar? (Sim/Não)",
        "🛂 Possui visto de trabalho válido? (Sim/Não)",
        "🚚 Está disponível para mudar de cidade? (Sim/Não)",
        "📸 Você é modelo e deseja enviar fotos? (Sim/Não) – opcional",
        "🎥 Envie um vídeo de apresentação (até 1 minuto)",
        "📝 Alguma observação adicional?"
    ],
    "es": [
        "👤 ¿Cuál es tu nombre completo?",
        "🎂 ¿Cuántos años tienes?",
        "🏳️ ¿Cuál es tu nacionalidad?",
        "💼 Cuéntanos sobre tus experiencias profesionales.",
        "🌐 ¿Qué idiomas hablas?",
        "📍 ¿Dónde te encuentras actualmente?",
        "⚠️ ¿Tienes multas pendientes? (Sí/No)",
        "🛂 ¿Tienes visa de trabajo válida? (Sí/No)",
        "🚚 ¿Estás disponible para mudarte? (Sí/No)",
        "📸 ¿Eres modelo y deseas enviar fotos? (Sí/No) – opcional",
        "🎥 Envía un video de presentación (hasta 1 minuto)",
        "📝 ¿Alguna observación adicional?"
    ],
    "ru": [
        "👤 Как вас зовут?",
        "🎂 Сколько вам лет?",
        "🏳️ Какая у вас национальность?",
        "💼 Расскажите о вашем профессиональном опыте.",
        "🌐 Какие языки вы знаете?",
        "📍 Где вы сейчас находитесь?",
        "⚠️ Есть ли у вас штрафы? (Да/Нет)",
        "🛂 Есть ли у вас рабочая виза? (Да/Нет)",
        "🚚 Готовы ли вы переехать? (Да/Нет)",
        "📸 Вы модель и хотите отправить фото? (Да/Нет) – опционально",
        "🎥 Отправьте презентационное видео (до 1 мин)",
        "📝 Дополнительные заметки?"
    ]
}

# =========================
# FUNÇÕES PRINCIPAIS
# =========================

# /start — escolha de idioma
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=code)] for code, name in LANGUAGES.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌐 Select your language / Selecione seu idioma / Seleccione su idioma / Выберите язык:",
        reply_markup=reply_markup
    )

# Escolha de idioma
async def language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data
    context.user_data["lang"] = lang
    context.user_data["q_index"] = 0
    context.user_data["photos"] = []
    await query.message.reply_text(SECURITY_MSG[lang])
    await ask_next_question(update, context)

# Enviar próxima pergunta
async def ask_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    index = context.user_data.get("q_index", 0)
    questions = QUESTIONS[lang]

    if index >= len(questions):
        await send_to_group(update, context)
        context.user_data.clear()
        return

    question = questions[index]
    keyboard = [[InlineKeyboardButton("🔄 Restart / Reiniciar / Перезапустить", callback_data="restart")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_chat.send_message(question, reply_markup=reply_markup)

# Captura texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "q_index" not in context.user_data:
        return
    index = context.user_data["q_index"]
    lang = context.user_data.get("lang", "en")
    text = update.message.text

    # Pergunta de modelo
    if QUESTIONS[lang][index].startswith("📸"):
        if text.lower() in ["no", "não", "n", "нет", "nao"]:
            context.user_data["q_index"] += 1
            await ask_next_question(update, context)
            return
        else:
            context.user_data["expect_photos"] = True
            await update.message.reply_text("📸 Please send at least 4 photos / Envie pelo menos 4 fotos / Envie al menos 4 fotos / Отправьте минимум 4 фото")
            return

    context.user_data[f"answer_{index}"] = text
    context.user_data["q_index"] += 1
    await ask_next_question(update, context)

# Captura fotos
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("expect_photos"):
        context.user_data["photos"].append(update.message.photo[-1].file_id)
        if len(context.user_data["photos"]) >= 4:
            context.user_data["q_index"] += 1
            context.user_data.pop("expect_photos")
            await ask_next_question(update, context)
        else:
            await update.message.reply_text(f"📸 {len(context.user_data['photos'])}/4 fotos recebidas. Envie mais.")
        return

# Captura vídeo
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = context.user_data.get("q_index", 0)
    context.user_data[f"answer_{index}"] = update.message.video.file_id if update.message.video else update.message.document.file_id
    context.user_data["q_index"] += 1
    await ask_next_question(update, context)

# Reiniciar
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await start(update, context)

# Callback dos botões
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "restart":
        await restart(update, context)
    else:
        await language_choice(update, context)

# Enviar respostas para grupo
async def send_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answers = context.user_data
    lang = answers.get("lang", "en")
    questions = QUESTIONS[lang]

    # Montar mensagem formatada
    message = "📩 Novo candidato via SafeJob!\n\n"
    icons = ["👤", "🎂", "🏳️", "💼", "🌐", "📍", "⚠️", "🛂", "🚚", "📸", "🎥", "📝"]

    for i, icon in enumerate(icons):
        key = f"answer_{i}"
        if key in answers:
            message += f"{icon} {answers[key]}\n"

    await context.bot.send_message(chat_id=GROUP_ID, text=message)

    # Enviar fotos
    for photo in answers.get("photos", []):
        await context.bot.send_photo(chat_id=GROUP_ID, photo=photo)

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.MimeType("video/mp4"), handle_video))

    app.run_polling()

if __name__ == "__main__":
    main()
