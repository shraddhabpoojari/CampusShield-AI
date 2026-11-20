import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "campusshield-secret-key"
    )

    DEBUG = True

    APP_NAME = "CampusShield AI"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

