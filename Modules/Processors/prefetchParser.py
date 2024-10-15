import os
import requests
from zipfile import ZipFile 
import subprocess

def setup():
    # download if not exists and unzip https://f001.backblazeb2.com/file/EricZimmermanTools/net6/PECmd.zip
    if os.path.isfile(r".\Modules\tools\PECmd\PECmd.exe"):
        return()
    url = "https://f001.backblazeb2.com/file/EricZimmermanTools/net6/PECmd.zip"
    
    filename = "./Modules/PECmd.zip"

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
    # unzip to .\Modules\tools\AmcacheParser
    extract_path=r".\Modules\tools\PECmd"
    with ZipFile(filename, 'r') as zip_ref:
        for name in zip_ref.namelist():
            try:
                zip_ref.extract(name, extract_path)
            except Exception as e:
                print("failed to extract PECmd")
    os.remove(filename)

def execute(config):
    setup()
    extract_path=config["drive_path"]
    # check if module already runned on this machine output file is AppCompatCache.csv"
    if os.path.isfile(config["drive_path"]+"\\CSVs\\prefetch.csv"):
        return()
    try:
        # .\PECmd.exe -d "C:\Evidencies\Redline_stealer\SLT\LAPTOP_UH5L93SM\C\Windows\prefetch" --csv "./out" --csvf "prefetch.csv"
        subprocess.check_call([r".\Modules\tools\PECmd\PECmd.exe", "-d", extract_path+"\Windows\prefetch","--csv",extract_path+"\CSVs","--csvf","prefetch.csv"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    except Exception as e:
        print("Error on Prefetch tool"+str(e))

def get_dependencies():
    return([])

def get_outputs():
    return([("prefetch.csv","prefetch"),("prefetch_Timeline.csv","prefetch")])

def get_type():
    return("machine_module")

def get_name():
    return("PrefetchParser")

def get_machine_type():
    return("windows")

def get_description():
    return("Parses the prefetch files into a CSV file")