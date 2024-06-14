import os
import pandas as pd
def execute(config):
    # check if module already runned on this machine
    if not os.path.isfile(config["drive_path"]+"\\CSVs\\MFT.csv"):
        return()
    if os.path.isfile(config["drive_path"]+"\\CSVs\\MFT_vip_ext.csv"):
        return()
    try:
        search=""
        with open("./Modules/tools/suspicious_tools.txt") as f:
            content = f.readlines()
            for line in content:
                search=search+line.strip()+"|"
        if len(search)==0:
            print("suspicious_tools.txt is empty")
        search=search.rstrip('|')
        df = pd.read_csv(config["drive_path"]+"\CSVs\MFT.csv",sep='|')
        # parse date
        df['date'] = pd.to_datetime(df['$FILENAME Creation Time'], format='%Y-%m-%d %H:%M:%S')
        df=df[df.File.str.contains('(?:'+search+')', case=False)]
        if len(df)>0:
            df.to_csv(config["drive_path"]+"\CSVs\MFT_suspicious_tools.csv")
    except Exception as e:
        print("Error on MFT tool"+str(e)+"\n")

def get_dependencies():
    return(["mft_transcoder"])

def get_outputs():
    return(["ext_filtered_MFT"])

def get_type():
    return("machine_module")

def get_name():
    return("mft_suspicious_searcher")

def get_machine_type():
    return("windows")

def get_description():
    return("Searches the strings inside /Modules/Tools/suspicious_tools.txt on the MFT")
