import os
import json
import logging
import functools
import random
import google.generativeai
from dotenv import load_dotenv
from datetime import datetime, timedelta
from config import Config

class BombocordException(Exception):
    """Base exception for Bombocord-specific errors"""
    pass

class RateLimitException(BombocordException):
    """Raised when a user hits rate limits"""
    pass

def rate_limit(func):
    """Decorator to check rate limits before executing a function"""
    @functools.wraps(func)
    def wrapper(user_id: int, *args, **kwargs):
        if check_rate_limit(user_id):
            raise RateLimitException("Yuh going too fast bredren!")
        return func(user_id, *args, **kwargs)
    return wrapper

# Setup logging
logging.basicConfig(
    filename=Config.LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables and initialize Gemini
load_dotenv()
google.generativeai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = google.generativeai.GenerativeModel("gemini-pro")

# Global state
jamaican_dict = {}
admin_users = {}
rate_limit_dict = {}

def check_rate_limit(user_id: int) -> bool:
    """Returns True if user is rate limited"""
    now = datetime.now()
    if user_id in rate_limit_dict:
        timestamps = rate_limit_dict[user_id]
        # Remove old timestamps
        timestamps = [ts for ts in timestamps if ts > now - timedelta(minutes=1)]
        if len(timestamps) >= Config.RATE_LIMIT:
            return True
        rate_limit_dict[user_id] = timestamps + [now]
    else:
        rate_limit_dict[user_id] = [now]
    return False

def load_file(filepath: str, default=None):
    """Generic JSON file loader with error handling"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading file {filepath}: {str(e)}")
        return default if default is not None else {}

def save_file(filepath: str, data):
    """Generic JSON file saver"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logging.info(f"Successfully saved file {filepath}")
    except Exception as e:
        logging.error(f"Error saving file {filepath}: {str(e)}")

def load_jamaican_dict():
    global jamaican_dict
    jamaican_dict = load_file(Config.JAMAICAN_DICT_PATH)
    logging.info("Jamaican dictionary loaded")
    
def save_jamaican_dict():
    save_file(Config.JAMAICAN_DICT_PATH, jamaican_dict)

def get_jamaican_reply(key: str):
    return jamaican_dict.get(key.lower())

def get_random_jamaican():
    """Returns a random entry from the Jamaican dictionary"""
    if not jamaican_dict:
        return None
    key = random.choice(list(jamaican_dict.keys()))
    return key, jamaican_dict[key]

def load_admins():
    global admin_users
    admin_users = load_file(Config.ADMIN_FILE_PATH)
    logging.info("Admin users loaded")

def is_admin(user_id: int) -> bool:
    return str(user_id) in admin_users

@rate_limit
def translate_to_jamaican(user_id: int, text: str) -> str:
    """Translate text to Jamaican patois using Gemini"""
    prompt = Config.TRANSLATION_PROMPT.format(text=text)
    try:
        response = gemini_model.generate_content(prompt).text
        logging.info("Translation generated successfully")
        return response
    except Exception as e:
        return handle_error(e, "Translation")

def handle_error(error: Exception, context: str = "Operation") -> str:
    """Common error handler for user-facing errors"""
    error_msg = f"{context} error: {str(error)}"
    logging.error(error_msg)
    return f"Yuh see mi bredren, I'm having some technical difficulties: {str(error)}"