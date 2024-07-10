import sys
import os
import os.path
import subprocess

_7ZIP_PATH = "7zip\\7z.exe"
TOOLS_PATH = None

def setup():
    #check if mft.exe is in the tools folder, if not download it
    if os.path.isfile(os.path.join(TOOLS_PATH, _7ZIP_PATH)):
        return()
    print(f" * Downloading 7zip and add the binary 7z.exe to the tools folder.")

def execute(config):
    path=config["path"]
    global TOOLS_PATH
    TOOLS_PATH = config["tools_path"]
    setup()
    print(" * Extracting "+path)
    extract_path=os.path.join(path.split(".")[0])
    if os.path.isdir(extract_path):
        print(" * Already extracted, skipping")
        return(extract_path)
    if not os.path.exists(os.path.join(TOOLS_PATH, _7ZIP_PATH)):
        raise Exception("7zip not found in tools folder")
    res = subprocess.Popen([os.path.join(TOOLS_PATH, _7ZIP_PATH), "x", path, f"-o{extract_path}","-tzip"],stdout=sys.stdout,stderr=subprocess.DEVNULL).communicate()
    return(extract_path)

def get_dependencies():
    return([".zip"])

def get_outputs():
    return(["extracted"])

def get_type():
    return("extractor_module")

def get_name():
    return("zip_extractor")

def get_description():
    return("Extracts zip files")