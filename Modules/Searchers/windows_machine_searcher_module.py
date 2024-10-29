import subprocess
import os
import json

def execute(config):
    #get iris info from configs.json
    try:
        file1 = open(".\\configs.json", "r")
    except:
        raise Exception("Could not open configs.json file!")
    configs=file1.read()
    file1.close()
    configs=json.loads(configs)
    print(configs)
    path=config["path"]
    #recurivelly iterate directories and detect all Machine paths, where a machine path is a directory that contains a $MFT file and return all in an array of tuples containing the machine name, the type and the path extract the name from the path where is not the drive leter
    machines=[]
    for root, dirs, files in os.walk(path):
        for file in files:
            if file=="$MFT":
                machine_path=root
                machine_name=machine_path.split("\\")[-2]
                if configs["avoidVss"]=="true" and machine_path.split("\\")[-1].startswith("VSS"):
                    continue
                machines.append((machine_name,machine_path))
    return(machines)
    
def get_dependencies():
    return(["triage_path"])

def get_outputs():
    return(["machine"])

def get_type():
    return("machine_finders")

def get_name():
    return("windows_machine_searcher")

def get_machine_type():
    return("windows")

def get_description():
    return("Searches for windows machines in a triage path by looking for $MFT files (Extracted with tools like kape or CYLR)")