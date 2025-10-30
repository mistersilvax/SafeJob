import logging
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

# === CONFIGURAÇÕES ===
TOKEN = "8200201915:AAHxipR8nov2PSAJ3oJLIZDqplOnxhHYRUc"
GROUP_ID = -5014344988
logging.basicConfig(level=logging.INFO)

# === TEXTOS MULTILÍNGUES ===
languages = {
    "pt": "🇧🇷 Português",
    "en": "🇺🇸 English",
    "es": "🇪🇸 Español",
    "ru": "🇷🇺 Русский"
}

security_messages = {
    "pt": "🔒 Bem-vindo ao SafeJob!\nTodas as vagas publicadas aqui são cuidadosamente analisadas pela nossa equipe.\nGarantimos que todas sejam seguras, transparentes e reais — para te ajudar a encontrar um trabalho estável, guardar seu dinheiro e aproveitar a vida com tranquilidade.",
    "en": "🔒 Welcome to SafeJob!\nEvery job opportunity shared here is carefully reviewed by our team.\nWe make sure all openings are safe, transparent, and real — to help you find stable work, save money, and enjoy your life with peace of mind.",
    "es": "🔒 ¡Bienvenido a SafeJob!\nTodas las ofertas publicadas aquí son revisadas cuidadosamente por nuestro equipo.\nGarantizamos que todas sean seguras, transparentes y reales, para ayudarte a encontrar un trabajo estable, ahorrar dinero y disfrutar tu vida con tranquilidad.",
    "ru": "🔒 Добро пожаловать в SafeJob!\nВсе вакансии, размещённые здесь, тщательно проверяются нашей командой.\nМы гарантируем, что все они безопасны, прозрачны и реальны — чтобы помочь вам найти стабильную работу, накопить деньги и спокойно наслаждаться жизнью."
}

fill_carefully = {
    "pt": "📝 Preencha suas informações com cuidado para que nossa equipe de apoio possa encontrar a melhor vaga possível para você.",
    "en": "📝 Please fill out your information carefully so our support team can find the best possible job for you.",
    "es": "📝 Complete su información con cuidado para que nuestro equipo de apoyo pueda encontrar el mejor trabajo posible para usted.",
    "ru": "📝 Пожалуйста, заполните свои данные внимательно, чтобы наша команда поддержки могла найти для вас лучшую возможную работу."
}

ask_model = {
    "pt": "📸 Você é modelo? Se sim, envie pelo menos 4 fotos suas. (opcional)",
    "en": "📸 Are you a model? If yes, send at least 4 photos. (optional)",
    "es": "📸 ¿Eres modelo? Si es así, envía al menos 4 fotos. (opcional)",
    "ru": "📸 Вы модель? Если да, отправьте не менее 4 фотографий. (необязательно)"
}

questions = {
    "pt": [
        "1️⃣ Qual é o seu nome completo?",
        "2️⃣ Quantos anos você tem?",
        "3️⃣ Qual é a sua nacionalidade?",
        "4️⃣ Fale um pouco sobre suas experiências profissionais.",
        "5️⃣ Quais idiomas você fala?",
        "6️⃣ Onde você está localizado atualmente?",
        "7️⃣ Você possui multas para pagar? (Sim/Não)",
        "8️⃣ Possui visto de trabalho válido? (Sim/Não)",
        "9️⃣ Está disponível para mudar de cidade? (Sim/Não)",
        "🔟 Envie um vídeo de apresentação (até 1 minuto).",
        "1️⃣1️⃣ Deseja adicionar alguma observação?"
    ],
    "en": [
        "1️⃣ What is your full name?",
        "2️⃣ How old are you?",
        "3️⃣ What is your nationality?",
        "4️⃣ Tell us about your work experience.",
        "5️⃣ What languages do you speak?",
        "6️⃣ Where are you currently located?",
        "7️⃣ Do you have fines to pay? (Yes/No)",
        "8️⃣ Do you have a valid work visa? (Yes/No)",
        "9️⃣ Are you available to relocate? (Yes/No)",
        "🔟 Send a presentation video (up to 1 minute).",
        "1️⃣1️⃣ Would you like to add any notes?"
    ],
    "es": [
        "1️⃣ ¿Cuál es tu nombre completo?",
        "2️⃣ ¿Cuántos años tienes?",
        "3️⃣ ¿Cuál es tu nacionalidad?",
        "4️⃣ Cuéntanos sobre tu experiencia laboral.",
        "5️⃣ ¿Qué idiomas hablas?",
        "6️⃣ ¿Dónde te encuentras actualmente?",
        "7️⃣ ¿Tienes multas por pagar? (Sí/No)",
        "8️⃣ ¿Posees visa de trabajo válida? (Sí/No)",
        "9️⃣ ¿Estás disponible para cambiar de ciudad? (Sí/No)",
        "🔟 Envía un video de presentación (hasta 1 minuto).",
        "1️⃣1️⃣ ¿Deseas añadir alguna observación?"
    ],
    "ru": [
        "1️⃣ Какое у вас полное имя?",
        "2️⃣ Сколько вам лет?",
        "3️⃣ Какое у вас гражданство?",
        "4️⃣ Расскажите о вашем опыте работы.",
        "5️⃣ На каких языках вы говорите?",
        "6️⃣ Где вы находитесь сейчас?",
        "7️⃣ Есть ли у вас штрафы к оплате? (Да/Нет)",
        "8️⃣ Есть ли у вас действующая рабочая виза? (Да/Нет)",
        "9️⃣ Готовы ли вы переехать? (Да/Нет)",
        "🔟 Отправьте видео-презентацию (до 1 минуты).",
        "1️⃣1️⃣ Хотите добавить какие-либо заметки?"
    ]
}

labels = {
    "pt": {
        "name":"👤 Nome", "age":"🎂 Idade", "nationality":"🏳️ Nacionalidade", "experience":"💼 Experiência",
        "languages":"🌐 Idiomas", "location":"📍 Localização", "fines":"⚠️ Multas",
        "visa":"🛂 Visto de trabalho válido", "relocate":"🚚 Disponível para mudar de cidade",
        "obs":"📝 Observações", "video":"🎥 Vídeo", "photos":"📸 Fotos como modelo"
    },
    "en": {
        "name":"👤 Name", "age":"🎂 Age", "nationality":"🏳️ Nationality", "experience":"💼 Experience",
        "languages":"🌐 Languages", "location":"📍 Location", "fines":"⚠️ Fines",
        "visa":"🛂 Work visa valid", "relocate":"🚚 Available to relocate",
        "obs":"📝 Notes", "video":"🎥 Video", "photos":"📸 Modeling photos"
    },
    "es": {
        "name":"👤 Nombre", "age":"🎂 Edad", "nationality":"🏳️ Nacionalidad", "experience":"💼 Experiencia",
        "languages":"🌐 Idiomas", "location":"📍 Ubicación", "fines":"⚠️ Multas",
        "visa":"🛂 Visa de trabajo válida", "relocate":"🚚 Disponible para cambiar de ciudad",
        "obs":"📝 Observaciones", "video":"🎥 Video", "photos":"📸 Fotos de modelo"
    },
    "ru": {
        "name":"👤 Имя", "age":"🎂 Возраст", "nationality":"🏳️ Гражданство", "experience":"💼 Опыт",
        "languages":"🌐 Языки", "location":"📍 Локация", "fines":"⚠️ Штрафы",
        "visa":"🛂 Рабочая виза", "relocate":"🚚 Готовность переехать",
        "obs":"📝 Примечания", "video":"🎥 Видео", "photos":"📸 Фото модели"
    }
}

# === TECLADO DE IDIOMAS ===
def lang_keyboard():
    keyboard = [
        [InlineKeyboardButton(lang, callback_data=f"lang_{code}")]
        for code, lang in languages.items()
    ]
    return InlineKeyboardMarkup(keyboard)

# === START ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌍 Please select your language / Por favor, selecione seu idioma:",
        reply_markup=lang_keyboard()
    )

# === ESCOLHA DE IDIOMA ===
async def language_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[1]
    context.user_data["lang"] = lang

    # Mensagem de segurança + aviso de preenchimento
    await query.edit_message_text(security_messages[lang] + "\n\n" + fill_carefully[lang])
    context.user_data["q_index"] = 0
    context.user_data["answers"] = []
    await ask_next_question(query.message, context)

# === FUNÇÃO PARA PERGUNTAS ===
async def ask_next_question(message, context):
    lang = context.user_data.get("lang", "



