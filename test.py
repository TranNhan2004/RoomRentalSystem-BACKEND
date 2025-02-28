import secrets

# Tạo khóa AES 256-bit (32 byte)
def generate_aes_key(bytes):
    key = secrets.token_bytes(bytes)  
    key_hex = key.hex()  # Chuyển đổi khóa thành chuỗi hexadecimal
    return key_hex

# In ra khóa
if __name__ == "__main__":
    bytes = 32
    key = generate_aes_key(bytes) # 32 byte = 256-bit
    print(f"Your AES key ({bytes * 8}-bit): {key[:-10]}-{len(key[:-10])}")

# import dotenv
# import os

# dotenv.load_dotenv('.env.development')

# print(os.getenv('DEBUG'))
# print(bool(os.getenv('DEBUG')))