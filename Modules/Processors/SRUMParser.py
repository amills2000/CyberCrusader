import os
import requests
from zipfile import ZipFile 
import subprocess

def setup():
    # download if not exists and unzip https://f001.backblazeb2.com/file/EricZimmermanTools/net6/SrumECmd.zip
    if os.path.isfile(r".\\Modules\\tools\\SrumECmd\\SrumECmd.exe"):
        return()
    url = "https://f001.backblazeb2.com/file/EricZimmermanTools/net6/SrumECmd.zip"
    
    filename = "./Modules/SrumECmd.zip"

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
    # unzip to .\\Modules\\tools\\AmcacheParser
    extract_path=r".\\Modules\\tools\\SrumECmd"
    with ZipFile(filename, 'r') as zip_ref:
        for name in zip_ref.namelist():
            try:
                zip_ref.extract(name, extract_path)
            except Exception as e:
                print("failed to extract SrumECmd")
    os.remove(filename)

def execute(config):
    setup()
    extract_path=config["drive_path"]
    path=config["drive_path"]+"\\CSVs\\"
    # check if module already runned on this machine output file is AppCompatCache.csv"
    if os.path.isfile(config["drive_path"]+"\\CSVs\\SrumECmd_AppResourceUseInfo.csv"):
        return()
    try:
        subprocess.check_call([r".\\Modules\\tools\\SrumECmd\\SrumECmd.exe", "-f", extract_path+"\\C\\Windows\\System32\\SRU\\SRUDB.dat","-r", extract_path+"\\C\\Windows\\System32\\config\\SOFTWARE","--csv",extract_path+"\CSVs"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        file_list = os.listdir(path)
        # Specify the pattern to match and the new file name
        pattern_to_match = "SrumECmd"
        for filename in file_list:
            if pattern_to_match in filename:
                old_file_path = os.path.join(path, filename)
                new_file_path = os.path.join(path, "_".join(filename.split("_")[1:-1]+".csv"))
                os.rename(old_file_path, new_file_path)
    except Exception as e:
        print("Error on AmcacheParser tool"+str(e))

def get_dependencies():
    return([])

def get_outputs():
    return(["SrumECmd_AppResourceUseInfo.csv"])

def get_type():
    return("machine_module")

def get_name():
    return("SRUMParser")

def get_machine_type():
    return("windows")

def get_description():
    return("Parses the SRUM DB into a CSV file")