class Config:
    RATE_LIMIT = 5
    COMMAND_PREFIX = "*"
    JAMAICAN_DICT_PATH = "jamaican_dict.json"
    ADMIN_FILE_PATH = "admins.json"
    LOG_FILE = "bombo.log"
    
    TRANSLATION_PROMPT = (
        "The following text should be translated into Jamaican Patois and your reply should ONLY include the translation and NOTHING else.\n\n"
        "Text: {text}\n\n"
    )
    
    @staticmethod
    def get_user_history_path(user_id: int) -> str:
        return f"{user_id}.json"
