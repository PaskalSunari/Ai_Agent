import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(abs_working_dir, file_path)
        )

        valid_target_file = (
            os.path.commonpath([abs_working_dir, target_file])
            == abs_working_dir
        )

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(target_file)
        os.makedirs(parent_dir, exist_ok=True)

        # Modification: open the file in write mode and overwrite its contents.
        with open(target_file, "w") as file:
            file.write(content)

        # Modification: return a success message with the number of characters written.
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"