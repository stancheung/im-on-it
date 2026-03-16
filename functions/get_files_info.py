import os

def get_files_info(working_directory, directory="."):
    # if not os.path.isdir(directory):
    #     return f'Error: "{directory}" is not a directory'
    rslt = ""
    if directory == ".":
        rslt += f"Result for current directory:\n"
    else:
        rslt += f"Result for '{directory}' directory:\n"

    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        rslt += f'Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
        return rslt;

    for entry in os.scandir(target_dir):
        try:
            basename = os.path.basename(entry)
            size = os.path.getsize(entry)
            is_dir = os.path.isdir(entry)
        except Exception as ex:
            rslt += f'Error: {ex}\n'
            return rslt;

        rslt += f'- {basename}: file_size={size} bytes, is_dir={is_dir}\n'

    return rslt;
