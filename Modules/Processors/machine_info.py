from Registry import Registry
import os
from os.path import exists
import pandas as pd
import json

def get_SO_info_json(config):
    #open the SAM hive
    rootPath = config["drive_path"]
    SAM = rootPath + "\\Windows\\System32\\config\\SAM"
    SYSTEM = rootPath + "\\Windows\\System32\\config\\SYSTEM"
    SOFTWARE = rootPath + "\\Windows\\System32\\config\\SOFTWARE"
    machine_data={}
    if not exists(SAM):
        raise Exception("SAM not found, check CyLr path")
    if not exists(SOFTWARE):
        raise Exception("SOFTWARE not found, check CyLr path")
    if not exists(SYSTEM):
        raise Exception("SYSTEM not found, check CyLr path")
    reg_sam = Registry.Registry(SAM)
    reg_software = reg = Registry.Registry(SOFTWARE)
    reg_system = reg = Registry.Registry(SYSTEM)
    #machine info on HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion
    try:
        key = reg_software.open("Microsoft\Windows NT\CurrentVersion")
        # get product name and verion
        for value in key.values():
            if value.name() == "ProductName":
                product_name = value.value()
                machine_data["product_name"]=product_name
            if value.name() == "CurrentVersion":
                version = value.value()
                machine_data["version"]=version
    except Exception as e:
        print(f"\033[91m"+"Error on SAM hive"+str(e)+"\n"+"\033[0m")
    # get the machine name
    try:
        key = reg_system.open("ControlSet001\Control\ComputerName\ComputerName")
        for value in key.values():
            if value.name() == "ComputerName":
                machine_name = value.value()
                machine_data["machine_name"]=machine_name
    except Exception as e:
        print(f"\033[91m"+"Error on SAM hive"+str(e)+"\n"+"\033[0m")
    # get the machine SID
    try:
        key = reg_sam.open(r"Domains\Account\Users\Names")
        for value in key.values():
            if value.name() == "Administrator":
                machine_sid = value.value().split("-")[0]
                machine_data["machine_sid"]=machine_sid
    except Exception as e:
        print(f"\033[91m"+"Error on SAM hive"+str(e)+"\n"+"\033[0m")
    # get the machine domain
    try:
        key = reg_sam.open("SAM\Domains\Account")
        for value in key.values():
            if value.name() == "V":
                machine_domain = value.value().split("\\")[0]
                machine_data["machine_domain"]=machine_domain
    except Exception as e:
        print(f"\033[91m"+"Error on SAM hive"+str(e)+"\n"+"\033[0m")
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
    try:
        values = reg.open("Microsoft\\Windows\\CurrentVersion\\Run")
        for value in values.values():
            df_run_tmp.loc[len(df_run_tmp.index)] = [value.values().strip(),"system"]
    except Exception as e:
        print(f"\033[91m"+"Error on SOFTWARE hive"+str(e)+"\n"+"\033[0m")
    try:
        values = reg.open("Microsoft\\Windows\\CurrentVersion\\RunOnce")
        for value in values.values():
            df_run_tmp.loc[len(df_run_tmp.index)] = [value.values().strip(),"system"]
    except Exception as e:
        print(f"\033[91m"+"Error on SOFTWARE hive"+str(e)+"\n"+"\033[0m")
    try:
        values = reg.open("WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Run")
        for value in values.values():
            df_run_tmp.loc[len(df_run_tmp.index)] = [value.values().strip(),"system"]
    except Exception as e:
        print(f"\033[91m"+"Error on SOFTWARE hive"+str(e)+"\n"+"\033[0m")
    try:
        values = reg.open("WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\RunOnce")
        for value in values.values():
            df_run_tmp.loc[len(df_run_tmp.index)] = [value.values().strip(),"system"]
    except Exception as e:
        print(f"\033[91m"+"Error on SOFTWARE hive"+str(e)+"\n"+"\033[0m")
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
        print(f"\033[91m"+"SYSTEM not found, check CyLr path"+"\033[0m")
    else:
        machine_data["IPs"]=printIP(SYSTEM)
        
        getServices(SYSTEM,rootPath)
    if not exists(SOFTWARE):
        print(f"\033[91m"+"SYSTEM not found, check CyLr path"+"\033[0m")
    else:
        machine_data["users"]=printUsers(SOFTWARE)
        
        getRuns(SOFTWARE,rootPath)
        
    if not exists(rootPath + "\\Users"):
        print(f"\033[91m"+"Users not found, check CyLr path"+"\033[0m")
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
        file1.write(json.dumps(machine_data))
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
