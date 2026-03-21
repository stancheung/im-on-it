import os
from google.genai import types
from config import MAX_CHAR

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get content of the specified file inside the working directory up to 10000 maximum characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the file that should be read, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHAR)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHAR} characters]'
                )
        return content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'

