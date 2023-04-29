import json


class Settings:
    def __init__(self, settings_file):
        self.settings_file = settings_file
        try:
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = {}

    def get(self, name):
        return self.settings.get(name)

    def set(self, name, value):
        self.settings[name] = value
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)


from typing import List
from pydantic import BaseModel


class FolderConfig(BaseModel):
    name: str
    folder_path: str
    output_path: str
    include_pattern: str = ''
    exclude_pattern: str = ''


def read_folder_config(filename: str) -> List[FolderConfig]:
    with open(filename, 'r') as f:
        data = json.load(f)
        folder_configs = []
        for folder_name, folder_data in data.items():
            folder_data['name'] = folder_name
            folder_config = FolderConfig(**folder_data)
            folder_configs.append(folder_config)
        return folder_configs
