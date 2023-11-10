import subprocess
import requests
import urllib
import os
import pandas as pd
def execute(config):
    keys="user,file,key_type,key\n"
    #extract all the ssh keys and its information from all users
    # check if module already runned on this machine
    if os.path.isfile(config["drive_path"]+"\\CSVs\\linux_ssh_keys.csv"):
        return()
    #itereate all home directories
    for path in os.listdir(config["drive_path"]+"\\home"):
        #check if the user has a .ssh folder
        if not os.path.isdir(config["drive_path"]+"\\home\\"+path+"\\.ssh"):
            continue
        #iterate the files in the .ssh folder
        for file in os.listdir(config["drive_path"]+"\\home\\"+path+"\\.ssh"):
            #check if the file is a key
            if not file.endswith(".pub"):
                continue
            #extract the key information
            try:
                with open(config["drive_path"]+"\\home\\"+path+"\\.ssh\\"+file, "r") as f:
                    key=f.read().strip().split(" ")
                    keys+=path+","+file+","+key[0]+","+key[1]+"\n"
            except:
                pass
    #save the keys to a csv
    with open(config["drive_path"]+"\\CSVs\\linux_ssh_keys.csv", "w") as f:
        f.write(keys)

def get_dependencies():
    return([])

def get_outputs():
    return(["linux_ssh_keys"])

def get_type():
    return("machine_module")

def get_name():
    return("get_linux_ssh_keys")

def get_machine_type():
    return("linux")

def get_description():
    return("Extracts linux ssh keys and its information")
