import pandas as pd
import os
import LnkParse3

df_recent= pd.DataFrame({"shortcut":[],"path":[],"user":[]})

def readRecentUser(user,userPath):
    global df_recent
    recentPath=os.path.join(userPath,"AppData\Roaming\Microsoft\Windows\Recent")
    if not os.path.isdir(recentPath):
        return()
    for path in os.listdir(recentPath):
        if not path.endswith(".lnk"):
            continue
        try:
            with open(os.path.join(recentPath,path), 'rb') as indata:
                shortcut = LnkParse3.lnk_file(indata)
                shortcut=shortcut.get_json()
                if shortcut["link_info"]["local_base_path"]:
                    df_recent=df_recent._append({"shortcut":path,"path":shortcut["link_info"]["local_base_path"],"user":user},ignore_index=True)
                else:
                    df_recent=df_recent._append({"shortcut":path,"path":"nofile","user":user},ignore_index=True)
        except Exception as e:
            continue

def readRecentUsers(extract_path):
    usersPath=extract_path+"\\Users"
    for path in os.listdir(usersPath):
        if not os.path.isdir(os.path.join(usersPath, path)):
            continue
        readRecentUser(path,os.path.join(usersPath, path))

def execute(config):
    # check if module already runned on this machine
    if os.path.isfile(config["drive_path"]+"\\CSVs\\recents.csv"):
        return()
    readRecentUsers(config["drive_path"])
    df_recent.to_csv(config["drive_path"]+"\\CSVs\\recents.csv",index=False)


def get_dependencies():
    return([])

def get_outputs():
    return([("recents.csv","recents")])

def get_type():
    return("machine_module")

def get_name():
    return("recents_parser")

def get_machine_type():
    return("windows")

def get_description():
    return("Extracts information from the recents folder")
