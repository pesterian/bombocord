# Bombocord
This started off an an inside joke where we would translate copypastas into Jamaican. So I decided to write a discord bot that translates messages into Jamaican and stores copypastas as a joke but then it turned into a passion project of mine. This is the second version of the bot; the first version is now lost to history as I am ashamed of what I have done.

The following explanation is AI generated because I am very lazy.

## How It Works
- Uses Google's Gemini AI to translate text into Jamaican patois
- Stores custom Jamaican translations in a JSON dictionary
- Commands prefixed with `*` for easy access
- Features rate limiting and cooldowns to prevent abuse
- Supports reply-based translation of messages
- Includes admin commands for managing custom translations

### Key Features
- Message translation to Jamaican patois
- Custom copypasta storage and retrieval
- Random Jamaican phrase roulette
- Admin controls for dictionary management

### Requirements
- Python 3.8+
- discord.py
- google-generativeai
- python-dotenv
- Discord bot token
- Google Gemini API
