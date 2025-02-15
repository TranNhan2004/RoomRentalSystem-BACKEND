import secrets

# Tạo một secret key dài 32 ký tự
# secret_key = secrets.token_urlsafe(64)
# print(secret_key)
# print(bool('True'))
# print(bool('false'))

import os
from dotenv import load_dotenv

load_dotenv('.env.development')
print(os.getenv('AUTH_COOKIE_SECURE') == 'True')