from zipfile import ZipFile 
import os
import argparse
import subprocess
import sys
from Registry import Registry
from os.path import exists
import numpy as np
import pandas as pd
import datetime as datetime
from pathlib import Path
from mft import *
from regtest import *
from plot_logins import *
from join_excel import * 
from browser_history import *

def extractfile(extract_path,file_path):
    print("Extracting "+extract_path)
    with ZipFile(file_path, 'r') as zip_ref:
        failes_extractions=""
        for name in zip_ref.namelist():
            try:
                zip_ref.extract(name, extract_path)
            except Exception as e:
                failes_extractions=failes_extractions+str(e)+"\n"
        if len(failes_extractions)>0:
            with open(os.path.join(extract_path,"failed extractions.txt"), "w") as file1:
                # Writing data to a file
                file1.writelines(failes_extractions)

def tools_execution(extract_path,args):
        #Executing tools:
        tools_errors=""
        # extracting MFT
        if args.mft:
            try:
                subprocess.check_call([r".\tools\mft.exe", "transcode", extract_path+"\$MFT",extract_path+"\CSVs\MFT.csv"])
            except Exception as e:
                tools_errors=tools_errors+"Error on MFT tool"+str(e)+"\n"
        # executing chainsaw
        if args.chainsaw:
            if (not exists(extract_path+"\CSVs\sigma.csv")) or args.force:
                try:
                    subprocess.check_call([r".\tools\chainsaw\chainsaw.exe", "hunt", extract_path+"\Windows\System32\winevt\Logs","-s",".\\tools\chainsaw\sigma","--mapping", ".\\tools\chainsaw\mappings\sigma-event-logs-all.yml","--csv","--output",extract_path+"\CSVs","--skip-errors"])
                except Exception as e:
                    tools_errors=tools_errors+"Error on chainsaw tool"+str(e)+"\n"
        if args.amcache_data:
            if (not exists(extract_path+"\CSVs\sig3ma.csv")) or args.force:
                try:
                    subprocess.check_call([r".\tools\AmcacheParser\AmcacheParser.exe", "-f", extract_path+"\Windows\\appcompat\Programs\Amcache.hve","--csv",extract_path+"\CSVs"])
                except Exception as e:
                    tools_errors=tools_errors+"Error on AmcacheParser tool"+str(e)+"\n"
        if args.appcompatcacheparser_data:
            if (not exists(extract_path+"\CSVs\sig3ma.csv")) or args.force:
                try:
                    subprocess.check_call([r".\tools\AppCompatCacheParser\AppCompatCacheParser.exe", "-f", extract_path+"\Windows\System32\config\SYSTEM","--csv",extract_path+"\CSVs"])
                except Exception as e:
                    tools_errors=tools_errors+"Error on AppCompatCacheParser tool"+str(e)+"\n"
        if args.regTest:
            try:
                regTest(extract_path)
            except Exception as e:
                tools_errors=tools_errors+"Error on regtest tool"+str(e)+"\n"
        if args.mft_ext:
            try:
                search_exe(extract_path)
            except Exception as e:
                tools_errors=tools_errors+"Error on MFT executable searching tool"+str(e)+"\n"
        if args.mft_search:
            try:
                search_sring_mft(extract_path,args.mft_search)
            except Exception as e:
                tools_errors=tools_errors+"Error on MFT search"+str(e)+"\n"
        if args.mft_st:
            try:
                search_suspicious_strings(extract_path)
            except Exception as e:
                tools_errors=tools_errors+"Error on MFT search"+str(e)+"\n"
        if args.browser_data:
            get_allbrowser_data_by_user(extract_path)
        if len(tools_errors)>0:
            with open(os.path.join(extract_path,"tool errors.txt"), "w") as file1:
                # Writing data to a file
                file1.writelines(tools_errors)
        


parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-p", "--path", help = "CYRL path", required=True)
parser.add_argument("-c", "--chainsaw", help = "don't run chainsaw", action='store_false')
parser.add_argument("-r", "--regTest", help = "don't run regTest", action='store_false')
parser.add_argument("-m", "--mft", help = "don't run mft to csv", action='store_false')
parser.add_argument("-me", "--mft_ext", help = "don't create a csv with only suspicious extention", action='store_false')
parser.add_argument("-mst", "--mft_st", help = "don't create a csv with suspicious tools", action='store_false')
parser.add_argument("-ms", "--mft_search", help = "search string on mft")
parser.add_argument("-el", "--extract_logins", help = "create a csv for all the logins on heach machine plus a common one", action='store_false')
parser.add_argument("-bd", "--browser_data", help = "extract browser data", action='store_false')
parser.add_argument("-amcd", "--amcache_data", help = "Am cache data", action='store_false')
parser.add_argument("-appcc", "--appcompatcacheparser_data", help = "App compat cache data", action='store_false')
parser.add_argument("-f", "--force", help = "forces the execution of tools as well as extraction", action='store_true')



args = parser.parse_args()

dir_path=args.path
df_users = pd.DataFrame({"Machine":[],"USER":[]})
df_ips= pd.DataFrame({"Machine":[],"IP":[]})
# Iterate directory
for path in os.listdir(dir_path):
    if path.endswith(".zip"):
        print("processing "+path)
        extract_path=os.path.join(dir_path, ".".join(path.split(".")[:-1]))
        #extracting ZIP if necessari 
        if (not os.path.exists(extract_path)) or args.force:
            if not os.path.exists(extract_path): os.makedirs(extract_path)
            extractfile(extract_path,os.path.join(dir_path,path))
    elif os.path.isdir(os.path.join(dir_path, path)):
        extract_path=os.path.join(dir_path, path)
    # check is triage
    info_folders=[]
    for path_extract_folder in os.listdir(extract_path):
        if os.path.isdir(os.path.join(extract_path,path_extract_folder)):
            folders_in_path_extract_folder=os.listdir(os.path.join(extract_path,path_extract_folder))
            if "Windows" in folders_in_path_extract_folder and "Users" in folders_in_path_extract_folder:
                info_folders.append(path_extract_folder)

    for folder in info_folders:
        if not os.path.exists(os.path.join(extract_path,folder,"CSVs")):
            os.makedirs(os.path.join(extract_path,folder,"CSVs"))
        #execute tools
        tools_execution(os.path.join(extract_path,folder),args)
        #sumarize users
        if exists(extract_path+"\\CSVs\\users.csv"):
            try:
                df_u_temp = pd.read_csv(extract_path+"\\CSVs\\users.csv")
                df_u_temp["Machine"]=".".join(path.split(".")[:-1])
                df_u_temp.drop(columns=["SID"])
                df_users=pd.concat([df_users,df_u_temp], ignore_index=True)
            except Exception as e:
                print("Error os usear read for",extract_path,"\\CSVs\\users.csv")
        #sumarize users
        if exists(extract_path+"\\IPS.txt"):
            with open(extract_path+"\\IPS.txt", "r") as f:
                for l in f:
                    df_ips.loc[len(df_ips.index)] = [".".join(path.split(".")[:-1]),l]
        join_excel(os.path.join(extract_path,folder))



if args.extract_logins:
    try:
        extract_logins(dir_path,args)
    except Exception as e:
        print("Error plot logins",str(e))
#output results
df_users.to_csv(dir_path+'\\users.csv', index=False) 
df_users["USER"].value_counts().apply(lambda x:x/df_users["Machine"].nunique()).to_csv(dir_path+'\\users_stats.csv', index=True) 
df_ips.to_csv(dir_path+'\\ips.csv', index=False)
