import subprocess
import requests
import urllib
import os
import pandas as pd
def execute(config):
    # check if module already runned on this machine
    if not os.path.isfile(config["drive_path"]+"\\CSVs\\MFT.csv"):
        return()
    if os.path.isfile(config["drive_path"]+"\\CSVs\\MFT_vip_ext.csv"):
        return()
    try:
        df = pd.read_csv(config["drive_path"]+"\CSVs\MFT.csv",sep='|')
        # parse date
        df['date'] = pd.to_datetime(df['$FILENAME Creation Time'], format='%Y-%m-%d %H:%M:%S')
        ext="BAT,BIN,CMD,COM,CPL,EXE,GADGET,INF1,INS,INX,ISU,JOB,JSE,LNK,MSC,MSI,MSP,MST,PAF,PIF,PS1,REG,RGS,SCR,SCT,SHB,SHS,U3P,VB,VBE,VBS,VBSCRIPT,WS,WSF,WSH".replace(",","|")
        df=df[df.File.str.contains('\.(?:'+ext+')$', case=False)]
        df.to_csv(config["drive_path"]+"\CSVs\MFT_vip_ext.csv")
    except Exception as e:
        print("Error on MFT tool"+str(e)+"\n")

def get_dependencies():
    return(["mft_transcoder"])

def get_outputs():
    return(["ext_filtered_MFT"])

def get_type():
    return("machine_module")

def get_name():
    return("mft_vip_exts")

def get_machine_type():
    return("windows")

def get_description():
    return("Extracts the most important extensions from the MFT")
