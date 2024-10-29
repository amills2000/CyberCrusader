import subprocess
import os

def execute(config):
    path=config["path"]
    #recurivelly iterate directories and detect all Machine paths, where a machine path is a directory that contains a $MFT file and return all in an array of tuples containing the machine name, the type and the path extract the name from the path where is not the drive leter
    machines={}

    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if dir=="LiveResponse":
                machine_path=os.path.join(root,dir)
                machine_name=machine_path.split("\\")[-2]
                if machine_name not in machines:
                    machines[machine_name]=(machine_name,machine_path,{"LiveResponse":True})
                else:
                    machines[machine_name][2]["LiveResponse"]=True
                
        for file in files:
            if file=="$MFT":
                machine_path=root
                machine_name=machine_path.split("\\")[-2]
                if machine_name not in machines:
                    machines[machine_name]=(machine_name,machine_path,{"MFT":True})
                else:
                    machines[machine_name][2]["MFT"]=True
    machines_out=[]
    for machine in machines:
        if "MFT" in machines[machine][2] and "LiveResponse" in machines[machine][2]:
            machines_out.append((machines[machine][0],machines[machine][1]))
    print(machines_out)
    print(machines)
    return machines_out
def get_dependencies():
    return(["triage_path"])

def get_outputs():
    return(["machine"])

def get_type():
    return("machine_finders")

def get_name():
    return("windows_live_response_machine_searcher")

def get_machine_type():
    return("windows_live_response")

def get_description():
    return("Searches for windows machines with live response in a triage path by looking for $MFT files and live response folder (Extracted with tools like kape or CYLR)")