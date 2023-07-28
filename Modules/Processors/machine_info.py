from Registry import Registry
import os
from os.path import exists
import pandas as pd

def get_SO_info_json(config):
    #open the SAM hive
    rootPath = config["drive_path"]
    SAM = rootPath + "\\Windows\\System32\\config\\SAM"
    if not exists(SAM):
        print("SAM not found, check CyLr path")
        return()
    reg = Registry.Registry(SAM)
    #machine info on HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion
    key = reg.open("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion")
    # get product name and verion
    for value in key.values():
        if value.name() == "ProductName":
            product_name = value.value()
        if value.name() == "CurrentVersion":
            version = value.value()
    # get the machine name
    key = reg.open("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName")
    for value in key.values():
        if value.name() == "ComputerName":
            machine_name = value.value()
    # get the machine SID
    key = reg.open(r"HKEY_LOCAL_MACHINE\SAM\Domains\Account\Users\Names")
    for value in key.values():
        if value.name() == "Administrator":
            machine_sid = value.value().split("-")[0]
    # get the machine domain
    key = reg.open("HKEY_LOCAL_MACHINE\SAM\SAM\Domains\Account")
    for value in key.values():
        if value.name() == "V":
            machine_domain = value.value().split("\\")[0]
    # get the machine domain
    key = reg.open(r"HKEY_LOCAL_MACHINE\SAM\Domains\Account\Users\Names")
    for value in key.values():
        if value.name() == "Administrator":
            machine_sid = value.value().split("-")[0]
    # add all the info to a dictionary
    machine_data={}
    machine_data["machine_name"]=machine_name
    machine_data["machine_sid"]=machine_sid
    machine_data["machine_domain"]=machine_domain
    machine_data["product_name"]=product_name
    machine_data["version"]=version
    return(machine_data)
    





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
    df_run_tmp = pd.DataFrame({"path":[],"user":[]})
    reg = Registry.Registry(SOFTWARE)
    values = reg.open("Microsoft\\Windows\\CurrentVersion\\Run")
    for value in values.values():
        df_run_tmp.loc[len(df_run_tmp.index)] = [value.values().strip(),"system"]
    values = reg.open("Microsoft\\Windows\\CurrentVersion\\RunOnce")
    for value in values.values():
        df_run_tmp.loc[len(df_run_tmp.index)] = [value.values().strip(),"system"]
    values = reg.open("WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Run")
    for value in values.values():
        df_run_tmp.loc[len(df_run_tmp.index)] = [value.values().strip(),"system"]
    values = reg.open("WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\RunOnce")
    for value in values.values():
        df_run_tmp.loc[len(df_run_tmp.index)] = [value.values().strip(),"system"]
    return df_run_tmp

def getUserRuns(SOFTWARE, username,extract_path):
    df_run_tmp = pd.DataFrame({"path":[],"user":[]})
    reg = Registry.Registry(SOFTWARE)
    try:
        values = reg.open("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run")
        for value in values.values():
            df_run_tmp.loc[len(df_run_tmp.index)] = [value.values().strip(),username]
    except:
       pass
    try:
        values = reg.open("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce")
        for value in values.values():
            df_run_tmp.loc[len(df_run_tmp.index)] = [value.values().strip(),username]
    except:
       pass
    try:
        values = reg.open("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Runonce")
        for value in values.values():
            df_run_tmp.loc[len(df_run_tmp.index)] = [value.values().strip(),username]
    except:
       pass
    
    return df_run_tmp

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
    machine_data=get_SO_info_json(config)
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
        df_run_tmp = pd.DataFrame({"path":[],"user":[]})
        for f in os.scandir(rootPath + "\\Users"):
            try:
                SOFTWARE = rootPath + "\\Users\\" + f.name + "\\NTUSER.DAT"
                df_run_tmp=pd.concat(df_run_tmp,getUserRuns(SOFTWARE, f.name,rootPath))
            except:
                pass
        df_run_tmp.to_csv(rootPath+'\\CSVs\\run-runonce.csv', index=False)        
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

def get_description():
    return("Extracts information from the machine")
