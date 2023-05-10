import os
from Registry import Registry
from os.path import exists
import datetime as datetime


def getServices(SYSTEM,extract_path):
    f = open(extract_path+"\\CSVs\\services.csv",'w',encoding='utf-8')
    reg = Registry.Registry(SYSTEM)
    key = reg.open("ControlSet001\\Services")
    for subkey in key.subkeys():
        subkey = ''.join(subkey.path().partition("ControlSet001")[1:3])
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

def printIP(SYSTEM,extract_path):
    reg = Registry.Registry(SYSTEM)
    key = reg.open("ControlSet001\\Services\\Tcpip\\Parameters\\Interfaces")
    ips=""
    for subkey in key.subkeys():
        subkey = ''.join(subkey.path().partition("ControlSet001")[1:3])
        values = reg.open(subkey)
        for value in values.values():
            if value.name() == "DhcpIPAddress" or value.name() == "IPAddress":
                if isinstance(value.value(),str):
                    if len(value.value())>0:
                        ips=ips+value.value()+"\n"
                else:
                    for v in value.value():
                        if len(v)>0:
                                ips=ips+str(v)+"\n"
    with open(os.path.join(extract_path,"IPS.txt"), "w") as file1:
    # Writing data to a file
        file1.writelines(ips)


def printUsers(SOFTWARE,extract_path):
    #HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\<SID>\ProfileImagePath
    reg = Registry.Registry(SOFTWARE)
    key = reg.open("Microsoft\\Windows NT\\CurrentVersion\\ProfileList")
    users="SID,USER\n"
    for subkey in key.subkeys():
        subkey = ''.join(subkey.path().partition("Microsoft")[1:3])
        sid = subkey.split("\\")[-1:][0]
        values = reg.open(subkey)
        for value in values.values():
            if value.name() == "ProfileImagePath":
                users=users+sid + ","+str(value.value().split("\\")[-1:][0])+"\n"
    with open(os.path.join(extract_path,"users.csv"), "w") as file1:
    # Writing data to a file
        file1.writelines(users)


def regTest(extract_path):
    rootPath = extract_path
    SYSTEM = rootPath + "\\Windows\\System32\\config\\SYSTEM"
    SOFTWARE = rootPath + "\\Windows\\System32\\config\\SOFTWARE"

    if not exists(SYSTEM):
        print("SYSTEM not found, check CyLr path")
    else:
        printIP(SYSTEM,rootPath)
        getServices(SYSTEM,rootPath)
    if not exists(SOFTWARE):
        print("SYSTEM not found, check CyLr path")
    else:
        printUsers(SOFTWARE,rootPath)
        getRuns(SOFTWARE,rootPath)
    if not exists(rootPath + "\\Users"):
        print("Users not found, check CyLr path")
    else:
        for f in os.scandir(rootPath + "\\Users"):
            SOFTWARE = rootPath + "\\Users\\" + f.name + "\\NTUSER.DAT"
            getUserRuns(SOFTWARE, f.name,rootPath)  