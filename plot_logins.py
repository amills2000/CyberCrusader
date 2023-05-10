import win32evtlog
import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
from os.path import exists
import os
import argparse
import math
from datetime import datetime 
import pandas as pd

def readfile(cylr_path,machine):
    df_connection = pd.DataFrame({"src_ip":[],"src":[],"dest":[],"logontime":[],"logontype":[],"user":[]})

    if not exists(cylr_path+"\Windows\System32\winevt\Logs/Security.evtx"):
        return
    query_handle = win32evtlog.EvtQuery(
        cylr_path+"\Windows\System32\winevt\Logs/Security.evtx",
        win32evtlog.EvtQueryFilePath)

    a=1
    while True:
        a += 1
        # read 1 record(s)
        events = win32evtlog.EvtNext(query_handle, 1)
        # if there is no record break the loop
        if len(events) == 0:
            break

        for event in events:
            try: 
                xml_content = win32evtlog.EvtRender(
                    event, win32evtlog.EvtRenderEventXml)
                # parse xml content
                xml = ET.fromstring(xml_content)
                import json
                #print(xml_content)
                
                ns = '{http://schemas.microsoft.com/win/2004/08/events/event}'


                event_id = xml.find(f'.//{ns}EventID').text
                if event_id=="4624":
                    computer = xml.find(f'.//{ns}Computer').text
                    event_data =xml.find(f'.//{ns}EventData')
                    json_data = {}
                    for data in event_data:
                            json_data[data.attrib["Name"]] = data.text
                    TargetUserName = json_data["TargetUserName"]
                    WorkstationName = json_data["WorkstationName"]
                    IpAddress = json_data["IpAddress"] 
                    LogonType = json_data["LogonType"]
                    TargetDomainName = json_data["TargetDomainName"]
                    time_created = xml.find(
                        f'.//{ns}TimeCreated').get('SystemTime')


                    event_data = f'Time: {time_created}, Computer: {computer}, Event Id: {event_id}, TargetUserName: {TargetUserName}, WorkstationName: {WorkstationName}, IpAddress: {IpAddress}, LogonType: {LogonType}, TargetDomainName: {TargetDomainName}'
                    if IpAddress and len(IpAddress)>4 and (LogonType=="10" or LogonType=="3") and not computer.split(".")[0]==WorkstationName:
                        print(event_data)
                        df_connection.loc[len(df_connection.index)] = [IpAddress,WorkstationName,computer.split(".")[0],time_created,LogonType,TargetUserName]
            except Exception as e:
                i=1
    
    df_connection.to_csv(cylr_path+'\\CSVs\\\logins'+machine+".csv", index=False) 
    return df_connection



def extract_logins(cylrs_path,args):
    print("Extracting logins")
    df_connection = pd.DataFrame({"src_ip":[],"src":[],"dest":[],"logontime":[],"logontype":[],"user":[]})
    for path in os.listdir(cylrs_path):
        # check if current path is a file
        extract_path=os.path.join(cylrs_path, path)
        if not os.path.isfile(extract_path):
            info_folders=[]
            for path_extract_folder in os.listdir(extract_path):
                if os.path.isdir(os.path.join(extract_path,path_extract_folder)):
                    folders_in_path_extract_folder=os.listdir(os.path.join(extract_path,path_extract_folder))
                    if "Windows" in folders_in_path_extract_folder and "Users" in folders_in_path_extract_folder:
                        if (not exists(os.path.join(extract_path,path_extract_folder)+'\\CSVs\\logins'+path+".csv") or args.force):
                            print("Extracting logins from machine",path)
                            df_connection=pd.concat([df_connection,readfile(os.path.join(extract_path,path_extract_folder),path)], ignore_index=True)
                        else:
                            print("reading logins from machine",path)
                            df_connection.pd.concat([df_connection,pd.read_csv(os.path.join(extract_path,path_extract_folder)+'\\CSVs\\logins'+path+".csv")],ignore_index=True)
                            
    df_connection.to_csv(cylrs_path+'\\logins.csv', index=False) 
    (df_connection.groupby('user').value_counts(subset=["dest","src_ip"],normalize=True)).to_csv(cylrs_path+"\\login_stats.csv")


 
