from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaVideo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# ======================
# CONFIGURAÇÕES
# ======================
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

# ======================
# PERGUNTAS COM EMOJIS
# ======================
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
        "🎥 Send a presentation video (up to 1 minute)",
        "📱 What is your Telegram username or number for contact?",
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
        "📱 Qual o seu Telegram para contato? (adicione @ ou número)",
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
        "📱 ¿Cuál es tu Telegram de contacto? (con @ o número)",
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
        "📱 Ваш Telegram для связи? (@ или номер)",
        "📝 Дополнительные заметки?"
    ]
}

# ======================
# START COMMAND
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=code)] for code, name in LANGUAGES.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌐 Select your language / Selecione seu idioma / Seleccione su idioma / Выберите язык:",
        reply_markup=reply_markup
    )

# ======================
# LINGUAGEM ESCOLHIDA
# ======================
async def language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data
    context.user_data["lang"] = lang
    context.user_data["q_index"] = 0
    context.user_data["photos"] = []
    await query.message.reply_text(SECURITY_MSG[lang])
    await ask_next_question(update, context)

# ======================
# FAZ A PRÓXIMA PERGUNTA
# ======================
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
    await update.effective_chat.send_message(question, reply_markup=InlineKeyboardMarkup(keyboard))

# ======================
# TRATA RESPOSTAS DE TEXTO
# ======================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "q_index" not in context.user_data:
        return
    index = context.user_data["q_index"]
    lang = context.user_data.get("lang", "en")
    text = update.message.text

    if QUESTIONS[lang][index].startswith("📸"):
        if text.lower() in ["no", "não", "n", "нет"]:
            context.user_data["q_index"] += 1
            await ask_next_question(update, context)
            return
        else:
            context.user_data["expect_photos"] = True
            await update.message.reply_text("📸 Please send at least 4 photos.")
            return

    context.user_data[f"answer_{index}"] = text
    context.user_data["q_index"] += 1
    await ask_next_question(update, context)

# ======================
# TRATA FOTOS
# ======================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("expect_photos"):
        context.user_data["photos"].append(update.message.photo[-1].file_id)
        if len(context.user_data["photos"]) >= 4:
            context.user_data["q_index"] += 1
            context.user_data.pop("expect_photos")
            await ask_next_question(update, context)
        else:
            await update.message.reply_text(f"📸 {len(context.user_data['photos'])}/4 received. Please send more.")
        return

# ======================
# TRATA VÍDEO
# ======================
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = context.user_data.get("q_index", 0)
    video = update.message.video or update.message.document
    context.user_data["video"] = video.file_id
    context.user_data["q_index"] += 1
    await ask_next_question(update, context)

# ======================
# CALLBACKS E REINÍCIO
# ======================
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await start(update, context)

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "restart":
        await restart(update, context)
    else:
        await language_choice(update, context)

# ======================
# ENVIA AS INFORMAÇÕES PARA O GRUPO
# ======================
async def send_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answers = context.user_data
    lang = answers.get("lang", "pt")

    msg = (
        "📩 Novo candidato via SafeJob!\n\n"
        f"👤 Nome: {answers.get('answer_0', '-')}\n"
        f"🎂 Idade: {answers.get('answer_1', '-')}\n"
        f"🏳️ Nacionalidade: {answers.get('answer_2', '-')}\n"
        f"💼 Experiência: {answers.get('answer_3', '-')}\n"
        f"🌐 Idiomas: {answers.get('answer_4', '-')}\n"
        f"📍 Localização: {answers.get('answer_5', '-')}\n"
        f"⚠️ Multas: {answers.get('answer_6', '-')}\n"
        f"🛂 Visto de trabalho válido: {answers.get('answer_7', '-')}\n"
        f"🚚 Disponível para mudar de cidade: {answers.get('answer_8', '-')}\n"
        f"📱 Telegram: {answers.get('answer_11', '-')}\n"
        f"📝 Observações: {answers.get('answer_12', '-')}"
    )

    await context.bot.send_message(chat_id=GROUP_ID, text=msg)

    # Envia fotos
    for photo in answers.get("photos", []):
        await context.bot.send_photo(chat_id=GROUP_ID, photo=photo)

    # Envia vídeo corretamente
    if "video" in answers:
        await context.bot.send_video(chat_id=GROUP_ID, video=answers["video"], caption="🎥 Vídeo de apresentação:")

    # Mensagem final para o candidato
    await update.effective_chat.send_message(
        "✅ Obrigado por enviar suas informações!\nNossa equipe irá analisá-las e retornará em breve. 🔎"
    )

# ======================
# MAIN
# ======================
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


