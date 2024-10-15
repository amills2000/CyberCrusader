import subprocess
import requests
import os
def setup():
    #check if mft.exe is in the tools folder, if not download it
    if os.path.isfile(r".\Modules\tools\mft.exe"):
        return()
    # GitHub repository information
    repo_owner = "makitos666"
    repo_name = "MFT_Fast_Transcoder"
    target_filename = "mft.exe"  # Filename of the asset you want to download

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
        filename = r".\Modules\tools\mft.exe"

        # Download the asset
        response = requests.get(asset_url)
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"'{filename}' downloaded successfully.")


def execute(config):
    setup()
    # check if module already runned on this machine
    if os.path.isfile(config["drive_path"]+"\\CSVs\\MFT.csv"):
        return()
    try:
        res = subprocess.Popen([r".\Modules\tools\mft.exe", "transcode", config["drive_path"]+"\\$MFT", config["drive_path"]+"\\CSVs\\MFT.csv"],stdout=subprocess.PIPE)
        out, err = res.communicate()
    except Exception as e:
        print("Error on MFT tool"+str(e)+"\n")

def get_dependencies():
    return([])

def get_outputs():
    return([("MFT.csv","MFT")])

def get_type():
    return("machine_module")

def get_name():
    return("mft_transcoder")

def get_machine_type():
    return("windows")

def get_description():
    return("Transcodes the MFT into a CSV file")
