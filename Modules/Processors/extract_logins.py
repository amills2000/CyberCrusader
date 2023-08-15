import sys
import win32com.client 
import pandas as pd
import os
import LnkParse3
import win32evtlog
import xml.etree.ElementTree as ET
from os.path import exists

def readfile(cylr_path,machine):
    df_connection = pd.DataFrame({"src_ip":[],"src":[],"dest":[],"logontime":[],"logontype":[],"user":[],"source":[]})

    if not exists(cylr_path+"\Windows\System32\winevt\Logs\Security.evtx"):
        return
    query_handle = win32evtlog.EvtQuery(
        cylr_path+"\Windows\System32\winevt\Logs\Security.evtx",
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
                        df_connection.loc[len(df_connection.index)] = [IpAddress,WorkstationName,computer.split(".")[0],time_created,LogonType,TargetUserName,"security"]
            except Exception as e:
                i=1
    # extract logins from incoming RDP connections from RDP logs
    if not exists(cylr_path+"\Windows\System32\winevt\Logs\Microsoft-Windows-TerminalServices-RemoteConnectionManager%4Operational.evtx"):
        execute=False
    else: 
        execute=True
        query_handle = win32evtlog.EvtQuery(
            cylr_path+"\Windows\System32\winevt\Logs\Microsoft-Windows-TerminalServices-RemoteConnectionManager%4Operational.evtx",
            win32evtlog.EvtQueryFilePath)
    a=1
    while execute:
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
                if event_id=="1149":
                    computer = xml.find(f'.//{ns}Computer').text
                    event_data =xml.find(f'.//{ns}EventData')
                    json_data = {}
                    for data in event_data:
                            json_data[data.attrib["Name"]] = data.text
                    IpAddress = json_data["IpAddress"] 
                    Domain = json_data["Domain"]
                    User = json_data["User"]
                    time_created = xml.find(
                        f'.//{ns}TimeCreated').get('SystemTime')

                    event_data = f'Time: {time_created}, Computer: {computer}, Event Id: {event_id}, IpAddress: {IpAddress}, Domain: {Domain}, User: {User}'
                    if IpAddress and len(IpAddress)>4:
                        df_connection.loc[len(df_connection.index)] = [IpAddress,computer.split(".")[0],machine,time_created,"RDP",User,"RDP"]
            except Exception as e:
                i=1
    # remove duplicates from security and RDP logs by time and source ip giving a 5 minute window
    df_connection["logontime"] = pd.to_datetime(df_connection["logontime"])
    df_connection = df_connection.sort_values(by=['logontime'])
    df_connection = df_connection.drop_duplicates(subset=['src_ip','logontime'], keep='first')

    df_connection.to_csv(cylr_path+'\\CSVs\\logins.csv', index=False) 
    return df_connection



def execute(config):
    # check if module already runned on this machine
    if os.path.isfile(config["drive_path"]+"\\CSVs\\logins.csv"):
        return()
    readfile(config["drive_path"],config["machine_name"])


def get_dependencies():
    return([])

def get_outputs():
    return(["logins"])

def get_type():
    return("machine_module")

def get_name():
    return("extract_logins")

def get_machine_type():
    return("windows")

def get_description():
    return("Extracts logins from a variety of sources on the machine")
