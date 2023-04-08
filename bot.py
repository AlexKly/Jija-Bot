import random, logging, aiogram, datetime

from src.msg_analyzer import Analyzer
from src import BOT_CONFIGS, DATA_INFO, DIR_AUDIO, DIR_IMAGES

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.getLogger('Logger is on.')

tg_bot = aiogram.Bot(token=BOT_CONFIGS['tg_bot_token'])
tg_dp = aiogram.Dispatcher(bot=tg_bot)
analyzer = Analyzer()

msg_timers = {'timer_1': datetime.datetime.now(), 'timer_2': datetime.datetime.now()}


# Receive voice message:
@tg_dp.message_handler(content_types=['text'], chat_type=aiogram.types.ChatType.SUPERGROUP)
async def handle_msg(message: aiogram.types.Message):
    """

    :param message:
    :return:
    """
    results = analyzer.analyze(msg=message.text)
    # Send recording:
    if results[0] != 'NORMAL' and results[0] != 'INSULT' and msg_timers['timer_1'] < datetime.datetime.now():
        fname = random.choice(seq=DATA_INFO['audio'][results[0]])
        with (DIR_AUDIO/fname).open('rb') as audio_f:
            await tg_bot.send_voice(chat_id=message.chat.id, voice=audio_f, reply_to_message_id=message.message_id)
        msg_timers['timer_1'] += datetime.timedelta(minutes=BOT_CONFIGS['audio_timeout'])
    # Send photo:
    if results[1][0] and msg_timers['timer_2'] < datetime.datetime.now():
        with (DIR_IMAGES/results[1][1][0]).open('rb') as img_f:
            await tg_bot.send_photo(
                chat_id=message.chat.id,
                photo=img_f,
                caption=results[1][1][1],
                reply_to_message_id=message.message_id
            )
        msg_timers['timer_2'] += datetime.timedelta(minutes=BOT_CONFIGS['image_timeout'])


if __name__ == '__main__':
    aiogram.executor.start_polling(tg_dp, skip_updates=True)
