
import sys
import zipfile_deflate64 as zipfile
import os
import os.path
import getopt
import concurrent.futures
import logging
import requests
import subprocess

def setup():
    #check if mft.exe is in the tools folder, if not download it
    if os.path.isfile(r".\Modules\tools\7zip\7z.exe"):
        return()
    print("Downloading 7zip and add the binary 7z.exe to the tools folder (./modules/tools/7zip/7z.exe)")

def execute(path):
    setup()
    print("Extracting "+path)
    extract_path=os.path.join(path.split(".")[0])
    if os.path.isdir(extract_path):
        return(extract_path)
    #extract using the .\Modules\tools\7zip\7zr.exe
    res = subprocess.Popen([r".\Modules\tools\7zip\7z.exe", "x", path, f"-o{extract_path}","-tzip"],stdout=sys.stdout,stderr=subprocess.DEVNULL).communicate()
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