# bot.py
# -*- coding: utf-8 -*-
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# -------------------------
# CONFIG
# -------------------------
# coloque seu token no Railway/ambiente: TOKEN
TOKEN = os.environ.get("TOKEN", "8200201915:AAHxipR8nov2PSAJ3oJLIZDqplOnxhHYRUc")
# Grupo (use inteiro, não string)
GROUP_ID = int(os.environ.get("GROUP_ID", "-5014344988"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------
# TEXTS / QUESTIONS
# -------------------------
LANGUAGES = {
    "en": "🇬🇧 English",
    "pt": "🇧🇷 Português",
    "es": "🇪🇸 Español",
    "ru": "🇷🇺 Русский",
}

SECURITY_MSG = {
    "en": "🔒 Welcome to SafeJob!\nEvery job opportunity shared here is carefully reviewed by our team.\nPlease fill your information carefully so our support team can find the best position for you.",
    "pt": "🔒 Bem-vindo ao SafeJob!\nTodas as vagas publicadas aqui são cuidadosamente analisadas pela nossa equipe.\nPor favor, preencha suas informações com cuidado para que a equipe encontre a melhor vaga para você.",
    "es": "🔒 ¡Bienvenido a SafeJob!\nTodas las ofertas publicadas aquí son revisadas cuidadosamente por nuestro equipo.\nPor favor, completa tu información con cuidado para que el equipo encuentre la mejor vacante para ti.",
    "ru": "🔒 Добро пожаловать в SafeJob!\nВсе вакансии тщательно проверяются нашей командой.\nПожалуйста, заполняйте информацию внимательно, чтобы команда могла подобрать лучшую работу для вас.",
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
        "1️⃣2️⃣ Any additional notes?",
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
        "1️⃣2️⃣ Alguma observação adicional?",
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
        "1️⃣2️⃣ Alguna observación adicional?",
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
        "1️⃣2️⃣ Дополнительные заметки?",
    ],
}

# -------------------------
# HELPERS
# -------------------------
def lang_keyboard():
    # keyboard inline com cada idioma em uma linha (mantive simples)
    keyboard = [[InlineKeyboardButton(name, callback_data=code)] for code, name in LANGUAGES.items()]
    return InlineKeyboardMarkup(keyboard)


def restart_keyboard(lang="en"):
    labels = {
        "en": "🔄 Restart chat",
        "pt": "🔄 Reiniciar chat",
        "es": "🔄 Reiniciar chat",
        "ru": "🔄 Перезапустить чат",
    }
    return InlineKeyboardMarkup([[InlineKeyboardButton(labels.get(lang, "🔄 Restart chat"), callback_data="restart")]])


def is_negative_answer(text: str) -> bool:
    if not text:
        return False
    t = text.strip().lower()
    return t in {"no", "n", "não", "nao", "нет"}


# -------------------------
# HANDLERS
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # mostra teclado de idiomas
    await update.message.reply_text(
        "🌐 Select your language / Selecione seu idioma / Seleccione su idioma / Выберите язык:",
        reply_markup=lang_keyboard(),
    )


async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # único handler de callbacks (idioma e restart)
    data = update.callback_query.data
    if data == "restart":
        await handle_restart(update, context)
    elif data in LANGUAGES:
        await handle_language_select(update, context)
    else:
        # desconhecido
        await update.callback_query.answer()


async def handle_language_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data  # 'pt','en',...
    # inicializa estado do usuário
    context.user_data.clear()
    context.user_data["lang"] = lang
    context.user_data["q_index"] = 0
    context.user_data["answers"] = {}  # map key -> value
    context.user_data["photos"] = []
    context.user_data["video_file_id"] = None
    context.user_data["expect_photos"] = False
    context.user_data["expect_video"] = False

    # mostra mensagem de segurança + instrução para preencher com cuidado
    sec = SECURITY_MSG.get(lang, SECURITY_MSG["en"])
    await query.edit_message_text(sec, parse_mode=None)
    # envia primeira pergunta
    await query.message.reply_text(QUESTIONS[lang][0], reply_markup=restart_keyboard(lang))


async def handle_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # limpa estado e volta para seleção de idioma
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.edit_message_text("🌐 Select your language / Selecione seu idioma:", reply_markup=lang_keyboard())


async def ask_next_question_by_index(chat, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    idx = context.user_data.get("q_index", 0)
    # se terminou
    if idx >= len(QUESTIONS[lang]):
        # finalizar
        # create fake update-like object for finalize (we'll call finalize via chat)
        return False
    # pergunta atual
    await chat.send_message(QUESTIONS[lang][idx], reply_markup=restart_keyboard(lang))
    return True


async def ask_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # wrapper: envia next question usando update context
    if update.callback_query:
        chat = update.callback_query.message.chat
    else:
        chat = update.message.chat
    cont = await ask_next_question_by_index(chat, context)
    if not cont:
        # if finished, finalize:
        await finalize_and_send(update, context)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Captura respostas de texto e encaminha o fluxo."""
    if "q_index" not in context.user_data:
        # não iniciado
        return

    lang = context.user_data.get("lang", "en")
    idx = context.user_data.get("q_index", 0)
    text = (update.message.text or "").strip()

    # Safety: if expecting photos or video, guide accordingly
    if context.user_data.get("expect_photos"):
        await update.message.reply_text({"en": "📸 Please send photos (minimum 4).", "pt": "📸 Por favor, envie fotos (mínimo 4)."}[lang])
        return
    if context.user_data.get("expect_video"):
        await update.message.reply_text({"en": "🎥 Please send your presentation video (file).", "pt": "🎥 Por favor, envie seu vídeo de apresentação (arquivo)."}[lang])
        return

    # If current question is the model question (index 9) -> special handling
    # Note: our QUESTIONS lists place the model question at index 9 (0-based)
    if QUESTIONS[lang][idx].startswith("🔟"):
        # user answered Yes or No
        if is_negative_answer(text):
            # store explicit "No" and jump to next question (video)
            context.user_data["answers"][f"q_{idx}"] = "No"
            context.user_data["q_index"] = idx + 1
            # ask next
            await ask_next_question(update, context)
            return
        else:
            # treat as yes (or anything else) -> expect photos
            context.user_data["answers"][f"q_{idx}"] = "Yes"
            context.user_data["expect_photos"] = True
            await update.message.reply_text({"en": "📸 Please send at least 4 photos now.", "pt": "📸 Por favor, envie pelo menos 4 fotos agora."}[lang])
            return

    # Normal questions: store answer
    context.user_data["answers"][f"q_{idx}"] = text
    context.user_data["q_index"] = idx + 1

    # If next question is model (handled above), ask it; else send next normally
    # Ask next (or finalize if none)
    await ask_next_question(update, context)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Coleta fotos quando expect_photos == True."""
    if "q_index" not in context.user_data:
        return
    lang = context.user_data.get("lang", "en")
    if not context.user_data.get("expect_photos"):
        # ignore or instruct
        await update.message.reply_text({"en": "📷 To send photos as a model, first answer the model question 'Yes'.", "pt": "📷 Para enviar fotos como modelo, primeiro responda a pergunta de modelo 'Sim'."}[lang])
        return

    # Append photo file_id
    photo_file_id = update.message.photo[-1].file_id
    context.user_data["photos"].append(photo_file_id)
    count = len(context.user_data["photos"])

    if count < 4:
        await update.message.reply_text({"en": f"📸 {count}/4 received. Send {4 - count} more.", "pt": f"📸 {count}/4 recebidas. Envie mais {4 - count} fotos."}[lang])
        return

    # enough photos collected
    context.user_data["expect_photos"] = False
    # advance q_index to next question (video)
    context.user_data["q_index"] = context.user_data.get("q_index", 0) + 1
    await update.message.reply_text({"en": "✅ Photos received. Now please send your presentation video.", "pt": "✅ Fotos recebidas. Agora envie seu vídeo de apresentação."}[lang])
    # ask next question (which should be video prompt)
    await ask_next_question(update, context)


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Captura vídeo (video message ou document mp4)."""
    if "q_index" not in context.user_data:
        return
    lang = context.user_data.get("lang", "en")
    idx = context.user_data.get("q_index", 0)

    # determine file id
    file_id = None
    if update.message.video:
        file_id = update.message.video.file_id
    elif update.message.document and update.message.document.mime_type and update.message.document.mime_type.startswith("video"):
        file_id = update.message.document.file_id

    if not file_id:
        await update.message.reply_text({"en": "🎥 Please send a video file.", "pt": "🎥 Por favor, envie um arquivo de vídeo."}[lang])
        return

    # save video file id
    context.user_data["video_file_id"] = file_id
    # advance to next (observation)
    context.user_data["q_index"] = idx + 1
    await update.message.reply_text({"en": "✅ Video received. Please answer the next question.", "pt": "✅ Vídeo recebido. Por favor, responda a próxima pergunta."}[lang])
    await ask_next_question(update, context)


async def finalize_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Monta a mensagem e envia ao grupo; limpa user_data no final."""
    lang = context.user_data.get("lang", "en")
    answers = context.user_data.get("answers", {})
    photos = context.user_data.get("photos", [])
    video_id = context.user_data.get("video_file_id")

    # Build message in PT format similar to your example (you can change language logic as needed)
    msg_lines = ["📩 Novo candidato via SafeJob!", ""]
    # try to map the stored answers to labels by index
    # we iterate keys q_0..q_n in order
    keys = sorted(k for k in answers.keys() if k.startswith("q_"))
    for k in keys:
        idx = int(k.split("_", 1)[1])
        qtext = QUESTIONS.get(lang, QUESTIONS["pt"])[idx] if idx < len(QUESTIONS.get(lang, [])) else f"Q{idx}"
        ans = answers[k]
        msg_lines.append(f"{qtext}\n➡️ {ans}\n")

    # add info about photos/video
    if photos:
        msg_lines.append(f"📸 Photos: {len(photos)} attached.")
    if video_id:
        msg_lines.append(f"🎥 Video: attached.")

    final_text = "\n".join(msg_lines)

    try:
        # send text summary
        await context.bot.send_message(chat_id=GROUP_ID, text=final_text)
        # send photos as media group if >=1
        if photos:
            from telegram import InputMediaPhoto
            media = [InputMediaPhoto(media=p) for p in photos]
            # send media group (Telegram allows up to 10)
            try:
                await context.bot.send_media_group(chat_id=GROUP_ID, media=media)
            except Exception:
                # fallback send individually
                for p in photos:
                    await context.bot.send_photo(chat_id=GROUP_ID, photo=p)
        # send video if exists
        if video_id:
            try:
                await context.bot.send_video(chat_id=GROUP_ID, video=video_id)
            except Exception:
                logger.exception("Could not send video to group.")
    except Exception:
        logger.exception("Failed to send candidate to group.")

    # confirmation to user
    reply_chat = update.effective_chat if update else None
    if reply_chat:
        await context.bot.send_message(chat_id=reply_chat.id, text={"en": "✅ Your info was submitted! We'll contact you soon.", "pt": "✅ Suas informações foram enviadas! Em breve entraremos em contato."}.get(lang, "✅ Submitted."))

    # clear state
    context.user_data.clear()


# -------------------------
# SETUP / MAIN
# -------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Command
    app.add_handler(CommandHandler("start", start))
    # Callback router (idiomas e restart)
    app.add_handler(CallbackQueryHandler(callback_router))
    # Text answers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    # Photos
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    # Video files (video messages) or documents with video mime
    video_filter = filters.VIDEO | filters.Document.MimeType("video/mp4")
    app.add_handler(MessageHandler(video_filter, handle_video))

    logger.info("SafeJob bot started.")
    app.run_polling()


if __name__ == "__main__":
    main()
