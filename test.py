import secrets

# Tạo khóa AES 256-bit (32 byte)
def generate_aes_key():
    key = secrets.token_bytes(32)  # 32 byte = 256-bit
    key_hex = key.hex()  # Chuyển đổi khóa thành chuỗi hexadecimal
    return key_hex

# In ra khóa
if __name__ == "__main__":
    key = generate_aes_key()
    print(f"Your AES key (256-bit): {key}")
