import os 
from google.genai import types


def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000
    full_path = os.path.join(working_directory, file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(full_path)
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    file = os.path.isfile(full_path)

    if not file:
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(full_path, "r") as f:
            file_content = f.read(MAX_CHARS + 1) 
    except Exception as e:
        return f"Error: {str(e)}"
    if len(file_content) > MAX_CHARS:
        file_content = file_content[:MAX_CHARS]  
        file_content += f'[...File "{file_path}" truncated at 10000 characters]'
        
    return file_content

schema_get_file_content = types.FunctionDeclaration(
name = "get_file_content",
description=" Read file contents.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description= (" The file_path permit us to read file contents in the working directory"),
        ),
    },
    required=["file_path"]
),
)


