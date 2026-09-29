# LFH Medical Invitations Telegram Bot

This repository contains the clean, rebuilt version of the LFH Medical
personal invitation Telegram bot.

## Files

- `bot.py` — Telegram bot application.
- `LFH_FINAL_INVITATION_TEMPLATE.jpg` — the approved LFH invitation artwork.
- `requirements.txt` — Python dependencies.
- `README.txt` — setup and deployment instructions.
- `render.yaml` — optional Render configuration.

## Important

Keep `bot.py` and `LFH_FINAL_INVITATION_TEMPLATE.jpg` in the same
repository directory.

The bot does NOT contain the invitation image as a huge encoded string.
The image is loaded as a normal file. This avoids the previous
unterminated-string syntax errors.

## 1. Create the GitHub repository

Create a NEW repository and upload all files from this package.

The repository should contain:

    bot.py
    LFH_FINAL_INVITATION_TEMPLATE.jpg
    requirements.txt
    README.txt
    render.yaml

Do not paste the old bot.py over this version.

## 2. Render

Create a new Web Service on Render and connect the NEW GitHub repository.

Recommended settings:

Runtime:
    Python 3

Build Command:
    pip install -r requirements.txt

Start Command:
    python bot.py

The included `render.yaml` can also be used as a guide.

## 3. Environment variable

In Render, add:

    BOT_TOKEN = YOUR_TELEGRAM_BOT_TOKEN

Do not put the Telegram token inside bot.py or GitHub.

Render automatically provides `PORT` and `RENDER_EXTERNAL_URL`.

## 4. Deploy

After connecting the repository:

1. Save the environment variable.
2. Deploy the service.
3. Open the Render logs.
4. A successful startup should show:
       Starting LFH invitation bot
       Webhook: https://...
5. Open the Telegram bot and send `/start`.

## 5. Creating an invitation

Tap:

    Create Personal Invitation

Then enter a name, for example:

    Dr John Doe

The bot creates a personal copy of the approved LFH invitation.

## Troubleshooting

If Render reports:

    SyntaxError: unterminated string literal

make sure the repository contains THIS `bot.py`, not one of the old
large embedded-image versions.

If the bot says the template is missing, confirm that
`LFH_FINAL_INVITATION_TEMPLATE.jpg` is in the same directory as `bot.py`.

If Render starts but Telegram does not respond, check that `BOT_TOKEN`
is present and correct.
