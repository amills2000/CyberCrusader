import os
import pandas as pd
def execute(config):
    # given a linux machine root files path, extract all users and its information
    # check if module already runned on this machine
    if os.path.isfile(config["drive_path"]+"\\CSVs\\linux_users.csv"):
        return()
    users={}   
    try:
        #get the users and their information from /etc/passwd
        with open(config["drive_path"]+"\\etc\\passwd", "r") as f:
            #read line by line and extract the information
            for line in f:
                line=line.strip().split(":")
                #extract the information
                users[line[0]]={
                    "password":line[1],
                    "uid":line[2],
                    "gid":line[3],
                    "description":line[4],
                    "home":line[5],
                    "shell":line[6]
                }
    except:
        pass
    #save user information to csv and to json
    df=pd.DataFrame(users)
    df=df.transpose().rename_axis('user')
    df.to_csv(config["drive_path"]+"\\CSVs\\linux_users.csv")
    with open(config["drive_path"]+"\\JSONs\\linux_users.json", "w") as file1:
        file1.write(df.to_json())
def get_dependencies():
    return([])

def get_outputs():
    return(["linux_users"])

def get_type():
    return("machine_module")

def get_name():
    return("get_linux_users")

def get_machine_type():
    return("linux","linux_uac")

def get_description():
    return("Extracts linux users and its information")
