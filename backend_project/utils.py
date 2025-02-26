import uuid
from datetime import date


def upload_to_fn(folder_path: str, filename: str, instance) -> str:    
    first_dot_char_idx = filename.find('.')
    
    filename_str = (f"{filename[:first_dot_char_idx]}" + 
                    f"{instance.id}" +
                    f"-{date.today()}-{uuid.uuid4().hex[:16]}" +
                    f"{filename[first_dot_char_idx:]}")
    
    return f'{folder_path}/{filename_str}'