## THIS BOT WILL NOT BE UPDATED ANY FURTHER
I re-wrote the bot from the ground up, check out https://github.com/pesterian/bombocord2

# Bombocord
This started off an an inside joke where we would translate copypastas into Jamaican. So I decided to write a discord bot that translates messages into Jamaican and stores copypastas as a joke but then it turned into a passion project of mine. This is the second version of the bot; the first version is now lost to history as I am ashamed of what I have done.

The following explanation is AI generated because I am very lazy.

## How It Works
- Uses Google's Gemini AI to translate text into Jamaican patois
- Stores custom copypastas in a JSON dictionary
- Commands prefixed with `*` for easy access - can be easily changed
- Features rate limiting and cooldowns to prevent abuse
- Supports reply-based translation of messages
- Includes admin commands for managing custom translations

### Key Features
- **Message translation** to Jamaican patois using AI
- **Custom copypasta** storage and retrieval system
- **Random Jamaican phrase** roulette feature
- **Admin controls** for dictionary management
- **Rate limiting** to prevent spam

### Commands
- `*bombocord [message]` - Translate text to Jamaican patois
- `*ja [key] [value]` - Add new Jamaican phrase (admin only)
- `*jr [key]` - Remove Jamaican phrase (admin only) 
- `*je [key] [value]` - Edit existing phrase (admin only)
- `*roulette` - Get a random Jamaican phrase
- `*[key]` - Access a custom copypasta by key
### Requirements
- Python 3.8+
- discord.py
- google-generativeai
- python-dotenv
- Discord bot token
- Google Gemini API key

### Setup
1. Clone this repository
2. Install dependencies: `pip install discord.py google-generativeai python-dotenv`
3. Create a `.env` file with:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   GOOGLE_API_KEY=your_gemini_api_key
   ```
4. Configure admin users in `admins.json`
5. Run with `python3 main.py`

### Files
- `main.py` - Main bot file with Discord commands
- `func.py` - Core functionality and AI integration
- `config.py` - Configuration settings
- `jamaican_dict.json` - Custom phrase dictionary
- `admins.json` - Admin user list
- `bombo.log` - Bot activity logs

