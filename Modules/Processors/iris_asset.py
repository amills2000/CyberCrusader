import os
import requests
from zipfile import ZipFile 
import subprocess
import json

def execute(config):
    #open machine info json and get machine name if exists, if not use config machine name
    if os.path.isfile(config["drive_path"]+"\\JSONs\\machine_info.json"):
        with open(config["drive_path"]+"\\JSONs\\machine_info.json", "r") as file1:
            machine_info=file1.read()
        machine_info=json.loads(machine_info)
        machine_name=machine_info["machine_name"]
        #get ip from machine info and join array with , and exclude 0.0.0.0
        ips=""
        for ip in machine_info["IPs"]:
            if ip!="0.0.0.0":
                ips+=ip+","
        if len(ips)>0:
            ips=ips[:-1]
    else:
        machine_name=config["machine_name"]
    #get iris info from configs.json
    with open(".\\configs.json", "r") as file1:
        configs=file1.read()
    configs=json.loads(configs)
    if configs["use_iris"]!="true":
        return()
    iris_url=configs["iris_url"]
    iris_token=configs["iris_token"]

    #check if environe variable case_id exists, if not ask user for case id and store it so it as environe variable
    if "cybercrusader_case_id" not in os.environ:
        #ask user for case id and store it so it as environe variable
        case_id=input("Enter case id: ")
    else:
        case_id=os.environ["cybercrusader_case_id"]
    #if empty case id or empyt config or config use_iris= false do not execute module
    if len(case_id)==0 or len(configs)==0 or configs["use_iris"]!="true":
        return()
    os.environ["cybercrusader_case_id"]=case_id
    
    #get all assets from iris
    url=iris_url+"/case/assets/list?cid="+case_id
    headers = {'Authorization': 'Bearer '+iris_token}
    response = requests.get(url, headers=headers)
    assets=json.loads(response.text)
    assets=assets["data"]["assets"]
    #if asset in iris is the same as machine name do not execute module
    for asset in assets:
        if asset["asset_name"]==machine_name:
            return()
    #if asset not in iris create it
    url=iris_url+"/case/assets/add?cid="+case_id
    if not ips or len(ips)==0:
        ips=""
    body={
        "asset_name": machine_name,
        "asset_type_id": 22,
        "asset_domain": "",
        "asset_ip": ips,
        "asset_info": "",
        "asset_compromise_status_id": 0,
        "analysis_status_id": 1,
        "ioc_links": [],
        "asset_tags": "",
        "asset_description": json.dumps(machine_info,indent=4),
        "custom_attributes": {}
        }
    headers = {'Authorization': 'Bearer '+iris_token}
    response = requests.post(url, headers=headers, json=body)

def get_dependencies():
    return(["machine_info"])

def get_outputs():
    return([])

def get_type():
    return("machine_module")

def get_name():
    return("iris_asset")

def get_machine_type():
    return("windows")

def get_description():
    return("Adds asset to iris")