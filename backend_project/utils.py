import uuid
import re
from typing import List
from datetime import date

VALID_FOLDER_NAME_REGEX = re.compile(r'^[a-zA-Z0-9-_]+$')  
VALID_FILE_NAME_REGEX = re.compile(r'^[a-zA-Z0-9-_\.]+$')  

def upload_to_fn(folders_path: List[str]=None, filename: str=None) -> str:

    if not folders_path:
        raise ValueError("Folders path for file upload cannot be empty.")
    
    if filename is None:
        raise ValueError("Filename for the uploaded file cannot be empty.")
    
    for folder in folders_path:
        if not VALID_FOLDER_NAME_REGEX.match(folder):
            raise ValueError(
                f"Invalid folder name: '{folder}'. It must only contain " +
                f"alphanumeric characters, hyphens, or underscores."
            )
    
    if not VALID_FILE_NAME_REGEX.match(filename):
        raise ValueError(
            f"Invalid filename: '{filename}'. It must only contain " + 
            f"alphanumeric characters, hyphens, underscores, and periods."
        )
    
    folders_str = '/'.join(folders_path)
    
    first_dot_char_idx = filename.find('.')
    
    filename_str = (f"{filename[:first_dot_char_idx]}" + 
                    f"-{date.today()}-{uuid.uuid4().hex[:16]}{filename[first_dot_char_idx:]}")
    
    return f'{folders_str}/{filename_str}'