import subprocess
import requests
import os
from zipfile import ZipFile 
import sys

def setup():
    #check if mft.exe is in the tools folder, if not download it
    if os.path.isfile(r".\Modules\tools\chainsaw\chainsaw.exe"):
        return()
    # GitHub repository information
    repo_owner = "WithSecureLabs"
    repo_name = "chainsaw"
    target_filename = "chainsaw_all_platforms+rules+examples.zip"  # Filename of the asset you want to download

    # Make a request to the GitHub API to get the latest release information
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(api_url)
    release_data = response.json()

    # Find the asset URL for the target filename
    asset_url = None
    for asset in release_data['assets']:
        if asset['name'] == target_filename:
            asset_url = asset['browser_download_url']
            break

    # Check if the target asset was found
    if asset_url is None:
        print(f"No asset with the filename '{target_filename}' found in the latest release.")
    else:
        # Extract the filename from the asset URL
        filename = r".\Modules\tools\chainsaw.zip"

        # Download the asset
        response = requests.get(asset_url)
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"'{filename}' downloaded successfully.")
        extract_path=r".\Modules\tools"
        with ZipFile(filename, 'r') as zip_ref:
            for name in zip_ref.namelist():
                try:
                    zip_ref.extract(name, extract_path)
                except Exception as e:
                    print("failed to extract Chainsaw")
        os.remove(filename)
        #rename chainsaw_x86_64-pc-windows-msvc.exe to chainsaw.exe
        os.rename(r".\Modules\tools\chainsaw\chainsaw_x86_64-pc-windows-msvc.exe",r".\Modules\tools\chainsaw\chainsaw.exe")

def execute(config):
    setup()
    # check if module already runned on this machine
    if os.path.isfile(config["drive_path"]+"\\CSVs\\sigma.csv"):
        return()
    
    extract_path=config["drive_path"]
    res = subprocess.Popen([r".\Modules\tools\chainsaw\chainsaw.exe", "hunt", extract_path+"\Windows\System32\winevt\Logs","-s",".\Modules\\tools\chainsaw\sigma","--mapping", ".\Modules\\tools\chainsaw\mappings\sigma-event-logs-all.yml", "-r" , ".\Modules\\tools\chainsaw\\rules","--csv","--output",extract_path+"\CSVs","--skip-errors"],stdout=sys.stdout,stderr=sys.stderr).communicate()
def get_dependencies():
    return([])

def get_outputs():
    return([("sigma.csv","sigma"),("rdp_attacks.csv","rdp_attacks"),("lateral_movement.csv","lateral_movement"),("antivirus.csv","antivirus")])

def get_type():
    return("machine_module")

def get_name():
    return("chainsaw")

def get_machine_type():
    return("windows")

def get_description():
    return("Executes the Chainsaw tool to use Sigma rules on the machine")