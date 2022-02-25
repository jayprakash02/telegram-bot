
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
# Best practice would be to replace context with an underscore,
# since context is an unused local variable.
# This being an example and not having context present confusing beginners,
# we decided to have it present as context.
def start(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    update.message.reply_text('Hi! Use /set <seconds> to set a timer')



def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context, text='Beep!')


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    g_id='@testtrader00000'
    try:
        # args[0] should contain the time for the timer in seconds
        t_type=context.args[0]
        t_chain=context.args[1]
        t_strike=context.args[2]
        t_sl=context.args[3]
        text='Entry at \n {0} {1} \n CMP: {2}Point \n SL: {3}Point'.format(t_type,t_chain,t_strike,t_sl)
        # due = int(context.args[0])
        # if due < 0:
        #     update.message.reply_text('Sorry we can not go back to future!')
        #     return

        # job_removed = remove_job_if_exists(str(chat_id), context)
        # context.job_queue.run_once(alarm, due, context=chat_id, name=str(chat_id))

        # text = 'Timer successfully set!'
        # if job_removed:
        #     text += ' Old one was removed.'
        update.message.reply_text(text)
        context.bot.send_message(g_id, text=text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)


def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5175692754:AAGsTSgOuRjDyuRhr4Lm0MateK1tWsL3XbY")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("set", set_timer))
    dispatcher.add_handler(CommandHandler("unset", unset))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
