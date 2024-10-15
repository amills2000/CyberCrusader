import os
import subprocess
import pandas as pd
import requests

def execute(config):
    extract_path=config["drive_path"]
    
    #check if module already runned on this machine
    if os.path.isfile(extract_path+"\\CSVs\\HashExecutablesFiltered.csv"):
        return()
    #open /hash_executables/hash_executables.md5 and split by "  " on pandas columns: md5,file
    df=pd.read_csv(extract_path+"\\hash_executables\\hash_executables.md5", sep="  ", names=["md5", "file"], engine="python")
    #setup a jason {hashes:[hash1,hash2,...]}
    hashes={"hashes":df["md5"].tolist()}
    #create a post request to https://hashlookup.circl.lu/bulk/md5 with the json as body
    response=requests.post("https://hashlookup.circl.lu/bulk/md5", json=hashes)
    #if hash in response[MD5] set column knwn to true else to false
    response_json = response.json()
    known_md5s = [item["MD5"] for item in response_json]
    #set all hashes to lowercase
    known_md5s = [hash.lower() for hash in known_md5s]
    df["known"] = df["md5"].apply(lambda x: x in known_md5s)
    #save the file to a csv
    df.to_csv(extract_path+"\\CSVs\\HashExecutablesFiltered.csv", index=False)

def get_dependencies():
    return([])

def get_outputs():
    return([("HashExecutablesFiltered.csv","HashExecutablesFiltered")])

def get_type():
    return("machine_module")

def get_name():
    return("HashExecutablesFilter")

def get_machine_type():
    return("uac_linux")

def get_description():
    return("Parses the bodyfile file into a CSV file")