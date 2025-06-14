import os


def get_files_info(working_directory, directory=None):
    """
    Get information about files and directories within a working directory.
    
    Args:
        working_directory (str): The base directory that limits where we can look
        directory (str): The specific directory to list (relative to working_directory)
        
    Returns:
        str: Formatted string with file information or error message
    """
    try:
        # Convert working_directory to absolute path for security checks
        working_dir_abs = os.path.abspath(working_directory)
        
        # If no directory specified, use the working directory itself
        if directory is None:
            target_directory = working_dir_abs
        else:
            # Join the working directory with the requested directory
            target_directory = os.path.abspath(os.path.join(working_directory, directory))
        
        # Security check: ensure target directory is within working directory
        if not target_directory.startswith(working_dir_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check if the target path exists and is a directory
        if not os.path.exists(target_directory):
            return f'Error: "{directory}" does not exist'
        
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'
        
        # Get directory contents
        try:
            contents = os.listdir(target_directory)
        except PermissionError:
            return f'Error: Permission denied to access "{directory}"'
        except OSError as e:
            return f'Error: Unable to access "{directory}": {str(e)}'
        
        # Sort contents for consistent output
        contents.sort()
        
        # Build the formatted string
        result_lines = []
        for item in contents:
            item_path = os.path.join(target_directory, item)
            
            try:
                # Check if it's a directory
                is_directory = os.path.isdir(item_path)
                
                # Get file size
                if is_directory:
                    # For directories, we can't get a meaningful size easily
                    # So we'll use a placeholder or calculated size
                    try:
                        file_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                                      for dirpath, dirnames, filenames in os.walk(item_path)
                                      for filename in filenames)
                    except (OSError, PermissionError):
                        file_size = 0
                else:
                    file_size = os.path.getsize(item_path)
                
                # Format the line
                result_lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_directory}")
                
            except (OSError, PermissionError) as e:
                # If we can't get info about this specific item, include error info
                result_lines.append(f"- {item}: Error getting info: {str(e)}")
        
        # Join all lines with newlines
        if result_lines:
            return "\n".join(result_lines)
        else:
            return "Directory is empty"
            
    except Exception as e:
        return f"Error: Unexpected error occurred: {str(e)}"
