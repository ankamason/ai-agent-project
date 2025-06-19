import os
import subprocess
from google.genai import types
from functions.get_files_info import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file

# Working directory as specified in assignment
WORKING_DIR = "./calculator"

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

# Basic function implementations
def get_files_info(directory=".", working_directory="./calculator"):
    try:
        target_dir = os.path.join(working_directory, directory) if directory != "." else working_directory
        files = os.listdir(target_dir)
        return "\n".join(files)
    except Exception as e:
        return f"Error: {str(e)}"

def get_file_content(file_path, encoding="utf-8", working_directory="./calculator"):
    try:
        full_path = os.path.join(working_directory, file_path)
        with open(full_path, 'r', encoding=encoding) as file:
            return file.read()
    except Exception as e:
        return f"Error: {str(e)}"

def run_python_file(file_path, arguments=None, working_directory="./calculator"):
    try:
        cmd = ["python3", file_path]
        if arguments:
            cmd.extend(arguments)
        
        result = subprocess.run(
            cmd,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            if output:
                output += result.stderr
            else:
                output = result.stderr
        
        return output.strip() if output else f"Script executed successfully (no output)"
        
    except Exception as e:
        return f"Error: {str(e)}"

def write_file(file_path, content, mode="write", encoding="utf-8", working_directory="./calculator"):
    try:
        full_path = os.path.join(working_directory, file_path)
        write_mode = "w" if mode == "write" else "a"
        
        with open(full_path, write_mode, encoding=encoding) as file:
            file.write(content)
        
        return f"File written: {file_path}"
        
    except Exception as e:
        return f"Error: {str(e)}"

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f" - Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    function_name = function_call_part.name
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR
    function_result = function_map[function_name](**args)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
