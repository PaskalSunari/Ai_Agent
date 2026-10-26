import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if file_path is outside the working_directory
        try:
            common = os.path.commonpath([abs_working_dir, absolute_file_path])
            if common != abs_working_dir:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        except ValueError:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if file exists and is a regular file
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Check if file ends with .py
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build command list
        command = ["python", absolute_file_path]
        if args:
            command.extend(args)

        # Run via subprocess with required arguments
        result = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Build output string based on CompletedProcess object
        output_parts = []
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"