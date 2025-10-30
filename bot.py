import logging
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from models import Candidate, session  # seu models.py continua igual

# === CONFIGURAÇÕES ===
TOKEN = "8200201915:AAHxipR8nov2PSAJ3oJLIZDqplOnxhHYRUc"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# === TEXTOS EM 4 IDIOMAS ===
TEXTS = {
    "pt": {
        "welcome": "👋 Bem-vindo ao *SafeJob*! 💼\nEncontre oportunidades incríveis de trabalho em Bavet e região.",
        "ask_name": "🧾 Por favor, digite seu *nome completo*:",
        "ask_age": "🎂 Informe sua *idade*:",
        "ask_experience": "💼 Conte um pouco sobre sua *experiência profissional*: ",
        "ask_contact": "📞 Envie seu *número de contato* ou *Telegram*:",
        "saved": "✅ Suas informações foram salvas com sucesso! Em breve entraremos em contato. 🤝",
        "restart": "🔄 Reiniciar chat"
    },
    "en": {
        "welcome": "👋 Welcome to *SafeJob*! 💼\nFind amazing job opportunities in Bavet and nearby areas.",
        "ask_name": "🧾 Please enter your *full name*: ",
        "ask_age": "🎂 Enter your *age*: ",
        "ask_experience": "💼 Tell us about your *work experience*: ",
        "ask_contact": "📞 Send your *contact number* or *Telegram username*: ",
        "saved": "✅ Your information has been saved successfully! We'll contact you soon. 🤝",
        "restart": "🔄 Restart chat"
    },
    "es": {
        "welcome": "👋 ¡Bienvenido a *SafeJob*! 💼\nEncuentra increíbles oportunidades de trabajo en Bavet y alrededores.",
        "ask_name": "🧾 Por favor, escribe tu *nombre completo*: ",
        "ask_age": "🎂 Indica tu *edad*: ",
        "ask_experience": "💼 Cuéntanos sobre tu *experiencia laboral*: ",
        "ask_contact": "📞 Envíanos tu *número de contacto* o *usuario de Telegram*: ",
        "saved": "✅ ¡Tu información ha sido guardada con éxito! Te contactaremos pronto. 🤝",
        "restart": "🔄 Reiniciar chat"
    },
    "ru": {
        "welcome": "👋 Добро пожаловать в *SafeJob*! 💼\nНайдите отличные рабочие возможности в Бавете и поблизости.",
        "ask_name": "🧾 Пожалуйста, введите ваше *полное имя*: ",
        "ask_age": "🎂 Укажите ваш *возраст*: ",
        "ask_experience": "💼 Расскажите о вашем *опыте работы*: ",
        "ask_contact": "📞 Отправьте ваш *контактный номер* или *Telegram*: ",
        "saved": "✅ Ваша информация успешно сохранена! Мы свяжемся с вами в ближайшее время. 🤝",
        "restart": "🔄 Перезапустить чат"
    }
}

# === ESCOLHA DE IDIOMA ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🇧🇷 Português", callback_data="lang_pt"),
            InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
        ],
        [
            InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")
        ]
    ]
    await update.message.reply_text(
        "🌐 *Escolha seu idioma / Choose your language / Elige tu idioma / Выберите язык:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# === FUNÇÃO DE REINÍCIO ===
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(query, context)

# === PROCESSO DE CADASTRO ===
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[1]
    context.user_data["lang"] = lang
    await query.edit_message_text(
        TEXTS[lang]["welcome"],
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(TEXTS[lang]["restart"], callback_data="restart")]
        ])
    )
    await query.message.reply_text(TEXTS[lang]["ask_name"])

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "pt")

    if "name" not in context.user_data:
        context.user_data["name"] = update.message.text
        await update.message.reply_text(TEXTS[lang]["ask_age"])
        return

    if "age" not in context.user_data:
        context.user_data["age"] = update.message.text
        await update.message.reply_text(TEXTS[lang]["ask_experience"])
        return

    if "experience" not in context.user_data:
        context.user_data["experience"] = update.message.text
        await update.message.reply_text(TEXTS[lang]["ask_contact"])
        return

    if "contact" not in context.user_data:
        context.user_data["contact"] = update.message.text

        # salvar no banco
        candidate = Candidate(
            name=context.user_data["name"],
            age=context.user_data["age"],
            experience=context.user_data["experience"],
            contact=context.user_data["contact"]
        )
        session.add(candidate)
        session.commit()

        await update.message.reply_text(
            TEXTS[lang]["saved"],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(TEXTS[lang]["restart"], callback_data="restart")]
            ])
        )
        context.user_data.clear()

# === MAIN ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(restart, pattern="restart"))
    app.add_handler(CallbackQueryHandler(button, pattern="lang_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()


