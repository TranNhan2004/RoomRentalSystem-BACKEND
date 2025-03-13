import uuid
import re
from datetime import date
from unidecode import unidecode
from django.utils.timezone import now

def upload_to_fn(folder_path: str, filename: str, instance) -> str:    
    first_dot_char_idx = filename.find('.')
    
    filename_str = (f"{filename[:first_dot_char_idx]}" + 
                    f"{instance.id}" +
                    f"-{date.today()}-{uuid.uuid4().hex[:16]}" +
                    f"{filename[first_dot_char_idx:]}")
    
    return f'{folder_path}/{filename_str}'


def get_text_without_accents(text: str) -> str:
    return unidecode(text)

def equals_address(old_address: str, new_address: str) -> bool:
    normalized_old = re.sub(r'\s+', '', get_text_without_accents(old_address)).lower()
    normalized_new = re.sub(r'\s+', '', get_text_without_accents(new_address)).lower()
    return normalized_old == normalized_new

def today():
    return now().date()

def date_time_now():
    return now()