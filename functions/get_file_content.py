import os

def get_file_content(working_directory, file_path):
    """
    Safely read the contents of a file within a working directory.
    
    Args:
        working_directory: The directory to restrict file access to
        file_path: The path to the file to read (relative to working_directory)
    
    Returns:
        str: The file contents, or an error message if something went wrong
    """
    try:
        # Convert working directory to absolute path
        abs_working_dir = os.path.abspath(working_directory)
        
        # Join the working directory with the file path and resolve to absolute
        abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
        
        # Security check: Ensure the file is within the working directory
        if not abs_file_path.startswith(abs_working_dir + os.sep):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if the path exists and is a regular file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read the file content with a maximum character limit
        MAX_CHARS = 10000
        with open(abs_file_path, 'r', encoding='utf-8') as f:
            content = f.read(MAX_CHARS + 1)  # Read one extra to check if we need to truncate
        
        # Check if truncation is needed
        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS]
            content += f'\n[...File "{file_path}" truncated at 10000 characters]'
        
        return content
        
    except Exception as e:
        # Catch any unexpected errors and return them as error strings
        return f"Error: {str(e)}"
