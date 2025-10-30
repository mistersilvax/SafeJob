# bot_safejob_final.py
# -*- coding: utf-8 -*-
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ======================
# CONFIGURAÇÕES
# ======================
TOKEN = "8200201915:AAHxipR8nov2PSAJ3oJLIZDqplOnxhHYRUc"            # <-- coloque seu token aqui
GROUP_ID = int("-5014344988")      # <-- grupo destino (inteiro)

LANGUAGES = {
    "en": "🇬🇧 English",
    "pt": "🇧🇷 Português",
    "es": "🇪🇸 Español",
    "ru": "🇷🇺 Русский",
}

SECURITY_MSG = {
    "en": "🔒 Welcome to SafeJob!\nEvery job opportunity shared here is carefully reviewed by our team.\nPlease fill in your information carefully so our team can find the best position for you.",
    "pt": "🔒 Bem-vindo ao SafeJob!\nTodas as vagas publicadas aqui são cuidadosamente analisadas pela nossa equipe.\nPor favor, preencha suas informações com atenção para que possamos encontrar a melhor vaga para você.",
    "es": "🔒 ¡Bienvenido a SafeJob!\nTodas las vacantes aquí son revisadas cuidadosamente por nuestro equipo.\nPor favor, completa tu información con atención para que podamos encontrar el mejor puesto para ti.",
    "ru": "🔒 Добро пожаловать в SafeJob!\nВсе вакансии тщательно проверяются нашей командой.\nПожалуйста, заполняйте данные внимательно, чтобы мы могли подобрать лучшую вакансию для вас.",
}

FINAL_MSG = {
    "en": "✅ Thank you! Our team will review your information and contact you soon. 🔎",
    "pt": "✅ Obrigado! Nossa equipe irá analisar suas informações e entrará em contato em breve. 🔎",
    "es": "✅ ¡Gracias! Nuestro equipo revisará tu información y se pondrá en contacto pronto. 🔎",
    "ru": "✅ Спасибо! Наша команда проверит вашу информацию и свяжется с вами в ближайшее время. 🔎",
}

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
        "📝 Any additional notes?",
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
        "📝 Alguma observação adicional?",
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
        "📝 ¿Alguna observación adicional?",
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
        "📝 Дополнительные заметки?",
    ],
}

# rótulos para montar a mensagem final (mantemos PT-like labels conforme exemplo)
FIELDS_LABELS = {
    "pt": [
        "👤 Nome",
        "🎂 Idade",
        "🏳️ Nacionalidade",
        "💼 Experiência",
        "🌐 Idiomas",
        "📍 Localização",
        "⚠️ Multas",
        "🛂 Visto de trabalho válido",
        "🚚 Disponível para mudar de cidade",
        "📸 Modelo (enviou fotos?)",
        "🎥 Vídeo de apresentação",
        "📱 Telegram",
        "📝 Observações",
    ],
    "en": [
        "👤 Name",
        "🎂 Age",
        "🏳️ Nationality",
        "💼 Experience",
        "🌐 Languages",
        "📍 Location",
        "⚠️ Fines",
        "🛂 Valid work visa",
        "🚚 Available to relocate",
        "📸 Model (sent photos?)",
        "🎥 Presentation video",
        "📱 Telegram",
        "📝 Notes",
    ],
    "es": [
        "👤 Nombre",
        "🎂 Edad",
        "🏳️ Nacionalidad",
        "💼 Experiencia",
        "🌐 Idiomas",
        "📍 Ubicación",
        "⚠️ Multas",
        "🛂 Visa de trabajo válida",
        "🚚 Disponible para mudarse",
        "📸 Modelo (envió fotos?)",
        "🎥 Video de presentación",
        "📱 Telegram",
        "📝 Observaciones",
    ],
    "ru": [
        "👤 Имя",
        "🎂 Возраст",
        "🏳️ Национальность",
        "💼 Опыт",
        "🌐 Языки",
        "📍 Местоположение",
        "⚠️ Штрафы",
        "🛂 Рабочая виза",
        "🚚 Готов к переезду",
        "📸 Модель (фото?)",
        "🎥 Видео",
        "📱 Telegram",
        "📝 Примечания",
    ],
}


# Helper para detectar resposta negativa
def is_negative_answer(text: str) -> bool:
    if not text:
        return False
    t = text.strip().lower()
    return t in {"no", "n", "não", "nao", "нет"}


# ======================
# HANDLERS DO BOT
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=code)] for code, name in LANGUAGES.items()]
    await update.message.reply_text(
        "🌐 Select your language / Selecione seu idioma / Seleccione su idioma / Выберите язык:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data
    # init user state
    context.user_data.clear()
    context.user_data["lang"] = lang
    context.user_data["q_index"] = 0
    context.user_data["answers"] = {}   # stores answers by index: "answer_0"...
    context.user_data["photos"] = []    # list of file_ids
    context.user_data["video"] = None   # file_id
    context.user_data["expect_photos"] = False

    # Send security notice and first question
    await query.message.reply_text(SECURITY_MSG[lang])
    await ask_next_question(update, context)


async def ask_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "pt")
    idx = context.user_data.get("q_index", 0)
    questions = QUESTIONS[lang]
    if idx >= len(questions):
        # finalize
        await send_to_group(update, context)
        # send thank you to user
        await update.effective_chat.send_message(FINAL_MSG[lang])
        context.user_data.clear()
        return
    # ask current question
    question = questions[idx]
    keyboard = [[InlineKeyboardButton("🔄 Restart / Reiniciar / Перезапустить", callback_data="restart")]]
    await update.effective_chat.send_message(question, reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "q_index" not in context.user_data:
        return
    lang = context.user_data.get("lang", "pt")
    idx = context.user_data["q_index"]
    text = (update.message.text or "").strip()

    # If expecting photos, ignore text and ask to send photos
    if context.user_data.get("expect_photos"):
        await update.message.reply_text({"pt": "📸 Por favor envie fotos (mínimo 4).", "en": "📸 Please send photos (minimum 4)."}[lang])
        return

    # If current question is the model question (index 9)
    if QUESTIONS[lang][idx].startswith("📸"):
        if is_negative_answer(text):
            # store "No" and skip to next
            context.user_data["answers"][f"answer_{idx}"] = "Não" if lang == "pt" else "No"
            context.user_data["q_index"] = idx + 1
            await ask_next_question(update, context)
            return
        else:
            # assume yes -> expect photos now
            context.user_data["answers"][f"answer_{idx}"] = "Sim" if lang == "pt" else "Yes"
            context.user_data["expect_photos"] = True
            await update.message.reply_text({"pt": "📸 Envie pelo menos 4 fotos agora.", "en": "📸 Please send at least 4 photos now."}[lang])
            return

    # Save normal answer
    context.user_data["answers"][f"answer_{idx}"] = text or "-"
    context.user_data["q_index"] = idx + 1
    await ask_next_question(update, context)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "q_index" not in context.user_data:
        return
    lang = context.user_data.get("lang", "pt")
    if not context.user_data.get("expect_photos"):
        await update.message.reply_text({"pt": "📷 Para enviar fotos como modelo, responda 'Sim' na pergunta de modelo.", "en": "📷 To send photos as a model, answer 'Yes' to the model question."}[lang])
        return
    file_id = update.message.photo[-1].file_id
    context.user_data["photos"].append(file_id)
    count = len(context.user_data["photos"])
    if count < 4:
        await update.message.reply_text({"pt": f"📸 {count}/4 recebidas. Envie mais {4 - count}.", "en": f"📸 {count}/4 received. Send {4 - count} more."}[lang])
        return
    # enough photos collected
    context.user_data["expect_photos"] = False
    # mark that model question answer stored already; advance
    context.user_data["q_index"] = context.user_data.get("q_index", 0) + 1
    await update.message.reply_text({"pt": "✅ Fotos recebidas. Agora envie seu vídeo (se tiver).", "en": "✅ Photos received. Now send your video (if you have one)."}[lang])
    await ask_next_question(update, context)


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "q_index" not in context.user_data:
        return
    file_id = None
    if update.message.video:
        file_id = update.message.video.file_id
    elif update.message.document and update.message.document.mime_type and update.message.document.mime_type.startswith("video"):
        file_id = update.message.document.file_id
    if not file_id:
        lang = context.user_data.get("lang", "pt")
        await update.message.reply_text({"pt": "🎥 Por favor envie um arquivo de vídeo válido.", "en": "🎥 Please send a valid video file."}[lang])
        return
    context.user_data["video"] = file_id
    # store a marker in answers for the video question slot if you want
    # advance to next question
    context.user_data["q_index"] = context.user_data.get("q_index", 0) + 1
    await ask_next_question(update, context)


async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    if data == "restart":
        await handle_restart(update, context)
    elif data in LANGUAGES:
        await language_choice(update, context)
    else:
        await update.callback_query.answer()


async def handle_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.edit_message_text("🌐 Select your language / Selecione seu idioma:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(name, callback_data=code)] for code, name in LANGUAGES.items()]))


# ======================
# ENVIO AGRUPADO (texto + mídia juntos)
# ======================

def build_final_text(data: dict, lang: str) -> str:
    labels = FIELDS_LABELS.get(lang, FIELDS_LABELS["pt"])
    # Build list of values for indices 0..12
    lines = ["📩 Novo candidato via SafeJob!", ""]
    for i, label in enumerate(labels):
        key = f"answer_{i}"
        value = data.get("answers", {}).get(key)
        # for the model and video fields, show yes/no or presence
        if i == 9:
            # model field: if photos exist -> "Sim" else check stored answer
            if data.get("photos"):
                val = "Sim" if lang == "pt" else "Yes"
            else:
                val = data.get("answers", {}).get(key, "Não" if lang == "pt" else "No")
            value = val
        elif i == 10:
            # video field: show "Sim" if video present else the stored answer or "-"
            value = "Sim" if data.get("video") else (data.get("answers", {}).get(key, "-"))
        elif value is None:
            value = data.get("answers", {}).get(key, "-")
        lines.append(f"{label}: {value}")
    return "\n".join(lines)


async def send_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = {
        "answers": context.user_data.get("answers", {}),
        "photos": context.user_data.get("photos", []),
        "video": context.user_data.get("video"),
        "lang": context.user_data.get("lang", "pt"),
    }
    lang = data["lang"]
    final_text = build_final_text(data, lang)

    photos = data.get("photos", [])[:]  # copy
    video_id = data.get("video")

    # Build media list: prefer putting the video as the first media (so caption can be attached to it)
    media_items = []
    if video_id:
        media_items.append(InputMediaVideo(media=video_id, caption=final_text, parse_mode=None))
    # add photos
    for p in photos:
        media_items.append(InputMediaPhoto(media=p))

    try:
        if media_items:
            # Telegram allows up to 10 items per media_group
            # We'll split into chunks of 10. Caption should be on the first media of the first group.
            groups = [media_items[i:i + 10] for i in range(0, len(media_items), 10)]
            # For groups after the first, remove captions (they are already in the first group)
            # If the first group's first item DOES NOT have caption (edge-case), ensure it does.
            # Send each group
            for gi, grp in enumerate(groups):
                # only the first group's first media keeps caption (already set)
                if gi > 0:
                    # remove caption attribute for all items in subsequent groups (if any)
                    for m in grp:
                        try:
                            m.caption = None
                        except Exception:
                            pass
                # send media group
                await context.bot.send_media_group(chat_id=GROUP_ID, media=grp)
        else:
            # no media: simply send message
            await context.bot.send_message(chat_id=GROUP_ID, text=final_text)
    except Exception as e:
        # If media_group fails, fallback to send text then media individually
        try:
            await context.bot.send_message(chat_id=GROUP_ID, text=final_text)
            for p in photos:
                await context.bot.send_photo(chat_id=GROUP_ID, photo=p)
            if video_id:
                await context.bot.send_video(chat_id=GROUP_ID, video=video_id, caption="🎥 Vídeo de apresentação")
        except Exception:
            # give up but log
            print("Failed to send media to group:", e)

# ======================
# BOOT
# ======================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    # video or mp4 document
    video_filter = filters.VIDEO | filters.Document.MimeType("video/mp4")
    app.add_handler(MessageHandler(video_filter, handle_video))

    print("SafeJob bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()


