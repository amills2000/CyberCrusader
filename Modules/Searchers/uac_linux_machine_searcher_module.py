import subprocess
import os

def execute(path):
    #recurivelly iterate directories and detect all Machine paths, where a machine path is a directory that contains a $MFT file and return all in an array of tuples containing the machine name, the type and the path extract the name from the path where is not the drive leter
    machines=[]
    for root, dirs, files in os.walk(path):
        for file in files:
            if file=="uac.log":
                machine_path=root
                machine_name=machine_path.split("\\")[-2]
                root_path = machine_path+"\\[root]"
                machines.append((machine_name,machine_path,root_path))
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
    return("uac_linux")

def get_description():
    return("Searches for uac linux machines in a triage path by looking for uac.log files")