import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:root@127.0.0.1:3306/aula_conectada"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
