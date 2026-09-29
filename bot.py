import os
import io
import logging

from PIL import Image, ImageDraw, ImageFont
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ["BOT_TOKEN"]
PORT = int(os.environ.get("PORT", "10000"))
PUBLIC_URL = os.environ.get("RENDER_EXTERNAL_URL", "").rstrip("/")
WEBHOOK_PATH = "telegram-webhook"

TEMPLATE = "LFH_FINAL_INVITATION_TEMPLATE.jpg"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


def get_font(size: int):
    candidates = [
        "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf",
    ]

    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


def make_invitation(guest: str):
    image = Image.open(TEMPLATE).convert("RGB")
    draw = ImageDraw.Draw(image)

    blue = (18, 63, 134)

    # The supplied artwork is 1024 x 1536.
    # Clear only the placeholder-name area.
    draw.rectangle((215, 490, 810, 550), fill="white")

    size = 42
    while size >= 26:
        font = get_font(size)
        bbox = draw.textbbox((0, 0), guest, font=font)
        width = bbox[2] - bbox[0]
        if width <= 760:
            break
        size -= 2

    bbox = draw.textbbox((0, 0), guest, font=font)
    width = bbox[2] - bbox[0]
    x = (image.width - width) / 2
    y = 493

    draw.text((x, y), guest, font=font, fill=blue)

    output = io.BytesIO()
    output.name = "LFH_Medical_Invitation.jpg"
    image.save(output, format="JPEG", quality=95, optimize=True)
    output.seek(0)
    return output


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            "💌 Create Personal Invitation",
            callback_data="create",
        )
    ]]

    await update.message.reply_text(
        "Welcome to LFH Medical Invitations.\n\n"
        "Tap the button below to create a personal invitation.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "create":
        context.user_data["awaiting_name"] = True
        await query.message.reply_text(
            "Please enter the guest's name exactly as you want it "
            "to appear on the invitation.\n\n"
            "Example: Dr John Doe"
        )


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_name"):
        await update.message.reply_text(
            "Tap “Create Personal Invitation” to begin."
        )
        return

    guest = update.message.text.strip()

    if len(guest) < 2 or len(guest) > 80:
        await update.message.reply_text(
            "Please enter a valid guest name (2–80 characters)."
        )
        return

    if not os.path.exists(TEMPLATE):
        await update.message.reply_text(
            "The LFH invitation template is missing from the bot server."
        )
        return

    context.user_data["awaiting_name"] = False

    try:
        invitation = make_invitation(guest)

        await update.message.reply_photo(
            photo=invitation,
            caption=(
                f"💌 Personal invitation for {guest}\n\n"
                "LFH Medical Launch & Community Health Camp\n\n"
                "We are pleased to invite you to the Launch and Grand "
                "Opening of LFH Medical.\n\n"
                "Then there will be a health camp under the theme:\n"
                "“Healthy Community, Healthy Nation.”\n\n"
                "Your presence will be of great honour!"
            ),
        )
    except Exception:
        logging.exception("Failed to create invitation")
        await update.message.reply_text(
            "Sorry, I could not create the invitation. Please try again."
        )


def main():
    if not PUBLIC_URL:
        raise RuntimeError(
            "RENDER_EXTERNAL_URL is missing. "
            "This bot is configured for a Render Web Service."
        )

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text)
    )

    webhook_url = f"{PUBLIC_URL}/{WEBHOOK_PATH}"

    logging.info("Starting LFH invitation bot")
    logging.info("Webhook: %s", webhook_url)

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=WEBHOOK_PATH,
        webhook_url=webhook_url,
        allowed_updates=Update.ALL_TYPES,
    )


if __name__ == "__main__":
    main()
