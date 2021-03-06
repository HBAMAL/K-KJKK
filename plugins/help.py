import logging
from config import Messages as tr
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.private & filters.incoming & filters.command(['start']))
def _start(client, message):
    client.send_message(message.chat.id,
        text=tr.START_MSG.format(message.from_user.first_name, message.from_user.id),
        parse_mode="markdown",
        disable_notification = True,
        reply_markup = InlineKeyboardMarkup(start(1)),
        reply_to_message_id=message.message_id
        )
    
@Client.on_message(filters.private & filters.incoming & filters.command(["about"]))
def _about_message(client, message):
    client.send_message(message.chat.id,
        text=tr.ABOUT_MSG,
        parse_mode="markdown",
        disable_notification = True,
        reply_markup = InlineKeyboardMarkup(about(1)),
        reply_to_message_id=message.message_id
        )


@Client.on_message(filters.private & filters.incoming & filters.command(['help']))
def _help(client, message):
    client.send_message(chat_id = message.chat.id,
        text = tr.HELP_MSG[1],
        parse_mode="markdown",
        disable_notification = True,
        reply_markup = InlineKeyboardMarkup(map(1)),
        reply_to_message_id = message.message_id
    )

help_callback_filter = filters.create(lambda _, __, query: query.data.startswith('help+'))

@Client.on_callback_query(help_callback_filter)
def help_answer(client, callback_query):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    msg = int(callback_query.data.split('+')[1])
    client.edit_message_text(chat_id=chat_id,    message_id=message_id,
        text=tr.HELP_MSG[msg],    reply_markup=InlineKeyboardMarkup(map(msg))
    )



def map(pos):
    if(pos==1):
        button = [
            [InlineKeyboardButton(text = '❤️CHANNNEL❤️', url="https://t.me/telsabots")],
            [InlineKeyboardButton(text = '🧑🏼‍💻DEV🧑🏼‍💻', url="https://t.me/alluaddict")],
        ]
    elif(pos==len(tr.HELP_MSG)-1):
        url = "https://github.com/DamienSoukara/FSub-Heroku"
        button = [
            [InlineKeyboardButton(text = '❤️CHANNNEL❤️', url="https://t.me/telsabots")],
            [InlineKeyboardButton(text = '🧑🏼‍💻DEV🧑🏼‍💻', url="https://t.me/alluaddict")],
        ]
    else:
        button = [
            [
                InlineKeyboardButton(text = '◀️', callback_data = f"help+{pos-1}"),
                InlineKeyboardButton(text = '▶️', callback_data = f"help+{pos+1}")
            ],
        ]
    return button

def about(pos):
    if(pos==3):
        button = [
            [InlineKeyboardButton(text = '❤️CHANNNEL❤️', url="https://t.me/telsabots")],
            [InlineKeyboardButton(text = '🧑🏼‍💻DEV🧑🏼‍💻', url="https://t.me/alluaddict")],
        ]
    elif(pos==len(tr.ABOUT_MSG)-1):
        url = "https://github.com/DamienSoukara/FSub-Heroku"
        button = [
           [InlineKeyboardButton(text = '❤️CHANNNEL❤️', url="https://t.me/telsabots")],
           [InlineKeyboardButton(text = '🧑🏼‍💻DEV🧑🏼‍💻', url="https://t.me/alluaddict")],
        ]
    else:
        button = [
            [
                [InlineKeyboardButton(text = '❤️CHANNNEL❤️', url="https://t.me/telsabots")],
                [InlineKeyboardButton(text = '🧑🏼‍💻DEV🧑🏼‍💻', url="https://t.me/alluaddict")]
            ],
        ]
    return button
            
def start(pos):
    if(pos==3):
        button = [
            [InlineKeyboardButton(text = '❤️CHANNNEL❤️', url="https://t.me/telsabots")],
            [InlineKeyboardButton(text = '🧑🏼‍💻DEV🧑🏼‍💻', url="https://t.me/alluaddict")],
            [InlineKeyboardButton(text = '◀️', callback_data = f"help+{pos-1}")],
        ]
    elif(pos==len(tr.START_MSG)-1):
        url = "https://github.com/DamienSoukara/FSub-Heroku"
        button = [
            [InlineKeyboardButton(text = '❤️CHANNNEL❤️', url="https://t.me/telsabots")],
            [InlineKeyboardButton(text = '🧑🏼‍💻DEV🧑🏼‍💻', url="https://t.me/alluaddict")]
        ]
    else:
        button = [
            [
                [InlineKeyboardButton(text = '❤️CHANNNEL❤️', url="https://t.me/telsabots")],
                [InlineKeyboardButton(text = '🧑🏼‍💻DEV🧑🏼‍💻', url="https://t.me/alluaddict")],
            ],
        ]
    return button
