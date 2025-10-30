from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# CONFIG
TOKEN = "8200201915:AAHxipR8nov2PSAJ3oJLIZDqplOnxhHYRUc"
GROUP_ID = "-5014344988"

LANGUAGES = {
    "en": "🇬🇧 English",
    "pt": "🇧🇷 Português",
    "es": "🇪🇸 Español",
    "ru": "🇷🇺 Русский"
}

SECURITY_MSG = {
    "en": "🔒 Welcome to SafeJob!\nEvery job opportunity shared here is carefully reviewed by our team.\nPlease fill your information carefully so our support team can find the best position for you.",
    "pt": "🔒 Bem-vindo ao SafeJob!\nTodas as vagas publicadas aqui são cuidadosamente analisadas pela nossa equipe.\nPor favor, preencha suas informações com cuidado para que a equipe encontre a melhor vaga para você.",
    "es": "🔒 ¡Bienvenido a SafeJob!\nTodas las ofertas publicadas aquí son revisadas cuidadosamente por nuestro equipo.\nPor favor, completa tu información con cuidado para que el equipo encuentre la mejor vacante para ti.",
    "ru": "🔒 Добро пожаловать в SafeJob!\nВсе вакансии тщательно проверяются нашей командой.\nПожалуйста, заполняйте информацию внимательно, чтобы команда могла подобрать лучшую работу для вас."
}

THANK_YOU = {
    "en": "✅ Thank you! Our team will review your information and contact you soon.",
    "pt": "✅ Obrigado! Nossa equipe vai analisar suas informações e entrará em contato em breve.",
    "es": "✅ ¡Gracias! Nuestro equipo revisará tu información y se pondrá en contacto contigo pronto.",
    "ru": "✅ Спасибо! Наша команда рассмотрит вашу информацию и свяжется с вами в ближайшее время."
}

QUESTIONS = {
    "en": [
        "1️⃣ What's your full name?",
        "2️⃣ How old are you?",
        "3️⃣ What's your nationality?",
        "4️⃣ Tell us about your professional experiences.",
        "5️⃣ What languages do you speak?",
        "6️⃣ Where are you currently located?",
        "7️⃣ Do you have any fines to pay? (Yes/No)",
        "8️⃣ Do you have a valid work visa? (Yes/No)",
        "9️⃣ Are you available to relocate? (Yes/No)",
        "🔟 Are you a model and want to provide photos? (Yes/No) – optional",
        "1️⃣1️⃣ Send a presentation video (up to 1 min)",
        "1️⃣2️⃣ What is your Telegram username or number for contact?",
        "1️⃣3️⃣ Any additional notes?"
    ],
    "pt": [
        "1️⃣ Qual é o seu nome completo?",
        "2️⃣ Quantos anos você tem?",
        "3️⃣ Qual é a sua nacionalidade?",
        "4️⃣ Fale sobre suas experiências profissionais.",
        "5️⃣ Quais idiomas você fala?",
        "6️⃣ Onde você está localizado atualmente?",
        "7️⃣ Você possui multas para pagar? (Sim/Não)",
        "8️⃣ Possui visto de trabalho válido? (Sim/Não)",
        "9️⃣ Está disponível para mudar de cidade? (Sim/Não)",
        "🔟 Você é modelo e deseja enviar fotos? (Sim/Não) – opcional",
        "1️⃣1️⃣ Envie um vídeo de apresentação (até 1 minuto)",
        "1️⃣2️⃣ Qual o seu Telegram para contato? (adicione @ ou número)",
        "1️⃣3️⃣ Alguma observação adicional?"
    ],
    "es": [
        "1️⃣ ¿Cuál es tu nombre completo?",
        "2️⃣ ¿Cuántos años tienes?",
        "3️⃣ ¿Cuál es tu nacionalidad?",
        "4️⃣ Cuéntanos sobre tus experiencias profesionales.",
        "5️⃣ ¿Qué idiomas hablas?",
        "6️⃣ ¿Dónde te encuentras actualmente?",
        "7️⃣ ¿Tienes multas pendientes? (Sí/No)",
        "8️⃣ ¿Tienes visa de trabajo válida? (Sí/No)",
        "9️⃣ ¿Estás disponible para mudarte? (Sí/No)",
        "🔟 ¿Eres modelo y deseas enviar fotos? (Sí/No) – opcional",
        "1️⃣1️⃣ Envía un video de presentación (hasta 1 min)",
        "1️⃣2️⃣ ¿Cuál es tu Telegram de contacto? (con @ o número)",
        "1️⃣3️⃣ Alguna observación adicional?"
    ],
    "ru": [
        "1️⃣ Как вас зовут?",
        "2️⃣ Сколько вам лет?",
        "3️⃣ Какая у вас национальность?",
        "4️⃣ Расскажите о вашем профессиональном опыте.",
        "5️⃣ Какие языки вы знаете?",
        "6️⃣ Где вы сейчас находитесь?",
        "7️⃣ Есть ли у вас штрафы? (Да/Нет)",
        "8️⃣ Есть ли у вас рабочая виза? (Да/Нет)",
        "9️⃣ Готовы ли вы переехать? (Да/Нет)",
        "🔟 Вы модель и хотите отправить фото? (Да/Нет) – опционально",
        "1️⃣1️⃣ Отправьте презентационное видео (до 1 мин)",
        "1️⃣2️⃣ Ваш Telegram для связи? (@ или номер)",
        "1️⃣3️⃣ Дополнительные заметки?"
    ]
}


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=code)] for code, name in LANGUAGES.items()]
    await update.message.reply_text(
        "🌐 Select your language / Selecione seu idioma / Seleccione su idioma / Выберите язык:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# LANGUAGE CHOICE
async def language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data
    context.user_data.clear()
    context.user_data["lang"] = lang
    context.user_data["q_index"] = 0
    context.user_data["photos"] = []
    await query.message.reply_text(SECURITY_MSG[lang])
    await ask_next_question(update, context)


# NEXT QUESTION
async def ask_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    index = context.user_data.get("q_index", 0)
    questions = QUESTIONS[lang]

    if index >= len(questions):
        await send_to_group(update, context)
        await update.effective_chat.send_message(THANK_YOU[lang])
        context.user_data.clear()
        return

    question = questions[index]
    keyboard = [[InlineKeyboardButton("🔄 Restart / Reiniciar / Перезапустить", callback_data="restart")]]
    await update.effective_chat.send_message(question, reply_markup=InlineKeyboardMarkup(keyboard))


# HANDLE TEXT
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "q_index" not in context.user_data:
        return
    index = context.user_data["q_index"]
    lang = context.user_data.get("lang", "en")
    text = update.message.text

    if QUESTIONS[lang][index].startswith("🔟"):
        if text.lower() in ["no", "não", "n", "нет", "nao"]:
            context.user_data["q_index"] += 1
            await ask_next_question(update, context)
            return
        else:
            context.user_data["expect_photos"] = True
            await update.effective_chat.send_message("📸 Please send at least 4 photos.")
            return

    context.user_data[f"answer_{index}"] = text
    context.user_data["q_index"] += 1
    await ask_next_question(update, context)


# HANDLE PHOTOS
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("expect_photos"):
        context.user_data["photos"].append(update.message.photo[-1].file_id)
        if len(context.user_data["photos"]) >= 4:
            context.user_data["q_index"] += 1
            context.user_data.pop("expect_photos")
            await ask_next_question(update, context)
        else:
            await update.message.reply_text(f"📸 {len(context.user_data['photos'])}/4 received. Send more photos.")


# HANDLE VIDEO
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["video_id"] = update.message.video.file_id if update.message.video else update.message.document.file_id
    context.user_data["q_index"] += 1
    await ask_next_question(update, context)


# RESTART
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await start(update, context)


# CALLBACKS
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "restart":
        await restart(update, context)
    else:
        await language_choice(update, context)


# SEND TO GROUP
async def send_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = context.user_data
    msg = (
        "📩 Novo candidato via SafeJob!\n\n"
        f"👤 Nome: {data.get('answer_0', '-')}\n"
        f"🎂 Idade: {data.get('answer_1', '-')}\n"
        f"🏳️ Nacionalidade: {data.get('answer_2', '-')}\n"
        f"💼 Experiência: {data.get('answer_3', '-')}\n"
        f"🌐 Idiomas: {data.get('answer_4', '-')}\n"
        f"📍 Localização: {data.get('answer_5', '-')}\n"
        f"⚠️ Multas: {data.get('answer_6', '-')}\n"
        f"🛂 Visto de trabalho válido: {data.get('answer_7', '-')}\n"
        f"🚚 Disponível para mudar de cidade: {data.get('answer_8', '-')}\n"
        f"📱 Telegram: {data.get('answer_11', '-')}\n"
        f"📝 Observações: {data.get('answer_12', '-')}\n"
    )

    await context.bot.send_message(chat_id=GROUP_ID, text=msg)

    # Envia fotos
    for photo in data.get("photos", []):
        await context.bot.send_photo(chat_id=GROUP_ID, photo=photo)

    # Envia vídeo corretamente
    if "video_id" in data:
        await context.bot.send_video(chat_id=GROUP_ID, video=data["video_id"], caption="🎥 Vídeo de apresentação")


# MAIN
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    video_filter = filters.VIDEO | filters.Document.MimeType("video/mp4")
    app.add_handler(MessageHandler(video_filter, handle_video))
    app.run_polling()


if __name__ == "__main__":
    main()

