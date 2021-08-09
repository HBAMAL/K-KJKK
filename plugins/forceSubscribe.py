
import time
import logging
from config import Config
from pyrogram import Client, filters
from sql_helpers import forceSubscribe_sql as sql
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(lambda _, __, query: query.data == "onUnMuteRequest")
@Client.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    channel = chat_db.channel
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
          try:
            client.get_chat_member(channel, user_id)
            client.unban_chat_member(chat_id, user_id)
            if cb.message.reply_to_message.from_user.id == user_id:
              cb.message.delete()
          except UserNotParticipant:
            client.answer_callback_query(cb.id, text="⚠️ JOIN CHANNEL FIRST & PRESS UNMUTE BUTTON⚠️", show_alert=True)
      else:
        client.answer_callback_query(cb.id, text="IDK", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"⚠️ **{cb.from_user.mention} IS TRYING TO UNMUTE HIMSELF BUT I CAN'T UNUMUTE HIM BECAUSE I AM NOT ADMIN IN GROUP MAKE ME AS ADMIN**\n__AND TRY ONCE MORE...__")
        client.leave_chat(chat_id)
      else:
        client.answer_callback_query(cb.id, text="⚠️ JOIN CHANNEL FIRST ⚠️", show_alert=True)



@Client.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channel = chat_db.channel
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = message.reply_text(
              "HLO {} 👋🏻  **PLZ JOIN MY**  [CHANNEL](https://t.me/{})  **THEN PRESS UNMUTE BUTTON ** TO UNMUTE .".format(message.from_user.mention, channel, channel),
              disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton('🥳JOIN🥳', url="https://t.me/{input_str}"),
                    InlineKeyboardButton('🗣UNMUTE ME 🗣', callback_data="onUnMuteRequest")]]
                )
          )
          client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          sent_message.edit(" **😕MAKE ME AS ADMIN IN THIS GROUP**\n__THEN TRY ONCE MORE...__")
          client.leave_chat(chat_id)
      except ChatAdminRequired:
        client.send_message(chat_id, text=f"😕 **MAKE ME AS ADMIN IN UR CHANNEL @{channel}**\n__THEN TRY ONCE MORE__")
        client.leave_chat(chat_id)


@Client.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def fsub(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status is "creator" or user.user.id in Config.SUDO_USERS:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable"):
        sql.disapprove(chat_id)
        message.reply_text("🚫 **DONE DISABLED🚫**")
      elif input_str.lower() in ('clear'):
        sent_message = message.reply_text('**UNMUTING ...**')
        try:
          for chat_member in client.get_chat_members(message.chat.id, filter="restricted"):
            if chat_member.restricted_by.id == (client.get_me()).id:
                client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          sent_message.edit('✅ **DONE UNMUTED EVERYONE.**')
        except ChatAdminRequired:
          sent_message.edit('😕**MAKE ME AS ADMIN IN THIS GROUP**\n__THEN TRY ONCE MORE....__')
      else:
        try:
          client.get_chat_member(input_str, "me")
          sql.add_channel(chat_id, input_str)
          message.reply_text(f"✅ **DONE ENABLED **\n__FORCE SUBSCRIBE, NEW USERS AND ALL MEMBERS IN THIS CHAT MUST JOIN THIS [channel](https://t.me/{input_str}).__", disable_web_page_preview=True)
        except UserNotParticipant:
          message.reply_text(f"😕 **MAKE ME AS ADMIN IN UR CHANNEL**\n__ [channel](https://t.me/{input_str}). THEN TRY ONCEMORE..__", disable_web_page_preview=True)
        except (UsernameNotOccupied, PeerIdInvalid):
          message.reply_text(f"⚠️ **INVALID USERNAME⚠️")
        except Exception as err:
          message.reply_text(f"⚠️ **ERROR:** ```{err}``` ⚠️️")
    else:
      if sql.fs_settings(chat_id):
        message.reply_text(f"✅ **DONE NEW USERS AND ALL MEMBERS IN THIS CHAT **\n__MUST JOIN THIS [❤️CHANNEL❤️](https://t.me/{sql.fs_settings(chat_id).channel})__", disable_web_page_preview=True)
      else:
        message.reply_text("**🚫FORCE SUBSCRIBE IS DISABLED🚫**")
  else:
      message.reply_text("**HEY I ONLY DEALS WITH OWNER 😏**\n__....__")
