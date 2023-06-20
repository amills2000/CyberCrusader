import os
import requests
from zipfile import ZipFile 
import subprocess

def setup():
    # download if not exists and unzip https://f001.backblazeb2.com/file/EricZimmermanTools/net6/AppCompatCacheParser.zip
    if os.path.isfile(r".\Modules\tools\AppCompatCacheParser\AppCompatCacheParser.exe"):
        return()
    url = "https://f001.backblazeb2.com/file/EricZimmermanTools/net6/AppCompatCacheParser.zip"
    
    filename = "./Modules/AppCompatCacheParser.zip"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Open the file in binary mode and write the downloaded content
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"File '{filename}' downloaded successfully!")
    else:
        print("Failed to download the file.")
    # unzip to .\Modules\tools\AppCompatCacheParser
    extract_path=r".\Modules\tools\AppCompatCacheParser"
    with ZipFile(filename, 'r') as zip_ref:
        for name in zip_ref.namelist():
            try:
                zip_ref.extract(name, extract_path)
            except Exception as e:
                print("failed to extract Chainsaw")
    os.remove(filename)

def execute(config):
    setup()
    extract_path=config["drive_path"]
    # check if module already runned on this machine output file is AppCompatCache.csv"
    if os.path.isfile(config["drive_path"]+"\\CSVs\\AppCompatCache.csv"):
        return()
    try:
        subprocess.check_call([r".\Modules\tools\AppCompatCacheParser\AppCompatCacheParser.exe", "-f", extract_path+"\Windows\System32\config\SYSTEM","--csv",extract_path+"\CSVs","--csvf","AppCompatCache.csv"])
    except Exception as e:
        print("Error on AppCompatCacheParser tool"+str(e))

def get_dependencies():
    return([])

def get_outputs():
    return(["AppCompatCache.csv"])

def get_type():
    return("machine_module")

def get_name():
    return("AppCompatCache")

def get_machine_type():
    return("windows")