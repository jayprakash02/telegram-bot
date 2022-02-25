from telegram import Update
from telegram.ext import  CallbackContext
from .settings import CHANNEL_ID

def start(update: Update, context: CallbackContext) -> None:
    text='Chaliye Suru krte h'
    context.bot.send_message(CHANNEL_ID, text=text)

def message(update: Update, context: CallbackContext) -> None:
    
    try:
        # args[0] should contain the time for the timer in seconds
        t_type=context.args[0]
        t_chain=context.args[1]
        t_strike=context.args[2]
        t_sl=context.args[3]
        text='Entry at \n {0} {1} \n CMP: {2}Point \n SL: {3}Point'.format(t_type,t_chain,t_strike,t_sl)
        update.message.reply_text(text)
        context.bot.send_message(CHANNEL_ID, text=text)

    except (IndexError, ValueError):
        update.message.reply_text('kuch to gadbad h')