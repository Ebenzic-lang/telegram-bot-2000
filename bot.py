from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import config

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{config.CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("🔓 I Joined (Unlock)", callback_data="check_join")]
    ]

    await update.message.reply_text(
        "Welcome 👋\n\nGet access to exclusive drops + winner alerts.\n\nStep 1/2: Join our channel to unlock.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# CHECK JOIN
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    member = await context.bot.get_chat_member(config.CHANNEL_USERNAME, user_id)

    if member.status in ['member', 'administrator', 'creator']:
        keyboard = [
            [InlineKeyboardButton("🎰 Play Now", url=config.PLAY_LINK)],
            [InlineKeyboardButton("🎁 Today’s Offer", url=config.OFFER_LINK)],
            [InlineKeyboardButton("💬 Support", url=config.SUPPORT_LINK)]
        ]

        await query.edit_message_text(
            "Unlocked 🎉\n\nStep 2/2: Continue below:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        keyboard = [
            [InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{config.CHANNEL_USERNAME.replace('@','')}")],
            [InlineKeyboardButton("🔓 Try Unlock Again", callback_data="check_join")]
        ]

        await query.answer("You must join first!", show_alert=True)

        await query.edit_message_text(
            "Not subscribed yet—join to unlock access.\n\n• Exclusive signals\n• Daily winners\n• VIP alerts",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# MAIN
def main():
    app = Application.builder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
