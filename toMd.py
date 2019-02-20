#!/usr/bin/env python3

import os
import json
import cson
import shutil

# Paths to necessary directories
# My paths:
#   BOOSTNOTE
#   GIT
from paths import *

SOURCE = BOOSTNOTE
DEST = GIT

def cson_to_md():
    folder_names = get_folders()
    original_files = get_all_files()
    copy_files(original_files, folder_names)

    
def get_folders():
    # Retrieve folder names from boostnote.json and perform operations
    with open(SOURCE + "/boostnote.json") as boostnote:
        folders = json.load(boostnote)["folders"]
    return get_folder_names(folders)

def get_folder_names(folders):
    folder_names = {}
    for i in range(0, len(folders)):
        folder_names[folders[i]["key"]] = folders[i]["name"]
    return folder_names

def get_all_files():
    files_path = SOURCE + "/notes"
    files = [files_path + "/" + f for f in os.listdir(files_path) if os.path.isfile(files_path + "/" + f)]
    return files

def copy_files(files, folders):
    for file in files:
        details = get_file_dir_and_name(file)
        if details:
            folder_name = folders[details["folder"]]
            name = details["name"]
            content = details["content"]
            # replace forward slash in path name
            name = name.replace('/', '-')
            copy_and_rename_file(file, DEST + "/" + folder_name, name, content)

def get_file_dir_and_name(file):
    file = open(file, "r")
    notes = cson.load(file)
    if notes["type"] == "MARKDOWN_NOTE":
        directory = {"folder": notes["folder"], "name": notes["title"], "content": notes["content"]}
    else:
        directory = None
    file.close()
    return directory

def copy_and_rename_file(src, dest, name, content):
    if not os.path.isdir(dest):
        os.makedirs(dest)
    new_path = shutil.copy(src, dest)
    rewrite_file(new_path, content)
    new_name = os.path.split(new_path)[0] + '/' + name + ".md"
    os.rename(new_path, new_name)

def rewrite_file(file, content):
    file = open(file, "w")
    for line in content:
        file.write(line)
    file.close()

if __name__ == "__main__":
    cson_to_md()













