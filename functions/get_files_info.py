import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    requested_path = os.path.join(working_directory, directory)

    absolute_working_dir = os.path.abspath(working_directory)
    absolute_requested_path = os.path.abspath(requested_path)

    if not absolute_requested_path.startswith(absolute_working_dir):
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(absolute_requested_path):
        return f'Error: "{directory}" is not a directory'

    try:

        item_names = os.listdir(absolute_requested_path)
        list = []
        for item in item_names:
            item_full_path = os.path.join(absolute_requested_path, item)
            size = os.path.getsize(item_full_path)
            is_dir = os.path.isdir(item_full_path)
            list.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(list)
         
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
name = "get_files_info",
description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "directory": types.Schema(
            type=types.Type.STRING,
            description=(
                "The directory to list files from, relative to the working directory. "
                "If not provided, lists files in the working directory itself."
            ),
        ),
    },
),
)


    








    
