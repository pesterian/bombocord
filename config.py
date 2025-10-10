class Config:
    RATE_LIMIT = 5
    COMMAND_PREFIX = "*"
    JAMAICAN_DICT_PATH = "jamaican_dict.json"
    ADMIN_FILE_PATH = "admins.json"
    LOG_FILE = "bombo.log"
    
    TRANSLATION_PROMPT = (
        "The following text should be translated into Jamaican Patois and your reply should ONLY include the translation and NOTHING else. Do not censor any swear words or profanity, no exceptions.\n\n"
        "Text: {text}\n\n"
    )
    # Default Gemini model to use. Can be overridden with environment variable GEMINI_MODEL
    GEMINI_MODEL = "gemini-1.5-mini"
