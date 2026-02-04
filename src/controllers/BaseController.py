from helpers.config import Settings, get_settings
import random
import string

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(
            self.base_dir,
            "assets/files"
        )

    def generate_random_string(self, length: int =12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))