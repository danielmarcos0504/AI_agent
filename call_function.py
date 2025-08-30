from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
from config import WORKING_DIR


available_functions =[ 
    types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )
]

def call_function(function_call_part, verbose=False):

    function_name = function_call_part.name
    kwargs = dict(function_call_part.args or {})


    if verbose:
        print(f"Calling function: {function_name}({kwargs})")
    else:
        print(f" - Calling function: {function_name}")

    
    FUNCTIONS = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,


}

    if function_name not in FUNCTIONS:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )


    kwargs = dict(function_call_part.args or {})
    kwargs["working_directory"] = WORKING_DIR  # inject for all functions

    func = FUNCTIONS[function_name]
    function_result = func(**kwargs)
    



    if not isinstance(function_result, dict):
        function_result = {"result": function_result}



    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response=function_result,
            )
        ],
    )
