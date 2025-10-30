# -*- coding: utf-8 -*-
import logging, os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime
import config
from models import Candidate, session
from utils import save_resume, save_video

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Multilingual texts (short)
TEXTS = {
    'en': {
        'welcome_title': '?? Welcome to SafeJob!',
        'welcome_body': 'Every job opportunity shared here is carefully reviewed by our team. We make sure all openings are safe, transparent, and real — to help you find stable work.',
        'choose_lang': '?? Select your language:',
        'thanks': '? Thank you! Your information was submitted. Our team will contact you soon.'
    },
    'pt': {
        'welcome_title': '?? Bem-vindo ao SafeJob!',
        'welcome_body': 'Todas as vagas publicadas aqui são cuidadosamente analisadas pela nossa equipe.',
        'choose_lang': '?? Selecione seu idioma:',
        'thanks': '? Obrigado! Seus dados foram enviados. Nossa equipe entrará em contato em breve.'
    },
    'es': {
        'welcome_title': '?? ¡Bienvenido a SafeJob!',
        'welcome_body': 'Todas las ofertas publicadas aquí son revisadas cuidadosamente por nuestro equipo.',
        'choose_lang': '?? Selecciona tu idioma:',
        'thanks': '? ¡Gracias! Tus datos han sido enviados. Nuestro equipo te contactará pronto.'
    },
    'ru': {
        'welcome_title': '?? ????? ?????????? ? SafeJob!',
        'welcome_body': '??? ????????, ??????????? ?????, ????????? ??????????? ????? ????????.',
        'choose_lang': '?? ???????? ????:',
        'thanks': '? ???????! ???? ?????? ??????????. ???? ??????? ???????? ? ????.'
    }
}

# Steps
STEPS = [
    'name','age','nationality','experience','languages','location',
    'fines','work_visa','relocate','need_passport_help','need_police_help',
    'resume','video','notes'
]

# in-memory session (small scale)
sessions = {}

def detect_lang_choice(text: str) -> str:
    t = text.lower()
    if 'english' in t or '????' in text: return 'en'
    if 'portug' in t or '????' in text or 'português' in t: return 'pt'
    if 'españ' in t or 'espan' in t or '????' in text: return 'es'
    if '???' in t or '????' in text: return 'ru'
    return 'en'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    sessions[chat_id] = {'step': None, 'lang': 'en', 'data': {}}
    kb = [['???? English','???? Português'],['???? Español','???? ???????']]
    await update.message.reply_text(TEXTS['en']['welcome_title'])
    await update.message.reply_text(TEXTS['en']['welcome_body'])
    await update.message.reply_text(TEXTS['en']['choose_lang'], reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True))

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text
    sess = sessions.get(chat_id)
    if not sess:
        await start(update, context)
        return

    # language chooser step
    if sess['step'] is None:
        lang = detect_lang_choice(text)
        sess['lang'] = lang
        sess['step'] = STEPS[0]
        # ask first question in chosen language
        q = {
            'en':'What is your full name?',
            'pt':'Qual é o seu nome completo?',
            'es':'¿Cuál es tu nombre completo?',
            'ru':'???? ?????? ????'
        }[lang]
        await update.message.reply_text(q)
        return

    step = sess['step']
    lang = sess['lang']
    data = sess['data']

    # store simple text answers
    if step in ['name','age','nationality','experience','languages','location']:
        data[step] = text
        next_i = STEPS.index(step) + 1
        sess['step'] = STEPS[next_i]
        # ask next in chosen language
        prompts = {
            'age': {'en':'How old are you?','pt':'Qual é a sua idade?','es':'¿Cuántos años tienes?','ru':'??????? ??? ????'},
            'nationality': {'en':'What is your nationality?','pt':'Qual é a sua nacionalidade?','es':'¿Cuál es tu nacionalidad?','ru':'????? ? ??? ???????????????'},
            'experience': {'en':'Briefly describe your work experience','pt':'Fale um pouco sobre suas experiências profissionais','es':'Describe brevemente tu experiencia laboral','ru':'?????? ??????? ??? ???? ??????'},
            'languages': {'en':'Which languages do you speak?','pt':'Quais idiomas você fala?','es':'¿Qué idiomas hablas?','ru':'?????? ??????? ?? ?????????'},
            'location': {'en':'Where are you currently located?','pt':'Onde você está localizado atualmente?','es':'¿Dónde te encuentras actualmente?','ru':'??? ?? ?????? ???????????'}
        }
        await update.message.reply_text(prompts.get(sess['step'], {}).get(lang, ''))
        return

    if step in ['fines','work_visa','relocate','need_passport_help','need_police_help']:
        data[step] = text
        next_i = STEPS.index(step) + 1
        sess['step'] = STEPS[next_i]
        if sess['step'] == 'resume':
            await update.message.reply_text({
                'en':'Please send your resume (PDF/DOC/DOCX/JPG/PNG).',
                'pt':'Envie seu currículo (PDF/DOC/DOCX/JPG/PNG).',
                'es':'Envíe su currículum (PDF/DOC/DOCX/JPG/PNG).',
                'ru':'????????? ???? ?????? (PDF/DOC/DOCX/JPG/PNG).'
            }[lang])
        else:
            # ask next question
            prompts = {
                'fines': {'en':'Do you have any fines to pay? (Yes/No)','pt':'Você possui multas para pagar? (Sim/Não)','es':'¿Tienes multas pendientes? (Si/No)','ru':'? ??? ???? ??????? (??/???)'},
                'work_visa': {'en':'Do you have a valid work visa? (Yes/No)','pt':'Possui visto de trabalho válido? (Sim/Não)','es':'¿Tienes visa de trabajo válida? (Si/No)','ru':'? ??? ???? ??????????? ??????? ????? (??/???)'},
                'relocate': {'en':'Are you available to relocate? (Yes/No)','pt':'Está disponível para mudar de cidade? (Sim/Não)','es':'¿Estás disponible para reubicarte? (Si/No)','ru':'?????? ?? ?? ?????????? (??/???)'},
                'need_passport_help': {'en':'Do you need help recovering your passport? (Yes/No)','pt':'Precisa de ajuda para recuperar seu passaporte? (Sim/Não)','es':'¿Necesitas ayuda para recuperar tu pasaporte? (Si/No)','ru':'????? ?? ??? ?????? ? ?????????????? ????????? (??/???)'},
                'need_police_help': {'en':'Do you need police assistance? (Yes/No)','pt':'Precisa de ajuda policial? (Sim/Não)','es':'¿Necesitas ayuda policial? (Si/No)','ru':'????? ?? ??? ?????? ???????? (??/???)'}
            }
            await update.message.reply_text(prompts.get(step, {}).get(lang, ''))
        return

    if step == 'notes':
        data['notes'] = text
        # finalize: save to DB and notify staff
        data['lang'] = lang
        data['created_at'] = datetime.utcnow().isoformat()
        # Map only fields in model
        cand_kwargs = {k: v for k, v in data.items() if k in Candidate.__table__.columns.keys()}
        candidate = Candidate(**cand_kwargs)
        session.add(candidate)
        session.commit()

        await notify_staff(context, data)
        link = config.PUBLIC_JOBS_GROUP_LINK
        await update.message.reply_text(TEXTS[lang]['thanks'] + f"\n\nCheck open positions: {link}")
        # clear session
        sess['step'] = None
        sess['data'] = {}
        return

    # fallback
    await update.message.reply_text("Please follow the instructions or send /start to begin.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    sess = sessions.get(chat_id)
    if not sess:
        await start(update, context); return
    step = sess['step']
    if step != 'resume':
        await update.message.reply_text("Unexpected file. Please follow the instructions or send /start.")
        return
    doc = update.message.document
    if not doc:
        await update.message.reply_text("No document found.")
        return
    # download
    file = await context.bot.get_file(doc.file_id)
    content = await file.download_as_bytearray()
    path = save_resume(doc.file_name or "resume", content)
    sess['data']['resume_path'] = path
    sess['step'] = 'video'
    await update.message.reply_text({
        'en':'Now send a short video presentation (MP4).',
        'pt':'Agora envie seu vídeo de apresentação (MP4).',
        'es':'Ahora envía un video de presentación (MP4).',
        'ru':'?????? ????????? ???????? ?????-??????????? (MP4).'
    }[sess['lang']])

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    sess = sessions.get(chat_id)
    if not sess:
        await start(update, context); return
    step = sess['step']
    if step != 'video':
        await update.message.reply_text("Unexpected video. Please follow the instructions or send /start.")
        return
    video = update.message.video
    if not video:
        await update.message.reply_text("No video found.")
        return
    file = await context.bot.get_file(video.file_id)
    content = await file.download_as_bytearray()
    path = save_video(video.file_name or "video.mp4", content)
    sess['data']['video_path'] = path
    sess['step'] = 'notes'
    await update.message.reply_text({
        'en':'Any additional notes?',
        'pt':'Deseja adicionar alguma observação?',
        'es':'¿Deseas añadir alguna observación?',
        'ru':'?????? ???????? ?????-???? ????????'
    }[sess['lang']])

async def notify_staff(context: ContextTypes.DEFAULT_TYPE, data: dict):
    msg = (f"?? *New candidate via SafeJob!*\\n\\n"
           f"?? Name: {data.get('name')}\\n"
           f"?? Age: {data.get('age')}\\n"
           f"??? Nationality: {data.get('nationality')}\\n"
           f"?? Experience: {data.get('experience')}\\n"
           f"?? Languages: {data.get('languages')}\\n"
           f"?? Location: {data.get('location')}\\n"
           f"?? Fines: {data.get('fines')}\\n"
           f"?? Work visa: {data.get('work_visa')}\\n"
           f"?? Relocate: {data.get('relocate')}\\n"
           f"?? Need passport help: {data.get('need_passport_help')}\\n"
           f"?? Need police help: {data.get('need_police_help')}\\n"
           f"?? Notes: {data.get('notes')}")
    try:
        await context.bot.send_message(chat_id=config.ADMIN_GROUP_ID, text=msg, parse_mode='Markdown')
        if data.get('resume_path'):
            await context.bot.send_document(chat_id=config.ADMIN_GROUP_ID, document=open(data['resume_path'],'rb'))
        if data.get('video_path'):
            await context.bot.send_video(chat_id=config.ADMIN_GROUP_ID, video=open(data['video_path'],'rb'))
    except Exception as e:
        logger.exception("Failed to notify staff: %s", e)

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN", config.TELEGRAM_BOT_TOKEN)
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    print("Bot started...")
    app.run_polling()

