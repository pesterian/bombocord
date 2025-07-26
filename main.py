import func
from dotenv import load_dotenv
import os
import discord
import logging
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from config import Config

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix=Config.COMMAND_PREFIX, intents=intents, help_command=None)

# Initialize data
func.load_jamaican_dict()
func.load_admins()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def confirm_action(ctx, action: str, timeout: int = 15) -> bool:
    """Helper for confirming user actions"""
    await ctx.send(f"Are you sure you want to {action}? Reply with `yes` to confirm.")
    
    try:
        msg = await bot.wait_for(
            "message",
            check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
            timeout=timeout
        )
        return msg.content.lower() == "yes"
    except Exception:
        await ctx.send("No confirmation received. Action cancelled.")
        return False

@bot.command(aliases=["ja"])
async def jadd(ctx, key: str, *, value: str):
    if not func.is_admin(ctx.author.id):
        await ctx.send("Error: You are not an admin.")
        return
    
    if key in func.jamaican_dict:
        await ctx.send(f"Key `{key}` already exists! Use `*jr {key}` to delete it, `*je {key} [new_value]` to edit it, or choose a different key.")
        return
        
    func.jamaican_dict[key] = value
    func.save_jamaican_dict()
    await ctx.send(f"Added `{key}`: `{value}` to Jamaican dictionary.")

@bot.command(aliases=["jr", "jrm", "jremove"])
async def jrem(ctx, key: str):
    if not func.is_admin(ctx.author.id):
        await ctx.send("Error: You are not an admin.")
        return
    if key not in func.jamaican_dict:
        await ctx.send(f"Key `{key}` not found.")
        return
        
    if await confirm_action(ctx, f"remove `{key}`"):
        del func.jamaican_dict[key]
        func.save_jamaican_dict()
        await ctx.send(f"Removed `{key}` from Jamaican dictionary.")

@bot.command(aliases=["je", "jed"])
async def jedit(ctx, key: str, *, new_value: str):
    if not func.is_admin(ctx.author.id):
        await ctx.send("Error: You are not an admin.")
        return
    if key not in func.jamaican_dict:
        await ctx.send(f"Key `{key}` not found.")
        return
        
    if await confirm_action(ctx, f"edit `{key}`"):
        func.jamaican_dict[key] = new_value
        func.save_jamaican_dict()
        await ctx.send(f"Edited `{key}`: `{new_value}`.")

@bot.event
async def on_message(message):
    # Skip bot messages
    if message.author.bot:
        return
    
    # Process commands first
    await bot.process_commands(message)
    
    # Check for key lookup only if it's not a command and starts with *
    if (message.content.startswith("*") and 
        not message.content.startswith("*bombocord") and
        not message.content.startswith("*ja") and
        not message.content.startswith("*jr") and
        not message.content.startswith("*je") and
        not message.content.startswith("*roulette") and
        not message.content.startswith("*r ") and
        not message.content.startswith("*random") and
        not message.content.startswith("*help") and
        not message.content.startswith("*commands") and
        not message.content.startswith("*info")):
        
        key = message.content[1:].strip().lower()
        reply_text = func.get_jamaican_reply(key)
        
        if reply_text:
            try:
                if message.reference:
                    ref = await message.channel.fetch_message(message.reference.message_id)
                    await ref.reply(reply_text)
                else:
                    await message.channel.send(reply_text)
            except Exception as e:
                logging.error(f"Error replying with key lookup: {e}")

@bot.command(aliases=["commands", "info"])
async def help(ctx):
    """Show available commands and usage"""
    help_text = """
    **Bombocord Commands**
    `*bombocord [message]` - Translate message to Jamaican patois
    `*ja [key] [value]` - Add new Jamaican phrase (admin only)
    `*jr [key]` - Remove Jamaican phrase (admin only)
    `*je [key] [value]` - Edit existing phrase (admin only)
    `*list` - List all dictionary keys
    `*roulette` - Get a random Jamaican phrase
    `*[key]` - Access a custom copypasta
    """
    await ctx.send(help_text)

@bot.command(name="list")
async def list_keys(ctx):
    """List all dictionary keys"""
    if not func.jamaican_dict:
        await ctx.send("Dictionary is empty!")
        return
    
    keys = list(func.jamaican_dict.keys())
    keys_text = ", ".join(f"`{key}`" for key in keys)
    await ctx.send(f"{keys_text}")

@bot.command()
@cooldown(1, 15, BucketType.user)  # One use every 15 seconds per user
async def bombocord(ctx, *, message: str = None):
    """Translate text to Jamaican patois"""
    # If no message is provided, check if it's a reply
    if message is None and ctx.message.reference:
        try:
            ref = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            message = ref.content
        except Exception as e:
            logging.error(f"Error fetching replied message: {str(e)}")
            await ctx.send("Mi cyaan find di message yuh replying to, bredren!")
            return
    
    if not message:
        await ctx.send("Gimme sumting fi translate nuh, bredren!")
        return

    try:
        translation = func.translate_to_jamaican(ctx.author.id, message)
        await ctx.send(translation)
    except func.RateLimitException as e:
        await ctx.send(str(e))
    except Exception as e:
        logging.error(f"Translation error: {str(e)}")
        await ctx.send("Translation failed, bredren!")

@bot.command(aliases=["r", "random"])
@cooldown(1, 5, BucketType.user)  # One use every 5 seconds per user
async def roulette(ctx):
    """Get a random entry from the Jamaican dictionary"""
    result = func.get_random_jamaican()
    if not result:
        await ctx.send("Mi dictionary empty bredren!")
        return
        
    key, value = result
    
    # Log the selected roulette entry
    logging.info(f"Roulette selected key: '{key}'")
    
    # If it's a reply to a message, reply to that message
    if ctx.message.reference:
        try:
            ref = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            await ref.reply(f"{value}")
        except Exception as e:
            logging.error(f"Error replying to message: {str(e)}")
            await ctx.send(f"{value}")
    else:
        await ctx.send(f"{value}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Easy nuh bredren! Try again in {error.retry_after:.0f} seconds.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Yuh missing some tings dere, check the help command!")
    else:
        logging.error(f"Command error: {str(error)}")
        # Don't send error details to chat

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))