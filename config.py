class Config:
    MAX_HISTORY_LINES = 100
    RATE_LIMIT = 5
    COMMAND_PREFIX = "*"
    JAMAICAN_DICT_PATH = "jamaican_dict.json"
    ADMIN_FILE_PATH = "admins.json"
    LOG_FILE = "bombo.log"
    
    # Bot persona and prompts
    BOT_PERSONA = (
        "You are Bombocord, a humorous Discord bot who speaks exclusively in Jamaican patois. "
        "Your main function is translating to Jamaican. "
        "You never shy away from making a joke at every opportunity. "
        "Take the conversation history into consideration where applicable."
    )
    
    TRANSLATION_PROMPT = (
        "Translate the following text to Jamaican patois. Keep the translation natural and "
        "authentic, using common Jamaican expressions and slang:\n\n"
        "Text: {text}\n\n"
        "Translation:"
    )
    
    @staticmethod
    def get_user_history_path(user_id: int) -> str:
        return f"{user_id}.json"
