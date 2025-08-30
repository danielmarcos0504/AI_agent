import os 
from google.genai import types






def write_file(working_directory, file_path, content):

    safe_workdir = os.path.realpath(working_directory)
    safe_target = os.path.realpath(os.path.join(working_directory, file_path))


    inside = (safe_target == safe_workdir) or safe_target.startswith(safe_workdir + os.sep)
    if not inside:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    parent_dir = os.path.dirname(safe_target)

    os.makedirs(parent_dir, exist_ok=True)

    try:

        with open(safe_target, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'



schema_write_file = types.FunctionDeclaration(
name = "write_file",
description="Write or overwrite files",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
        type=types.Type.STRING,
        description="We write an overwrite the file in file_path of the working directory",
        ),
        "content": types.Schema(
            type=types.Type.STRING,
            
            description= "Content to write the file",
        ),
    },
    required=["file_path", "content"]
),
)
