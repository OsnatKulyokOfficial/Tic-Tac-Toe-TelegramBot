import logging
from Game import Game
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    Updater,
    CallbackQueryHandler
)
import bot_settings
from end_game_messages 
import WIN_MESSAGES, TIE_MESSAGES, LOSS_MESSAGES
import random

WELCOME_TEXT = "⭕❌ Welcome to the UNBEATABLE Tic Tac Toe ❌⭕\nThis bot is a game of Tic Tac Toe that is designed " \
               "to be unbeatable. It uses advanced algorithms to analyze the game board and determine the optimal move " \
               "at every turn, ensuring that the bot always makes the best possible move and will never lose the game."

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    context.user_data['avatar'] = 0
    context.bot.send_message(chat_id=chat_id, text=WELCOME_TEXT)
    context.bot.send_message(chat_id=chat_id, text='Go to the menu to continue')


def new_game(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    game = create_game(context, update.message.message_id)
    avatar_index = context.user_data['avatar']
    context.bot.send_message(chat_id=chat_id, text="Take a head start, you wouldn't beat me anyway!")
    context.bot.send_message(chat_id=chat_id, text="Choose empty tile:", reply_markup=build_board(game, avatar_index))


def create_game(context, message_id):
    game = context.user_data.get(message_id)
    if not game:
        game = Game()
        context.user_data[message_id] = game
    return game


def build_board(game, avatar_index):
    buttons = [InlineKeyboardButton(emojis[avatar_index] if e == 'X' else bot_emojis[avatar_index] if e == 'O' else ' ',
                                    callback_data=i) for i, e in
               enumerate(game.board)]
    board = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
    return InlineKeyboardMarkup(board)


emojis = ['❌', '🧔‍♂', '🐷', '💀', '🐮', '💪']
bot_emojis = ['⭕', '👩', '🥓', '👻', '🍔', '🦾']


def choose_avatar(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    a_buttons = [InlineKeyboardButton(e, callback_data=f'{i}a') for i, e in enumerate(emojis)]
    a_board = [a_buttons[i:i + 3] for i in range(0, len(a_buttons), 3)]
    context.bot.send_message(chat_id=chat_id, text="Your avatar:", reply_markup=InlineKeyboardMarkup(a_board))


def callback_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data
    game = create_game(context, query.message.message_id)
    logger.info(f'{game=}')
    logger.info(f'button clicked {data=}')
    bot_response = game.turn(int(data))
    logger.info(f'button clicked {bot_response=}')
    avatar_index = context.user_data['avatar']
    reply_markup = build_board(game, avatar_index)
    context.bot.edit_message_reply_markup(chat_id=chat_id, message_id=query.message.message_id,
                                          reply_markup=reply_markup)
    if "O wins" in str(bot_response):
        context.bot.send_message(chat_id=chat_id, text=random.choice(LOSS_MESSAGES), disable_web_page_preview=True)
    elif bot_response == "Tie":
        context.bot.send_message(chat_id=chat_id, text=random.choice(TIE_MESSAGES), disable_web_page_preview=True)
    elif bot_response == "X wins":
        context.bot.send_message(chat_id=chat_id, text=random.choice(WIN_MESSAGES), disable_web_page_preview=True)


def avatar_callback_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data[0]
    context.user_data['avatar'] = int(data)
    context.bot.send_message(chat_id=chat_id, text='👍')


my_bot = Updater(token=bot_settings.BOT_TOKEN, use_context=True)
my_bot.dispatcher.add_handler(CommandHandler("start", start))
my_bot.dispatcher.add_handler(CommandHandler("new_game", new_game))
my_bot.dispatcher.add_handler(CommandHandler("choose_avatar", choose_avatar))
my_bot.dispatcher.add_handler(CallbackQueryHandler(callback_handler, pattern="[0-9]$"))
my_bot.dispatcher.add_handler(CallbackQueryHandler(avatar_callback_handler, pattern="[0-9]a"))

logger.info("* Start polling...")
my_bot.start_polling()  # Starts polling in a background thread.
my_bot.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
