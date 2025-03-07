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


import requests
from urllib.parse import quote
from unidecode import unidecode


def get_text_without_accents(text: str) -> str:
    return unidecode(text)

def get_lat_and_lng(address: str):
    API_KEY = ''
    
    encode_address = quote(get_text_without_accents(address))
    print(encode_address)
    
    response = requests.get(f"https://rsapi.goong.io/geocode?address={encode_address}&api_key={API_KEY}")
    
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Yêu cầu thất bại với mã lỗi: {response.status_code}")




def get_distance(lat_source, lng_source, lat_destination, lng_destination):
    API_KEY = '8E0DAHQ3tcoK7aawVavHxYtwnrdGrGA0RBcTto5S'
    
    response = requests.get(f"https://rsapi.goong.io/DistanceMatrix?origins={lat_source},{lng_source}" +
                            f"&destinations={lat_destination},{lng_destination}&vehicle=bike&api_key={API_KEY}")
    
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Yêu cầu thất bại với mã lỗi: {response.status_code}")

# get_lat_and_lng(address='Trường Đại học Cần Thơ, Đ. 3 Tháng 2, Phường Xuân Khánh, Quận Ninh Kiều, Thành phố Cần Thơ')

h233_lat = 10.044368255553708
h233_lng = 105.77174012117797
ctu_lat = 10.029553099000054
ctu_lng = 105.77107771100003

get_distance(h233_lat, h233_lng, ctu_lat, ctu_lng)