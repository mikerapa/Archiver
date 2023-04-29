from rich.console import Console
from rich.text import Text
from settings import read_folder_config
from archiver import Archiver

if __name__ == '__main__':
    console = Console()
    archiver = Archiver()
    folder_configs = read_folder_config('folder_config.json')
    for folder_config in folder_configs:
        name_text = Text(f"{folder_config.name}", style="blue")
        console.print(name_text, end="")
        archiver.archive(folder_config.folder_path, output_path=folder_config.output_path,
                         include_pattern=folder_config.include_pattern,
                         exclude_pattern=folder_config.exclude_pattern)
        check_text = Text(" \u2713", style="green")
        console.print(check_text)
    console.print(Text("Done!", style="green"))
