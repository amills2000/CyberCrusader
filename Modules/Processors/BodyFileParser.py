import os
import subprocess
import pandas as pd

def execute(config):
    extract_path=config["drive_path"]
    
    #check if module already runned on this machine
    if os.path.isfile(extract_path+"\\CSVs\\BodyFile.csv"):
        return()
    #extract the bodyfile information by opening the file extract_path+bodyfile/bodyfile.txt with pandas with | as separators
    #columns are: MD5|name|inode|mode_as_string|UID|GID|size|atime|mtime|ctime|crtime
    try:
        df=pd.read_csv(extract_path+"\\bodyfile\\bodyfile.txt", sep="|", header=None)
        df.columns=["MD5","name","inode","mode_as_string","UID","GID","size","atime","mtime","ctime","crtime"]
        #format *time so it is readable by excel in utc0
        df["atime"]=pd.to_datetime(df["atime"], unit="s").dt.strftime('%Y-%m-%d %H:%M:%S')
        df["mtime"]=pd.to_datetime(df["mtime"], unit="s").dt.strftime('%Y-%m-%d %H:%M:%S')
        df["ctime"]=pd.to_datetime(df["ctime"], unit="s").dt.strftime('%Y-%m-%d %H:%M:%S')
        df["crtime"]=pd.to_datetime(df["crtime"], unit="s").dt.strftime('%Y-%m-%d %H:%M:%S')
        #save the bodyfile information to a csv
        df.to_csv(extract_path+"\\CSVs\\BodyFile.csv", index=False)

    except:
        pass

def get_dependencies():
    return([])

def get_outputs():
    return([("BodyFile.csv","BodyFile")])

def get_type():
    return("machine_module")

def get_name():
    return("BodyFileParser")

def get_machine_type():
    return("uac_linux")

def get_description():
    return("Parses the bodyfile file into a CSV file")