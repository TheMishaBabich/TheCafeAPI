from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
JWT_SECRET = os.getenv('JWT_SECRET')
CLIENT_ID_PAYMENT = os.getenv('CLIENT_ID_PAYMENT')
SECRET_PAYMENT = os.getenv('SECRET_PAYMENT')