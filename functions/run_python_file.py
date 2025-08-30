import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):

    safe_workdir = os.path.realpath(working_directory)
    safe_target = os.path.realpath(os.path.join(working_directory, file_path))

    inside = (safe_target == safe_workdir) or safe_target.startswith(safe_workdir + os.sep)
    if not inside:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'


    exist = os.path.exists(file_path)
    if not exist:
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith("py"):
        return f'Error: "{file_path}" is not a Python file.'

    output_message = ""
    try:
        command_list = ["python", file_path]
        final_list = command_list + args
        result = subprocess.run(final_list, timeout = 30, capture_output=True, cwd = safe_workdir
        )
        decoded_stdout = result.stdout.decode('utf-8')
        decoded_stderr = result.stderr.decode('utf-8')

        if decoded_stdout:
            output_message += "STDOUT:" + decoded_stdout
        if decoded_stderr:
            output_message += "STDERR:" + decoded_stderr
        if result.returncode != 0:
            output_message += f"Process exited with code {result.returncode}"

    except Exception as e:
        return f"Error: executing Python file: {e}"

    if output_message == "":
        return "No output produced."
    else:
        return output_message

schema_run_python_file = types.FunctionDeclaration(
name = "run_python_file",
description="Execute Python files with optional arguments",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
        type=types.Type.STRING,
        description="Execute python in the file_path of the working directory",
        ),
        "args": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(
                type=types.Type.STRING,
            ),
            description= ("We execute python files with diferents and optionals arguments of args"),
        ),
    },
    required=["file_path"]
),
)



