import subprocess
import requests
import urllib
import os
from zipfile import ZipFile 
import sys 

def setup():
    #check if mft.exe is in the tools folder, if not download it
    if os.path.isfile(r".\Modules\tools\hayabusa\hayabusa.exe"):
        return()
    # GitHub repository information
    repo_owner = "Yamato-Security"
    repo_name = "hayabusa"
    target_filename = "hayabusa-3.1.0-win-x64.zip"  # Filename of the asset you want to download

    # Make a request to the GitHub API to get the latest release information
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(api_url)
    release_data = response.json()

    # Find the asset URL for the target filename
    asset_url = None
    final_file_name=""
    for asset in release_data['assets']:
        if asset['name'].endswith(target_filename):
            asset_url = asset['browser_download_url']
            final_file_name=asset['name']
            break

    # Check if the target asset was found
    if asset_url is None:
        print(f"No asset ending with the filename '{target_filename}' found in the latest release.")
    else:
        # Extract the filename from the asset URL
        filename = r".\Modules\tools\\"+target_filename

        # Download the asset
        response = requests.get(asset_url)
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"'{filename}' downloaded successfully.")
        extract_path=r".\Modules\tools\hayabusa"
        with ZipFile(filename, 'r') as zip_ref:
            for name in zip_ref.namelist():
                try:
                    zip_ref.extract(name, extract_path)
                except Exception as e:
                    print("failed to extract tool")
        os.remove(filename)
        #rename chainsaw_x86_64-pc-windows-msvc.exe to chainsaw.exe
        os.rename(f".\\Modules\\tools\\hayabusa\\hayabusa-3.1.0-win-x64.exe",r".\Modules\tools\hayabusa\hayabusa.exe")
def execute(config):
    setup()
    # check if module already runned on this machine
    if os.path.isfile(config["drive_path"]+"\\CSVs\\hayabusa.csv"):
        return()
    
    extract_path=config["drive_path"]
    res = subprocess.Popen([r".\Modules\tools\hayabusa\hayabusa.exe", "csv-timeline","--directory",extract_path+"\\Windows\\System32\\winevt\\Logs","-s","-X","--no-wizard","-m","medium","--profile","all-field-info-verbose","-o",extract_path+"\\CSVs\\hayabusa.csv"],stdout=sys.stdout,stderr=sys.stderr).communicate()
    res = subprocess.Popen([r".\Modules\tools\hayabusa\hayabusa.exe", "logon-summary","--directory",extract_path+"\\Windows\\System32\\winevt\\Logs","-o",extract_path+"\\CSVs\\logon-summary.csv"],stdout=sys.stdout,stderr=sys.stderr).communicate()
    res = subprocess.Popen([r".\Modules\tools\hayabusa\hayabusa.exe", "extract-base64","--directory",extract_path+"\\Windows\\System32\\winevt\\Logs","-o",extract_path+"\\CSVs\\extract-base64.csv"],stdout=sys.stdout,stderr=sys.stderr).communicate()

def get_dependencies():
    return([])

def get_outputs():
    return(["hayabusa.csv"])

def get_type():
    return("machine_module")

def get_name():
    return("hayabusa")

def get_machine_type():
    return("windows")

def get_description():
    return("Executes the hayabusa tool to use Sigma rules on the machine")