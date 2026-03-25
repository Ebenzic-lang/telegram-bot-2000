import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

bot = telebot.TeleBot(config.BOT_TOKEN)

# START COMMAND
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{config.CHANNEL_USERNAME.replace('@','')}")
    )
    markup.add(
        InlineKeyboardButton("🔓 I Joined (Unlock)", callback_data="check_join")
    )

    bot.send_message(
        message.chat.id,
        "Welcome 👋\n\nGet access to exclusive drops + winner alerts.\n\nStep 1/2: Join our channel to unlock.",
        reply_markup=markup
    )

# CHECK JOIN
@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join(call):
    user_id = call.from_user.id

    try:
        member = bot.get_chat_member(config.CHANNEL_USERNAME, user_id)

        if member.status in ['member', 'administrator', 'creator']:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🎰 Play Now", url=config.PLAY_LINK))
            markup.add(InlineKeyboardButton("🎁 Today’s Offer", url=config.OFFER_LINK))
            markup.add(InlineKeyboardButton("💬 Support", url=config.SUPPORT_LINK))

            bot.edit_message_text(
                "Unlocked 🎉\n\nStep 2/2: Continue below:",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=markup
            )
        else:
            raise Exception("Not joined")

    except:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{config.CHANNEL_USERNAME.replace('@','')}")
        )
        markup.add(
            InlineKeyboardButton("🔓 Try Unlock Again", callback_data="check_join")
        )

        bot.answer_callback_query(call.id, "You must join first!", show_alert=True)

        bot.edit_message_text(
            "Not subscribed yet—join to unlock access.\n\n• Exclusive signals\n• Daily winners\n• VIP alerts",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

print("Bot is running...")
bot.infinity_polling()
