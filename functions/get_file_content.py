import os
from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_target_file = (
            os.path.commonpath([abs_working_dir, target_file])
            == abs_working_dir
        )

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as file:
            content = file.read(MAX_CHARS)
            if file.read(1):
                content += (
                    f'[...File "{file_path}" truncated at '
                    f'{MAX_CHARS} characters]'
                )
            return content
    except Exception as e:
        return f"Error: {e}"