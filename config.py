class Config:
    RATE_LIMIT = 5
    COMMAND_PREFIX = "*"
    JAMAICAN_DICT_PATH = "jamaican_dict.json"
    ADMIN_FILE_PATH = "admins.json"
    LOG_FILE = "bombo.log"
    
    TRANSLATION_PROMPT = (
        "Translate the following text to Jamaican patois. Keep the translation natural and "
        "authentic, using common Jamaican expressions and slang:\n\n"
        "Text: {text}\n\n"
        "Translation:"
    )
    
    @staticmethod
    def get_user_history_path(user_id: int) -> str:
        return f"{user_id}.json"
