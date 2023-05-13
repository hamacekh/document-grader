import os

def get_filename_without_extension(path):
    base_name = os.path.basename(path)  # get the name of the file from the path
    file_name_without_extension, _ = os.path.splitext(base_name)  # split the base name into file name and extension
    return file_name_without_extension