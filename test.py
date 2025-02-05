import secrets

# Tạo một secret key dài 32 ký tự
secret_key = secrets.token_urlsafe(64)
print(secret_key)
print(bool('True'))
