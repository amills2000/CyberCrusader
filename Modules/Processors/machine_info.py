from Registry import Registry
import os
from os.path import exists
import pandas as pd


def getServices(SYSTEM,extract_path):
    f = open(extract_path+"\\CSVs\\services.csv",'w',encoding='utf-8')
    reg = Registry.Registry(SYSTEM)

    # iterate all ControlSet00X
    for i in range(1, 10):
        try:
            key = reg.open("ControlSet00" + str(i) + "\\Services")
            for subkey in key.subkeys():
                subkey = ''.join(subkey.path().partition("ControlSet00" + str(i))[1:3])
                values = reg.open(subkey)
                DisplayName = ""
                ImagePath = ""
                timestamp = str(values.timestamp())
                for value in values.values():
                    if(str(value.name()) == "DisplayName"):
                        DisplayName = value.value()
                    if(str(value.name()) == "ImagePath"):
                        ImagePath = value.value()
                if DisplayName != "" and ImagePath != "":
                    f.write(DisplayName + "|" + ImagePath + "|" + timestamp + "\n")
        except:
            pass
    f.close()

def getRuns(SOFTWARE,extract_path):
    f = open(extract_path+"\\CSVs\\run-runonce-system.csv",'w',encoding='utf-8')
    reg = Registry.Registry(SOFTWARE)
    values = reg.open("Microsoft\\Windows\\CurrentVersion\\Run")
    for value in values.values():
        f.write(value.value() + "\n")
    values = reg.open("Microsoft\\Windows\\CurrentVersion\\RunOnce")
    for value in values.values():
        f.write(value.value() + "\n")
    values = reg.open("WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Run")
    for value in values.values():
        f.write(value.value() + "\n")
    values = reg.open("WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\RunOnce")
    for value in values.values():
        f.write(value.value() + "\n")
    f.close()

def getUserRuns(SOFTWARE, username,extract_path):
    f = open(extract_path+"\\CSVs\\run-runonce-" + username + ".csv",'w',encoding='utf-8')
    reg = Registry.Registry(SOFTWARE)
    try:
        values = reg.open("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run")
        for value in values.values():
            f.write(value.value() + "\n")
    except:
       pass
    try:
        values = reg.open("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce")
        for value in values.values():
            f.write(value.value() + "\n")
    except:
       pass
    try:
        values = reg.open("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Runonce")
        for value in values.values():
            f.write(value.value() + "\n")
    except:
       pass
    f.close()  

def printIP(SYSTEM):
    reg = Registry.Registry(SYSTEM)
    key = reg.open("ControlSet001\\Services\\Tcpip\\Parameters\\Interfaces")
    ips=[]
    for subkey in key.subkeys():
        subkey = ''.join(subkey.path().partition("ControlSet001")[1:3])
        values = reg.open(subkey)
        for value in values.values():
            if value.name() == "DhcpIPAddress" or value.name() == "IPAddress":
                if isinstance(value.value(),str):
                    if len(value.value())>0:
                        ips.append(value.value())
                else:
                    for v in value.value():
                        if len(v)>0:
                                ips.append(str(v))
    return ips

def printUsers(SOFTWARE):
    reg = Registry.Registry(SOFTWARE)
    key = reg.open("Microsoft\\Windows NT\\CurrentVersion\\ProfileList")
    users={}
    for subkey in key.subkeys():
        subkey = ''.join(subkey.path().partition("Microsoft")[1:3])
        sid = subkey.split("\\")[-1:][0]
        values = reg.open(subkey)
        for value in values.values():
            if value.name() == "ProfileImagePath":
                users[str(value.value().split("\\")[-1:][0])]=sid
    return(users)


def execute(config):
    #check if module already runned on this machine
    if exists(config["drive_path"]+"\\JSONs\\machine_info.json"):
        return()
    rootPath = config["drive_path"]
    SYSTEM = rootPath + "\\Windows\\System32\\config\\SYSTEM"
    SOFTWARE = rootPath + "\\Windows\\System32\\config\\SOFTWARE"
    machine_data={}
    if not exists(SYSTEM):
        print("SYSTEM not found, check CyLr path")
    else:
        machine_data["IPs"]=printIP(SYSTEM)
        getServices(SYSTEM,rootPath)
    if not exists(SOFTWARE):
        print("SYSTEM not found, check CyLr path")
    else:
        machine_data["users"]=printUsers(SOFTWARE)
        getRuns(SOFTWARE,rootPath)
    if not exists(rootPath + "\\Users"):
        print("Users not found, check CyLr path")
    else:
        for f in os.scandir(rootPath + "\\Users"):
            try:
                SOFTWARE = rootPath + "\\Users\\" + f.name + "\\NTUSER.DAT"
                getUserRuns(SOFTWARE, f.name,rootPath)
            except:
                pass 
    #save machine data to file
    with open(rootPath+"\\JSONs\\machine_info.json", "w") as file1:
        file1.write(str(machine_data))
    return(machine_data)

    
def get_dependencies():
    return([])

def get_outputs():
    return(["machine_info_json"])

def get_type():
    return("machine_module")

def get_name():
    return("machine_info")

def get_machine_type():
    return("windows")
