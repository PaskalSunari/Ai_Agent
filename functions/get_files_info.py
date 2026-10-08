import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)

        target_dir = os.path.normpath(
            os.path.join(abs_working_dir, directory)
        )

        valid_target_dir = (
            os.path.commonpath([abs_working_dir, target_dir])
            == abs_working_dir
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        result = ""

        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)

            file_size = os.path.getsize(item_path)
            is_directory = os.path.isdir(item_path)

            result += (
                f"- {item}: file_size={file_size} bytes, "
                f"is_dir={is_directory}\n"
            )

        return result

    except Exception as e:
        return f"Error: {e}"