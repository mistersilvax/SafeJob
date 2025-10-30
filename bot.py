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
# Troque pelo token real ou use variável de ambiente
TOKEN = os.environ.get("TOKEN", "8200201915:AAHxipR8nov2PSAJ3oJLIZDqplOnxhHYRUc")
# Grupo para envio das fichas (conforme informado)
GROUP_ID = -5014344988

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# === TEXTOS e PERGUNTAS (PT / EN / ES / RU) ===
TEXTS = {
    "pt": {
        "choose_lang": "🌐 *Escolha seu idioma:*",
        "welcome": "👋 Bem-vindo ao *SafeJob*! 💼\nVamos começar seu cadastro — responda às perguntas abaixo.",
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
            "1️⃣1️⃣ Deseja adicionar alguma *observação*?"
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
            "video": "🎥 Vídeo"
        },
        "restart": "🔄 Reiniciar chat",
        "invalid_yesno": "❗️ Responda apenas 'Sim' ou 'Não'.",
    },
    "en": {
        "choose_lang": "🌐 *Choose your language:*",
        "welcome": "👋 Welcome to *SafeJob*! 💼\nLet's start your registration — answer the questions below.",
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
            "1️⃣1️⃣ Would you like to add any *notes*?"
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
            "video": "🎥 Video"
        },
        "restart": "🔄 Restart chat",
        "invalid_yesno": "❗️ Please answer 'Yes' or 'No'.",
    },
    "es": {
        "choose_lang": "🌐 *Elige tu idioma:*",
        "welcome": "👋 ¡Bienvenido a *SafeJob*! 💼\nComencemos tu registro — responde las preguntas a continuación.",
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
            "1️⃣1️⃣ ¿Deseas añadir alguna *observación*?"
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
            "video": "🎥 Video"
        },
        "restart": "🔄 Reiniciar chat",
        "invalid_yesno": "❗️ Responde solo 'Sí' o 'No'.",
    },
    "ru": {
        "choose_lang": "🌐 *Выберите язык:*",
        "welcome": "👋 Добро пожаловать в *SafeJob*! 💼\nНачнем регистрацию — ответьте на вопросы ниже.",
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
            "1️⃣1️⃣ Хотите добавить какие-либо *заметки*?"
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
            "video": "🎥 Видео"
        },
        "restart": "🔄 Перезапустить чат",
        "invalid_yesno": "❗️ Ответьте 'Да' или 'Нет'.",
    }
}

# === TECLADO: idiomas e restart ===
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


def restart_button(lang="pt"):
    label = TEXTS.get(lang, TEXTS["pt"])["restart"]
    return InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data="restart")]])


# === HELPERS ===
def normalize_yesno(text):
    t = text.strip().lower()
    if t in ("s", "sim", "yes", "y", "да", "d", "si"):
        return "Sim"
    if t in ("n", "não", "nao", "no", "нет", "n"):
        return "Não"
    return None


# === HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # send language selection
    await update.message.reply_text(
        TEXTS["pt"]["choose_lang"],
        parse_mode="Markdown",
        reply_markup=lang_keyboard(),
    )


async def lang_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # data like lang_pt
    lang = query.data.split("_")[1]
    context.user_data.clear()
    context.user_data["lang"] = lang
    context.user_data["q_idx"] = 0
    context.user_data["answers"] = {}
    # send welcome and first question
    await query.edit_message_text(
        TEXTS[lang]["welcome"],
        parse_mode="Markdown",
        reply_markup=restart_button(lang),
    )
    # send first question
    await query.message.reply_text(
        TEXTS[lang]["questions"][0],
        reply_markup=restart_button(lang),
        parse_mode="Markdown",
    )


async def restart_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # When user presses restart — go back to language selection
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.edit_message_text(
        TEXTS["pt"]["choose_lang"],
        parse_mode="Markdown",
        reply_markup=lang_keyboard(),
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # main guided flow
    user = update.message.from_user
    lang = context.user_data.get("lang", "pt")
    q_idx = context.user_data.get("q_idx", 0)
    answers = context.user_data.get("answers", {})

    # Accept video as direct message when at video question index (9 -> index starts at 0)
    VIDEO_Q_INDEX = 9  # 0-based index for question 10 (video)
    text = update.message.text or ""

    # If we're expecting video but user sent text, ask for video
    if q_idx == VIDEO_Q_INDEX:
        # check for video message
        video = update.message.video or update.message.video_note
        doc = update.message.document
        video_file_id = None
        if video:
            video_file_id = video.file_id
        elif doc and doc.mime_type and doc.mime_type.startswith("video"):
            video_file_id = doc.file_id

        if video_file_id is None:
            # user sent text instead of video
            await update.message.reply_text(TEXTS[lang]["questions"][q_idx] + "\n\n" + "❗️ Por favor, envie o vídeo como arquivo (até 1 minuto).", reply_markup=restart_button(lang))
            return
        # store video id
        answers["video_file_id"] = video_file_id
        context.user_data["answers"] = answers
        context.user_data["q_idx"] = q_idx + 1
        # ask next (observation)
        await update.message.reply_text(TEXTS[lang]["questions"][q_idx + 1], reply_markup=restart_button(lang), parse_mode="Markdown")
        return

    # Normal question flow: save text answers
    current_q = TEXTS[lang]["questions"][q_idx]
    # Basic validation for yes/no questions indices 6,7,8 (0-based)
    if q_idx in (6, 7, 8):
        yn = normalize_yesno(text)
        if yn is None:
            await update.message.reply_text(TEXTS[lang]["invalid_yesno"], reply_markup=restart_button(lang))
            return
        # map to Sim/Não strings for storage
        answers_key = ["fines", "visa", "relocate"][ (6,7,8).index(q_idx) ]
        answers[answers_key] = yn
    else:
        # mapping keys by index
        keys = ["name", "age", "nationality", "experience", "languages", "location"]
        if q_idx < len(keys):
            answers[keys[q_idx]] = text
        elif q_idx == 10:
            # last observation
            answers["obs"] = text
        else:
            # safety fallback
            answers[f"q_{q_idx}"] = text

    # advance
    context.user_data["answers"] = answers
    context.user_data["q_idx"] = q_idx + 1

    # if finished (we had 11 questions -> q_idx now == 11)
    if context.user_data["q_idx"] >= len(TEXTS[lang]["questions"]):
        # Save to DB (best-effort: set attributes that Candidate accepts)
        try:
            candidate = Candidate()
            # try to set attributes if exist, otherwise ignore
            for k, v in answers.items():
                try:
                    setattr(candidate, k, v)
                except Exception:
                    # model may not have attribute — ignore
                    pass
            session.add(candidate)
            session.commit()
        except Exception as e:
            logging.exception("Erro ao salvar candidato: %s", e)

        # send confirmation to user
        await update.message.reply_text(TEXTS[lang]["confirm"], reply_markup=restart_button(lang), parse_mode="Markdown")

        # build group message in Portuguese style similar to exemplo (we'll send in Portuguese for group)
        labels = TEXTS["pt"]["labels"]
        msg_lines = [
            TEXTS["pt"]["group_title"],
            "",
            f"{labels['name']}: {answers.get('name','-')}",
            f"{labels['age']}: {answers.get('age','-')}",
            f"{labels['nationality']}: {answers.get('nationality','-')}",
            f"{labels['experience']}: {answers.get('experience','-')}",
            f"{labels['languages']}: {answers.get('languages','-')}",
            f"{labels['location']}: {answers.get('location','-')}",
            f"{labels['fines']}: {answers.get('fines','-')}",
            f"{labels['visa']}: {answers.get('visa','-')}",
            f"{labels['relocate']}: {answers.get('relocate','-')}",
            f"{labels['obs']}: {answers.get('obs','-')}",
        ]
        group_text = "\n".join(msg_lines)

        # send message and video if present
        try:
            # if video exists, try to send it then text as caption or message
            video_id = answers.get("video_file_id")
            if video_id:
                # send video to group with caption (caption must be <=1024 chars normally)
                try:
                    await context.bot.send_video(chat_id=GROUP_ID, video=video_id, caption=group_text)
                except Exception:
                    # fallback: send text then forward video
                    await context.bot.send_message(chat_id=GROUP_ID, text=group_text)
                    await context.bot.send_video(chat_id=GROUP_ID, video=video_id)
            else:
                await context.bot.send_message(chat_id=GROUP_ID, text=group_text)
        except Exception as e:
            logging.exception("Erro ao enviar para grupo: %s", e)

        # clear user_data for next use
        context.user_data.clear()
        return

    # else, send next question
    next_q = TEXTS[lang]["questions"][context.user_data["q_idx"]]
    await update.message.reply_text(next_q, reply_markup=restart_button(lang), parse_mode="Markdown")


# CallbackQuery handlers wrapper: pattern routing
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    if data.startswith("lang_"):
        await lang_select(update, context)
    elif data == "restart":
        await restart_callback(update, context)
    else:
        await update.callback_query.answer()  # noop


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    # single callback handler routes by data
    app.add_handler(CallbackQueryHandler(callback_router))
    # messages handler for guided answers (text and files)
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()



