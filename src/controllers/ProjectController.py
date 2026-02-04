from .BaseController import BaseController, BASE_DIR
from fastapi import UploadFile
from models import ResponseSignal # The easy way by configuring `__init__.py` to directly import ResponseSignal from models
import os


class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id: str):
        project_dir = os.path.join(
            self.files_dir,
            project_id
        )
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        return project_dir
    
