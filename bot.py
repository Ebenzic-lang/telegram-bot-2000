from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import config

# START COMMAND
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{config.CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("🔓 I Joined (Unlock)", callback_data="check_join")]
    ]

    update.message.reply_text(
        "Welcome 👋\n\nGet access to exclusive drops + winner alerts.\n\nStep 1/2: Join our channel to unlock.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# CHECK IF USER JOINED
def check_join(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    member = context.bot.get_chat_member(config.CHANNEL_USERNAME, user_id)

    if member.status in ['member', 'administrator', 'creator']:
        keyboard = [
            [InlineKeyboardButton("🎰 Play Now", url=config.PLAY_LINK)],
            [InlineKeyboardButton("🎁 Today’s Offer", url=config.OFFER_LINK)],
            [InlineKeyboardButton("💬 Support", url=config.SUPPORT_LINK)]
        ]

        query.edit_message_text(
            "Unlocked 🎉\n\nStep 2/2: Continue below:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        keyboard = [
            [InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{config.CHANNEL_USERNAME.replace('@','')}")],
            [InlineKeyboardButton("🔓 Try Unlock Again", callback_data="check_join")]
        ]

        query.answer("You must join first!", show_alert=True)

        query.edit_message_text(
            "Not subscribed yet—join to unlock access.\n\n• Exclusive signals\n• Daily winners\n• VIP alerts",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# MAIN FUNCTION
def main():
    updater = Updater(config.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
