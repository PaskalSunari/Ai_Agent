import os


def get_files_info(
    working_directory: str, directory: str = ".", task: str = ""
) -> str:
  try:
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))

    valid_target_dir = (
        os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
    )

    if not valid_target_dir:
      return (
          f'Error: Cannot list "{directory}" as it is outside the permitted'
          " working directory"
      )

    if not os.path.isdir(target_dir):
      return f'Error: "{directory}" is not a directory'

    # === ADDED FOR TRACKING AND LEARNING: Optional task context tracking ===
    result = f"Task: {task}\n" if task else ""

    for item in os.listdir(target_dir):
      item_path = os.path.join(target_dir, item)
      file_size = os.path.getsize(item_path)
      is_directory = os.path.isdir(item_path)

      result += (
          f"- {item}: file_size={file_size} bytes, is_dir={is_directory}\n"
      )

    return result

  except Exception as e:
    return f"Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": (
            "Lists files in a specified directory relative to the working"
            " directory, providing file size and directory status"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": (
                        "Directory path to list files from, relative to the"
                        " working directory (default is the working directory"
                        " itself)"
                    ),
                },
                # === ADDED FOR TRACKING AND LEARNING: Schema definition for the task parameter ===
                "task": {
                    "type": "string",
                    "description": (
                        "Optional context or description of the task requiring"
                        " this file listing"
                    ),
                },
            },
        },
    },
}