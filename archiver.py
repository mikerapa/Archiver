import os
import fnmatch
import zipfile


class Archiver:
    def locate_files(self, folder_path: str, include_pattern: str = "*", exclude_pattern: str = None) -> list[str]:
        file_list = []
        if include_pattern == "":
            include_pattern = "*"
        for root, dirs, files in os.walk(folder_path):
            for filename in fnmatch.filter(files, include_pattern):
                if exclude_pattern and fnmatch.fnmatch(filename, exclude_pattern):
                    continue
                file_list.append(os.path.join(root, filename))
        return file_list

    def zip_files(self, file_paths, output_path):
        with zipfile.ZipFile(output_path, 'w') as zip_file:
            for file_path in file_paths:
                zip_file.write(file_path, os.path.basename(file_path))

    def archive(self, folder_path, output_path: str, include_pattern: str, exclude_pattern):
        files = self.locate_files(folder_path, include_pattern, exclude_pattern)
        self.zip_files(files, output_path)
