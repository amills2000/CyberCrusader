from Registry import Registry
import os
from os.path import exists
import pandas as pd
import json

def getUserMRURuns(SOFTWARE, username,extract_path):
    df_mrurun_tmp = pd.DataFrame({"command":[],"user":[]})
    reg = Registry.Registry(SOFTWARE)
    try:
        values = reg.open("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU")
        for value in values.values(): 
           df_mrurun_tmp.loc[len(df_mrurun_tmp.index)] = [value.value(),username]
    except:
       pass
    return(df_mrurun_tmp)

def execute(config):
    #check if module already runned on this machine
    if exists(config["drive_path"]+"\\CSVs\\runMRU.csv"):
        return()
    rootPath = config["drive_path"]
        
    if not exists(rootPath + "\\Users"):
        print(f"\033[91m"+" * Users not found, check CyLr path"+"\033[0m")
    else:
        df_run_tmp = pd.DataFrame({"command":[],"user":[]})
        for f in os.scandir(rootPath + "\\Users"):
            try:
                SOFTWARE = rootPath + "\\Users\\" + f.name + "\\NTUSER.DAT"
                df_run_tmp=pd.concat([df_run_tmp,getUserMRURuns(SOFTWARE, f.name,rootPath)], ignore_index=True)
            except:
                pass
        df_run_tmp.to_csv(rootPath+'\\CSVs\\runMRU.csv', index=False)   
    
def get_dependencies():
    return([])

def get_outputs():
    return(["Runmru_csv"])

def get_type():
    return("machine_module")

def get_name():
    return("runMRU")

def get_machine_type():
    return("windows")

def get_description():
    return("Extracts information runMRU of each user win+r")
