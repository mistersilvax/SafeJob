# -*- coding: utf-8 -*-
import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from models import Candidate, session  # seu models.py continua igual

# === CONFIG ===
TOKEN = os.environ.get("TOKEN", "8200201915:AAHxipR8nov2PSAJ3oJLIZDqplOnxhHYRUc")
GROUP_ID = -5014344988

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# === TEXTOS e PERGUNTAS (PT / EN / ES / RU) ===
TEXTS = {
    "pt": {
        "choose_lang": "🌐 *Escolha seu idioma:*",
        "welcome": "👋 Bem-vindo ao *SafeJob*! 💼",
        "safety_msg": (
            "🔒 Bem-vindo ao SafeJob!\n"
            "Todas as vagas publicadas aqui são cuidadosamente analisadas pela nossa equipe.\n"
            "Garantimos que todas sejam seguras, transparentes e reais — para te ajudar a encontrar um trabalho estável, guardar seu dinheiro e aproveitar a vida com tranquilidade.\n"
            "⚠️ Por favor, preencha as próximas perguntas *com atenção*, para que nossa equipe de apoio encontre a melhor vaga possível para você."
        ),
        "questions": [
            "1️⃣ Qual é o seu *nome completo*?",
            "2️⃣ Quantos *anos* você tem?",
            "3️⃣ Qual é a sua *nacionalidade*?",
            "4️⃣ Fale um pouco sobre suas *experiências profissionais*.",
            "5️⃣ Quais *idiomas* você fala?",
            "6️⃣ Onde você está *localizado atualmente*?",
            "7️⃣ Você possui *multas para pagar*? (Sim/Não)",
            "8️⃣ Possui *visto de trabalho válido*? (Sim/Não)",
            "9️⃣ Está disponível para *mudar de cidade*? (Sim/Não)",
            "🔟 Envie um *vídeo de apresentação* (até 1 minuto).",
            "1️⃣1️⃣ Deseja adicionar alguma *observação*?",
            "1️⃣2️⃣ Você trabalha como modelo? Se sim, envie **mínimo 4 fotos**. (opcional)"
        ],
        "confirm": "✅ Obrigado por enviar suas informações! Nossa equipe analisará seu perfil e entrará em contato.",
        "group_title": "📩 Novo candidato via SafeJob!",
        "labels": {
            "name": "👤 Nome",
            "age": "🎂 Idade",
            "nationality": "🏳️ Nacionalidade",
            "experience": "💼 Experiência",
            "languages": "🌐 Idiomas",
            "location": "📍 Localização",
            "fines": "⚠️ Multas",
            "visa": "🛂 Visto de trabalho válido",
            "relocate": "🚚 Disponível para mudar de cidade",
            "obs": "📝 Observações",
            "video": "🎥 Vídeo",
            "photos": "📸 Fotos como modelo"
        },
        "restart": "🔄 Reiniciar chat",
        "invalid_yesno": "❗️ Responda apenas 'Sim' ou 'Não'.",
    },
    "en": {
        "choose_lang": "🌐 *Choose your language:*",
        "welcome": "👋 Welcome to *SafeJob*! 💼",
        "safety_msg": (
            "🔒 Welcome to SafeJob!\n"
            "Every job opportunity shared here is carefully reviewed by our team.\n"
            "We make sure all openings are safe, transparent, and real — to help you find stable work, save money, and enjoy your life with peace of mind.\n"
            "⚠️ Please fill in the following questions *carefully*, so our support team can find the best possible job for you."
        ),
        "questions": [
            "1️⃣ What is your *full name*?",
            "2️⃣ How *old* are you?",
            "3️⃣ What is your *nationality*?",
            "4️⃣ Tell us about your *work experience*.",
            "5️⃣ What *languages* do you speak?",
            "6️⃣ Where are you *currently located*?",
            "7️⃣ Do you have *fines to pay*? (Yes/No)",
            "8️⃣ Do you have a *valid work visa*? (Yes/No)",
            "9️⃣ Are you available to *relocate*? (Yes/No)",
            "🔟 Send a *presentation video* (up to 1 minute).",
            "1️⃣1️⃣ Would you like to add any *notes*?",
            "1️⃣2️⃣ Do you work as a model? If yes, send **at least 4 photos**. (optional)"
        ],
        "confirm": "✅ Thanks for sending your information! Our team will review your profile and contact you soon.",
        "group_title": "📩 New candidate via SafeJob!",
        "labels": {
            "name": "👤 Name",
            "age": "🎂 Age",
            "nationality": "🏳️ Nationality",
            "experience": "💼 Experience",
            "languages": "🌐 Languages",
            "location": "📍 Location",
            "fines": "⚠️ Fines",
            "visa": "🛂 Work visa valid",
            "relocate": "🚚 Available to relocate",
            "obs": "📝 Notes",
            "video": "🎥 Video",
            "photos": "📸 Modeling photos"
        },
        "restart": "🔄 Restart chat",
        "invalid_yesno": "❗️ Please answer 'Yes' or 'No'.",
    },
    "es": {
        "choose_lang": "🌐 *Elige tu idioma:*",
        "welcome": "👋 ¡Bienvenido a *SafeJob*! 💼",
        "safety_msg": (
            "🔒 ¡Bienvenido a SafeJob!\n"
            "Todas las ofertas publicadas aquí son revisadas cuidadosamente por nuestro equipo.\n"
            "Garantizamos que todas sean seguras, transparentes y reales, para ayudarte a encontrar un trabajo estable, ahorrar dinero y disfrutar tu vida con tranquilidad.\n"
            "⚠️ Por favor, responde las próximas preguntas *con cuidado*, para que nuestro equipo de apoyo pueda encontrar la mejor oferta de trabajo para ti."
        ),
        "questions": [
            "1️⃣ ¿Cuál es tu *nombre completo*?",
            "2️⃣ ¿Cuántos *años* tienes?",
            "3️⃣ ¿Cuál es tu *nacionalidad*?",
            "4️⃣ Cuéntanos sobre tu *experiencia laboral*.",
            "5️⃣ ¿Qué *idiomas* hablas?",
            "6️⃣ ¿Dónde te encuentras *actualmente*?",
            "7️⃣ ¿Tienes *multas por pagar*? (Sí/No)",
            "8️⃣ ¿Posees *visa de trabajo válida*? (Sí/No)",
            "9️⃣ ¿Estás disponible para *cambiar de ciudad*? (Sí/No)",
            "🔟 Envía un *video de presentación* (hasta 1 minuto).",
            "1️⃣1️⃣ ¿Deseas añadir alguna *observación*?",
            "1️⃣2️⃣ ¿Trabajas como modelo? Si es así, envía **mínimo 4 fotos**. (opcional)"
        ],
        "confirm": "✅ ¡Gracias por enviar tu información! Nuestro equipo revisará tu perfil y se pondrá en contacto.",
        "group_title": "📩 Nuevo candidato vía SafeJob!",
        "labels": {
            "name": "👤 Nombre",
            "age": "🎂 Edad",
            "nationality": "🏳️ Nacionalidad",
            "experience": "💼 Experiencia",
            "languages": "🌐 Idiomas",
            "location": "📍 Ubicación",
            "fines": "⚠️ Multas",
            "visa": "🛂 Visa de trabajo válida",
            "relocate": "🚚 Disponible para cambiar de ciudad",
            "obs": "📝 Observaciones",
            "video": "🎥 Video",
            "photos": "📸 Fotos de modelo"
        },
        "restart": "🔄 Reiniciar chat",
        "invalid_yesno": "❗️ Responde solo 'Sí' o 'No'.",
    },
    "ru": {
        "choose_lang": "🌐 *Выберите язык:*",
        "welcome": "👋 Добро пожаловать в *SafeJob*! 💼",
        "safety_msg": (
            "🔒 Добро пожаловать в SafeJob!\n"
            "Все вакансии, размещённые здесь, тщательно проверяются нашей командой.\n"
            "Мы гарантируем, что все они безопасны, прозрачны и реальны — чтобы помочь вам найти стабильную работу, накопить деньги и спокойно наслаждаться жизнью.\n"
            "⚠️ Пожалуйста, отвечайте на следующие вопросы *внимательно*, чтобы наша команда поддержки могла найти для вас наилучшую вакансию."
        ),
        "questions": [
            "1️⃣ Какое у вас *полное имя*?",
            "2️⃣ Сколько вам *лет*?",
            "3️⃣ Какое у вас *гражданство*?",
            "4️⃣ Расскажите о вашем *опыте работы*.",
            "5️⃣ На каких *языках* вы говорите?",
            "6️⃣ Где вы *находитесь сейчас*?",
            "7️⃣ Есть ли у вас *штрафы к оплате*? (Да/Нет)",
            "8️⃣ Есть ли у вас *действующая рабочая виза*? (Да/Нет)",
            "9️⃣ Готовы ли вы *переехать*? (Да/Нет)",
            "🔟 Отправьте *видео-презентацию* (до 1 минуты).",
            "1️⃣1️⃣ Хотите добавить какие-либо *заметки*?",
            "1️⃣2️⃣ Вы работаете моделью? Если да, отправьте **не менее 4 фотографий**. (необязательно)"
        ],
        "confirm": "✅ Спасибо! Ваша информация отправлена. Наша команда свяжется с вами.",
        "group_title": "📩 Новый кандидат через SafeJob!",
        "labels": {
            "name": "👤 Имя",
            "age": "🎂 Возраст",
            "nationality": "🏳️ Гражданство",
            "experience": "💼 Опыт",
            "languages": "🌐 Языки",
            "location": "📍 Локация",
            "fines": "⚠️ Штрафы",
            "visa": "🛂 Рабочая виза",
            "relocate": "🚚 Готовность переехать",
            "obs": "📝 Примечания",
            "video": "🎥 Видео",
            "photos": "📸 Фото модели"
        },
        "restart": "🔄 Перезапустить чат",
        "invalid_yesno": "❗️ Ответьте 'Да' или 'Нет'.",
    }
}

# === TECLADO DE IDIOMAS ===
def lang_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🇧🇷 Português", callback_data="lang_pt"),
            InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
        ],
        [
            InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


