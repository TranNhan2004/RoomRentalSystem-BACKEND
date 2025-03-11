# import secrets

# # Tạo khóa AES 256-bit (32 byte)
# def generate_aes_key(bytes):
#     key = secrets.token_bytes(bytes)  
#     key_hex = key.hex()  # Chuyển đổi khóa thành chuỗi hexadecimal
#     return key_hex

# # In ra khóa
# if __name__ == "__main__":
#     bytes = 32
#     key = generate_aes_key(bytes) # 32 byte = 256-bit
#     print(f"Your AES key ({bytes * 8}-bit): {key}-{len(key[:-10])}")

# import dotenv
# import os

# dotenv.load_dotenv('.env.development')

# print(os.getenv('DEBUG'))
# print(bool(os.getenv('DEBUG')))

from backend_project.goong_api import get_coords, get_distance_value

# get_coords(address='Trường Đại học Cần Thơ, Đ. 3 Tháng 2, Phường Xuân Khánh, Quận Ninh Kiều, Thành phố Cần Thơ')

# h233_coords = (10.044368255553708, 105.77174012117797)
# ctu_coords = (10.029553099000054, 105.77107771100003)

# get_distance_value(h233_coords, ctu_coords)

