import discord  # type: ignore
from discord.ext import commands  # type: ignore
from google import genai
import random
import sys
import csv

# Set up intents and bot instance
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Gemini Initialization
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if not GENAI_API_KEY:
    raise ValueError("GENAI_API_KEY environment variable not set.")
genai_client = genai.Client(api_key=GENAI_API_KEY)

# Your bot token
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN environment variable not set.")

# Admin user ID
ADMIN_USER_ID = 336106546847023104

# File paths
DICT_FILE_PATH = "jamaican_dict.txt"

# Load Jamaican dictionary from file
def load_jamaican_dict(file_path):
    jamaican_dict = {}
    try:
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    english, jamaican = map(str.strip, row)
                    jamaican_dict[english.lower()] = jamaican.strip('"')
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Make sure the file exists.")
    return jamaican_dict

# Save the dictionary to the file
def save_dict_to_file(file_path, dictionary):
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        for english, jamaican in dictionary.items():
            writer.writerow([english, f'"{jamaican}"'])

# Load dictionary
jamaican_dict = load_jamaican_dict(DICT_FILE_PATH)

@bot.event
async def on_ready():
    print(f"The bot is ready and logged in as {bot.user}")

@bot.command()
async def cmd(ctx, *, text: str = None):
    """Translate text using the dictionary, allowing multi-word/multi-line entries and checking for a single trigger word."""
    if ctx.message.reference:
        # Use the content of the replied message
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        text = ctx.message.content[len("!cmd "):].strip()
        if not text:
            await ctx.send("Please provide a valid command.")
            return
        words = text.split()
        if len(words) != 1:
            await ctx.send("Please use exactly one command!")
            return
        trigger_word = words[0].lower()
        translation = jamaican_dict.get(trigger_word, f"No translation found for '{trigger_word}'.")
        await replied_message.reply(f"{translation}", mention_author=False)
    else:
        if not text:
            await ctx.send("Please provide a valid command.")
            return
        words = text.split()
        if len(words) != 1:
            await ctx.send("Please use exactly one command!")
            return
        trigger_word = words[0].lower()
        translation = jamaican_dict.get(trigger_word, f"No translation found for '{trigger_word}'.")
        await ctx.send(f"{translation}")

@bot.command()
async def bombocord(ctx, *, text: str = None):
    """Translate text using Google Gemini AI."""
    if not text and ctx.message.reference:
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        text = replied_message.content
    if not text:
        await ctx.send("Please provide text or reply to a message for translation.")
        return
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Translate this to Jamaican Patois. In your response ONLY provide the translation. Here's the text: {text}",
        )
        await ctx.send(response.text)
    except Exception as e:
        await ctx.send(f"Mi sorry, mi cyaan do dat right now. Error: {e}")

@bot.command()
async def add_dict(ctx, english: str, *, jamaican: str):
    """Add a new entry to the Jamaican dictionary."""
    english = english.lower().strip()
    jamaican = jamaican.strip()
    if english in jamaican_dict:
        await ctx.send(f"The word '{english}' already exists as '{jamaican_dict[english]}'. Updating it.")
    jamaican_dict[english] = jamaican
    save_dict_to_file(DICT_FILE_PATH, jamaican_dict)
    await ctx.send(f"Added/Updated '{english}' as '{jamaican}'.")

@bot.command()
async def rm_dict(ctx, *, english: str):
    """Remove an entry from the Jamaican dictionary."""
    english = english.lower().strip()
    if english in jamaican_dict:
        del jamaican_dict[english]
        save_dict_to_file(DICT_FILE_PATH, jamaican_dict)
        await ctx.send(f"Removed '{english}' from the dictionary.")
    else:
        await ctx.send(f"The word '{english}' does not exist in the dictionary.")

async def generate_response(ctx, prompt: str, language: str):
    """Generate a response using Google GenAI."""
    username = ctx.message.author.name
    if ctx.message.reference:
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        replied_text = replied_message.content
        if prompt:
            prompt = f"{replied_text}\n{username} says: {prompt}"
        else:
            prompt = f"{username} says: {replied_text}"
    else:
        if prompt:
            prompt = f"{username} says: {prompt}"
        else:
            await ctx.send("Please provide a prompt or reply to a message.")
            return
    try:
        if language == "patois":
            response = genai_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"{prompt} (Respond in Jamaican Patois.)",
            )
        elif language == "english":
            response = genai_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"{prompt} (Respond in English.)",
            )
        await ctx.send(response.text)
    except Exception as e:
        await ctx.send(f"Mi sorry, mi cyaan do dat right now. \n Error: {e}" if language == "patois" else f"I'm sorry, I can't do that right now. \n Error: {e}")

@bot.command(name="talk")
async def talk(ctx, *, prompt: str = None):
    """Responds in Jamaican Patois using Google GenAI."""
    await generate_response(ctx, prompt, "patois")

@bot.command(name="entalk")
async def entalk(ctx, *, prompt: str = None):
    """Responds in English using Google GenAI."""
    await generate_response(ctx, prompt, "english")

@bot.command()
async def list(ctx):
    """List all English dictionary entries."""
    if not jamaican_dict:
        await ctx.send("The dictionary is currently empty.")
        return
    entries = "\n".join(jamaican_dict.keys())
    await ctx.send(f"**Dictionary Entries:**\n{entries}")

@bot.command()
async def bigup(ctx):
    """Display help for commands."""
    help_message = (
        "**Bot Commands:**\n"
        "- `!bombocord <text>`: Translate text into Jamaican Patois using Google Gemini AI.\n"
        "- `!cmd <text>`: Copypasta command. Returns text if valid command from the dictionary is given.\n"
        "- `!add_dict <command> <copypasta>`: Add a word to the dictionary.\n"
        "- `!rm_dict <command>`: Remove a word from the dictionary.\n"
        "- `Both dictionary commands require manual approval from the admin user.`\n"
        "- `!list`: List all dictionary entries.\n"
        "- `!talk <prompt>`: Respond in Jamaican Patois using Google GenAI.\n"
        "- `!entalk <prompt>`: Respond in English using Google GenAI."
    )
    await ctx.send(help_message)

@bot.command()
async def swear(ctx):
    """Increase the swear counter by 1."""
    file_path = "swear.txt"
    try:
        with open(file_path, "r") as file:
            count = int(file.read().strip())
    except (FileNotFoundError, ValueError):
        count = 0
    count += 1
    with open(file_path, "w") as file:
        file.write(str(count))
    await ctx.send(f"Swear added! Total swears: {count}")

@bot.command()
async def swearcount(ctx):
    """Display the current swear count."""
    file_path = "swear.txt"
    try:
        with open(file_path, "r") as file:
            count = int(file.read().strip())
    except (FileNotFoundError, ValueError):
        count = 0
    await ctx.send(f"The current swear count is: {count}")

@bot.command()
async def swearby(ctx, increment: int):
    """Increase the swear counter by a specified number."""
    file_path = "swear.txt"
    try:
        with open(file_path, "r") as file:
            count = int(file.read().strip())
    except (FileNotFoundError, ValueError):
        count = 0
    count += increment
    with open(file_path, "w") as file:
        file.write(str(count))
    await ctx.send(f"Swear count increased by {increment}! Total swears: {count}")


# Run the bot
bot.run(TOKEN)
