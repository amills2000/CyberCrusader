import subprocess
import os

def execute(config):
    path=config["path"]
    #recurivelly iterate directories and detect all Machine paths, where a machine path is a directory that contains at least 2 folders alled root and home
    machines=[]
    for root, dirs, files in os.walk(path):
        if "root" in dirs and "home" in dirs:
            machine_path=root
            try:
                #open /etc/HOSTNAME and extract the machine namew
                with open(machine_path+"\\etc\\hostname", "r") as f:
                    machine_name=f.read().strip()	
            except:
                machine_name=machine_path.split("\\")[-1]
            machines.append((machine_name,machine_path))
    return(machines)
def get_dependencies():
    return(["triage_path"])

def get_outputs():
    return(["machine"])

def get_type():
    return("machine_finders")

def get_name():
    return("linux_machine_searcher")

def get_machine_type():
    return("linux")

def get_description():
    return("Searches for linux machines in a triage path by looking for the home and root directories")