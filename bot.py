# -*- coding: utf-8 -*-
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Optional: import your models if you have them (SQLAlchemy)
# from models import Candidate, session

# === CONFIG ===
TOKEN = os.environ.get("TOKEN", "8200201915:AAHxipR8nov2PSAJ3oJLIZDqplOnxhHYRUc")
GROUP_ID = -5014344988
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === MULTI-LANGUAGE TEXTS ===
LANGUAGES = {
    "pt": "🇧🇷 Português",
    "en": "🇺🇸 English",
    "es": "🇪🇸 Español",
    "ru": "🇷🇺 Русский",
}

SECURITY = {
    "en": (
        "🔒 Welcome to SafeJob!\n"
        "Every job opportunity shared here is carefully reviewed by our team.\n"
        "We make sure all openings are safe, transparent, and real — to help you find stable work, save money, and enjoy your life with peace of mind.\n\n"
        "⚠️ Please fill in the following questions *carefully*, so our support team can find the best possible job for you."
    ),
    "pt": (
        "🔒 Bem-vindo ao SafeJob!\n"
        "Todas as vagas publicadas aqui são cuidadosamente analisadas pela nossa equipe.\n"
        "Garantimos que todas sejam seguras, transparentes e reais — para te ajudar a encontrar um trabalho estável, guardar seu dinheiro e aproveitar a vida com tranquilidade.\n\n"
        "⚠️ Por favor, preencha as próximas perguntas *com atenção*, para que nossa equipe de apoio encontre a melhor vaga possível para você."
    ),
    "es": (
        "🔒 ¡Bienvenido a SafeJob!\n"
        "Todas las ofertas publicadas aquí son revisadas cuidadosamente por nuestro equipo.\n"
        "Garantizamos que todas sean seguras, transparentes y reales, para ayudarte a encontrar un trabajo estable, ahorrar dinero y disfrutar tu vida con tranquilidad.\n\n"
        "⚠️ Por favor, responde las próximas preguntas *con cuidado*, para que nuestro equipo de apoyo pueda encontrar la mejor oferta de trabajo para ti."
    ),
    "ru": (
        "🔒 Добро пожаловать в SafeJob!\n"
        "Все вакансии, размещённые здесь, тщательно проверяются нашей командой.\n"
        "Мы гарантируем, что все они безопасны, прозрачны и реальны — чтобы помочь вам найти стабильную работу, накопить деньги и спокойно наслаждаться жизнью.\n\n"
        "⚠️ Пожалуйста, отвечайте на следующие вопросы *внимательно*, чтобы наша команда поддержки могла найти для вас наилучшую вакансию."
    ),
}

FILL_CAREFULLY = {
    "en": "📝 Please fill out your information carefully so our support team can find the best possible job for you.",
    "pt": "📝 Preencha suas informações com cuidado para que nossa equipe de apoio possa encontrar a melhor vaga possível para você.",
    "es": "📝 Complete su información con cuidado para que nuestro equipo de apoyo pueda encontrar el mejor trabajo posible para usted.",
    "ru": "📝 Пожалуйста, заполните свои данные внимательно, чтобы наша команда поддержки могла найти для вас лучшую возможную работу.",
}

ASK_MODEL = {
    "en": "📸 Do you work as a model? If yes, please send at least 4 photos of yourself. (optional)",
    "pt": "📸 Você trabalha como modelo? Se sim, envie pelo menos 4 fotos suas. (opcional)",
    "es": "📸 ¿Trabajas como modelo? Si es así, envía al menos 4 fotos tuyas. (opcional)",
    "ru": "📸 Вы работаете моделью? Если да, отправьте не менее 4 фотографий. (необязательно)",
}

# Questions order:
# 0..8 = normal questions (name..relocate)
# 9 = MODEL question (optional; expects photos if yes)
# 10 = VIDEO question (expect video file)
# 11 = OBSERVATION (free text) -> finish
QUESTIONS = {
    "pt": [
        "1️⃣ Qual é o seu *nome completo*?",
        "2️⃣ Quantos *anos* você tem?",
        "3️⃣ Qual é a sua *nacionalidade*?",
        "4️⃣ Fale um pouco sobre suas *experiências profissionais*.",
        "5️⃣ Quais *idiomas* você fala?",
        "6️⃣ Onde você está *localizado atualmente*?",
        "7️⃣ Você possui *multas para pagar*? (Sim/Não)",
        "8️⃣ Possui *visto de trabalho válido*? (Sim/Não)",
        "9️⃣ Está disponível para *mudar de cidade*? (Sim/Não)",
        # 9 -> model question will be ASK_MODEL
        "🔟 Envie um *vídeo de apresentação* (até 1 minuto).",
        "1️⃣1️⃣ Deseja adicionar alguma *observação*?"
    ],
    "en": [
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
    "es": [
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
    "ru": [
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
}

LABELS_PT = {
    "name": "👤 Nome",
    "age": "🎂 Idade",
    "nationality": "🏳️ Nacionalidade",
    "experience": "💼 Experiência",
    "languages": "🌐 Idiomas",
    "location": "📍 Localização",
    "fines": "⚠️ Multas",
    "visa": "🛂 Visto de trabalho válido",
    "relocate": "🚚 Disponível para mudar de cidade",
    "video": "🎥 Vídeo",
    "photos": "📸 Fotos como modelo",
    "obs": "📝 Observações",
}

# Helper: keyboard for languages
def lang_keyboard():
    keyboard = [
        [InlineKeyboardButton(LANGUAGES[code], callback_data=f"lang_{code}")]
        for code in LANGUAGES.keys()
    ]
    return InlineKeyboardMarkup(keyboard)


def restart_kb(lang="en"):
    label = {"en": "🔄 Restart chat", "pt": "🔄 Reiniciar chat", "es": "🔄 Reiniciar chat", "ru": "🔄 Перезапустить чат"}.get(lang, "🔄 Restart chat")
    return InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data="restart")]])


# normalize yes/no answers across languages
def normalize_yesno(text):
    if not text:
        return None
    t = text.strip().lower()
    yes = {"s", "sim", "yes", "y", "да", "si"}
    no = {"n", "não", "nao", "no", "нет"}
    if t in yes:
        return "yes"
    if t in no:
        return "no"
    return None


# === Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # send language selection
    await update.message.reply_text("🌍 Please select your language / Por favor, selecione seu idioma:", reply_markup=lang_keyboard())


async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    if data.startswith("lang_"):
        await handle_lang_select(update, context)
    elif data == "restart":
        await handle_restart(update, context)
    elif data == "model_yes":
        await handle_model_yes(update, context)
    elif data == "model_no":
        await handle_model_no(update, context)
    else:
        await update.callback_query.answer()  # noop for unknowns


async def handle_lang_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_", 1)[1]
    # initialize user state
    context.user_data.clear()
    context.user_data["lang"] = lang
    context.user_data["q_idx"] = 0  # 0..11 where 9 = model question, 10 = video, 11 = obs
    context.user_data["answers"] = {}
    context.user_data["photos"] = []
    context.user_data["video_file_id"] = None
    context.user_data["expecting_photos"] = False
    context.user_data["expecting_video"] = False

    # show security msg then first question
    await query.edit_message_text(SECURITY[lang] + "\n\n" + FILL_CAREFULLY[lang], parse_mode="Markdown")
    # send first question after that (index 0)
    await query.message.reply_text(QUESTIONS[lang][0], reply_markup=restart_kb(lang), parse_mode="Markdown")


async def handle_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    # show language keyboard again
    await query.edit_message_text("🌍 Please select your language / Por favor, selecione seu idioma:", reply_markup=lang_keyboard())


async def handle_model_yes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")
    context.user_data["expecting_photos"] = True
    # ask user to send photos
    await query.edit_message_text(ASK_MODEL[lang] + "\n\n📸 Envie as fotos agora (mínimo 4).", reply_markup=restart_kb(lang))


async def handle_model_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")
    # store "no" for photos
    context.user_data["answers"]["photos"] = "No"
    # advance q_idx to next question (video), video is index 10 when counting our flow (we maintain mapping)
    context.user_data["q_idx"] = 10  # skip model question (9) and go to video (10)
    await query.edit_message_text({"en": "✅ OK, continuing...", "pt": "✅ Certo, continuando...", "es": "✅ Bien, continúo...", "ru": "✅ Хорошо, продолжаем..."}[lang], reply_markup=restart_kb(lang))
    # ask video question
    await query.message.reply_text(QUESTIONS[lang][10 - 1], reply_markup=restart_kb(lang), parse_mode="Markdown")  # index 9 in QUESTIONS includes video place earlier; ensure match


# text answers handler
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    q_idx = context.user_data.get("q_idx", 0)
    text = update.message.text.strip() if update.message.text else ""

    # If expecting photos, ignore text (ask to send photos)
    if context.user_data.get("expecting_photos"):
        await update.message.reply_text({"en": "📸 Please send photos (minimum 4).", "pt": "📸 Por favor, envie as fotos (mínimo 4).", "es": "📸 Por favor, envía las fotos (mínimo 4).", "ru": "📸 Пожалуйста, отправьте фотографии (минимум 4)."}[lang])
        return

    # If expecting video, ask to send video
    if context.user_data.get("expecting_video"):
        await update.message.reply_text({"en": "🎥 Please send your presentation video (as a video file).", "pt": "🎥 Por favor, envie seu vídeo de apresentação (como arquivo de vídeo).", "es": "🎥 Por favor, envía tu video de presentación (como archivo de video).", "ru": "🎥 Пожалуйста, отправьте ваше видео-презентацию (в виде файла)."}[lang])
        return

    # Map q_idx to correct question storage:
    # Our QUESTIONS list length is 11 (index 0..10). We treat model as a special at idx 9, video at idx10.
    # We keep q_idx counting 0..11 where:
    # 0..8 -> questions[0..8]
    # 9 -> model (handled by callbacks)
    # 10 -> video
    # 11 -> observation (questions[10])
    # However easier: if q_idx <=8 -> store in keys mapping
    keys_order = ["name", "age", "nationality", "experience", "languages", "location", "fines", "visa", "relocate"]
    if q_idx <= 8:
        key = keys_order[q_idx]
        context.user_data["answers"][key] = text
        context.user_data["q_idx"] = q_idx + 1
        # After storing, if next is model question (index 9)
        if context.user_data["q_idx"] == 9:
            # send model question buttons
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Sim / Yes", callback_data="model_yes"), InlineKeyboardButton("❌ Não / No", callback_data="model_no")]])
            await update.message.reply_text(ASK_MODEL[lang], reply_markup=kb)
            return
        # else ask next question
        next_q_idx = context.user_data["q_idx"]
        await update.message.reply_text(QUESTIONS[lang][next_q_idx], reply_markup=restart_kb(lang), parse_mode="Markdown")
        return

    # If q_idx == 10 (expecting video) and user sent text, remind them to send video
    if q_idx == 10:
        await update.message.reply_text({"en": "🎥 Please send your presentation video file (up to 1 minute).", "pt": "🎥 Por favor, envie seu vídeo de apresentação (arquivo, até 1 minuto).", "es": "🎥 Por favor, envía tu video de presentación (archivo, hasta 1 minuto).", "ru": "🎥 Пожалуйста, отправьте видео-презентацию (файл, до 1 минуты)."}[lang], reply_markup=restart_kb(lang))
        return

    # If q_idx == 11 (observations)
    if q_idx == 11:
        context.user_data["answers"]["obs"] = text
        context.user_data["q_idx"] = 12  # finish
        await finalize_and_send(update, context)
        return

    # Fallback
    await update.message.reply_text(QUESTIONS[lang][min(q_idx, len(QUESTIONS[lang]) - 1)], reply_markup=restart_kb(lang))


# photo handler (for model photos)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    if not context.user_data.get("expecting_photos"):
        # If not expecting photos, ignore or say how to use
        await update.message.reply_text({"en": "📷 If you want to add photos as a model, first press the model button.", "pt": "📷 Se desejar enviar fotos como modelo, primeiro selecione a opção modelo.", "es": "📷 Si deseas enviar fotos como modelo, primero selecciona la opción de modelo.", "ru": "📷 Если вы хотите отправить фото как модель, сначала выберите опцию модель."}[lang])
        return

    photo_file_id = update.message.photo[-1].file_id
    photos = context.user_data.get("photos", [])
    photos.append(photo_file_id)
    context.user_data["photos"] = photos
    remain = max(0, 4 - len(photos))
    if remain > 0:
        await update.message.reply_text({"en": f"📸 Received {len(photos)}. Please send {remain} more.", "pt": f"📸 Recebidas {len(photos)}. Envie mais {remain}.", "es": f"📸 Recibidas {len(photos)}. Por favor envía {remain} más.", "ru": f"📸 Получено {len(photos)}. Пожалуйста, отправьте еще {remain}."}[lang], reply_markup=restart_kb(lang))
        return
    # enough photos
    context.user_data["answers"]["photos"] = photos
    context.user_data["expecting_photos"] = False
    # advance to video question
    context.user_data["q_idx"] = 10
    await update.message.reply_text({"en": "✅ Photos received. Now please send your presentation video.", "pt": "✅ Fotos recebidas. Agora envie seu vídeo de apresentação.", "es": "✅ Fotos recibidas. Ahora envía tu video de presentación.", "ru": "✅ Фотографии получены. Теперь отправьте ваше видео-презентацию."}[lang], reply_markup=restart_kb(lang))


# video handler (for presentation video)
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    # accept video or document with video mime
    video = update.message.video or update.message.video_note
    doc = update.message.document
    file_id = None
    if video:
        file_id = video.file_id
    elif doc and doc.mime_type and doc.mime_type.startswith("video"):
        file_id = doc.file_id

    if not file_id:
        await update.message.reply_text({"en": "🎥 Please send a video file.", "pt": "🎥 Por favor, envie um arquivo de vídeo.", "es": "🎥 Por favor, envía un archivo de video.", "ru": "🎥 Пожалуйста, отправьте видеофайл."}[lang], reply_markup=restart_kb(lang))
        return

    context.user_data["video_file_id"] = file_id
    # after receiving video, advance to observation
    context.user_data["q_idx"] = 11
    await update.message.reply_text(QUESTIONS[lang][11 - 1], reply_markup=restart_kb(lang), parse_mode="Markdown")  # ask observation (index 10 in QUESTIONS is video originally)


async def finalize_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    answers = context.user_data.get("answers", {})
    photos = context.user_data.get("photos", [])
    video_id = context.user_data.get("video_file_id")

    # Try to save to DB if models exist (best-effort)
    try:
        from models import Candidate, session  # optional; will fail if models not present
        candidate = Candidate()
        for k, v in answers.items():
            try:
                setattr(candidate, k, v)
            except Exception:
                pass
        # if photos/video fields exist, set them too
        try:
            if photos:
                setattr(candidate, "photos", str(photos))
        except Exception:
            pass
        try:
            if video_id:
                setattr(candidate, "video_file_id", video_id)
        except Exception:
            pass
        session.add(candidate)
        session.commit()
    except Exception:
        # ignore DB errors silently but log
        logger.debug("DB save skipped or failed (no models configured).")

    # Build group message (Portuguese labels style, like your example)
    lines = ["📩 Novo candidato via SafeJob!", ""]
    # mapping from keys to labels in Portuguese
    lab = LABELS_PT
    lines.append(f"{lab['name']}: {answers.get('name','-')}")
    lines.append(f"{lab['age']}: {answers.get('age','-')}")
    lines.append(f"{lab['nationality']}: {answers.get('nationality','-')}")
    lines.append(f"{lab['experience']}: {answers.get('experience','-')}")
    lines.append(f"{lab['languages']}: {answers.get('languages','-')}")
    lines.append(f"{lab['location']}: {answers.get('location','-')}")
    lines.append(f"{lab['fines']}: {answers.get('fines','-')}")
    lines.append(f"{lab['visa']}: {answers.get('visa','-')}")
    lines.append(f"{lab['relocate']}: {answers.get('relocate','-')}")
    lines.append(f"{lab['obs']}: {answers.get('obs','-')}")
    msg_text = "\n".join(lines)

    # send to group: try send text + attachments
    try:
        if video_id:
            # try send video with caption (caption length limits)
            try:
                await context.bot.send_video(chat_id=GROUP_ID, video=video_id, caption=msg_text)
            except Exception:
                # fallback: send text then video
                await context.bot.send_message(chat_id=GROUP_ID, text=msg_text)
                await context.bot.send_video(chat_id=GROUP_ID, video=video_id)
        else:
            await context.bot.send_message(chat_id=GROUP_ID, text=msg_text)

        # send photos if exist (send as album if >=1)
        if photos:
            # photos is list of file_ids
            media_group = []
            from telegram import InputMediaPhoto
            for pid in photos:
                media_group.append(InputMediaPhoto(media=pid))
            try:
                await context.bot.send_media_group(chat_id=GROUP_ID, media=media_group)
            except Exception:
                # fallback: send individually
                for pid in photos:
                    await context.bot.send_photo(chat_id=GROUP_ID, photo=pid)
    except Exception as e:
        logger.exception("Failed to send candidate to group: %s", e)

    # confirm to user
    await update.message.reply_text({"en": "✅ Your info was submitted! We will contact you soon.", "pt": "✅ Suas informações foram enviadas! Em breve entraremos em contato.", "es": "✅ ¡Tu información ha sido enviada! Nos pondremos en contacto pronto.", "ru": "✅ Ваша информация отправлена! Мы свяжемся с вами в ближайшее время."}[lang], reply_markup=restart_kb(lang))

    # clear user data
    context.user_data.clear()


# === Setup application and handlers ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_router))
    # messages: text (answers), photos (model photos), video/document (presentation)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    # accept both video type and documents with video mime
    app.add_handler(MessageHandler(filters.VIDEO | filters.VideoNote | (filters.Document & filters.Document.MimeType("video/mp4")), handle_video))

    logger.info("Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()




