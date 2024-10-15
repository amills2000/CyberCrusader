
import pandas as pd
import re
from ipaddress import IPv4Network

machine_info = {}

def get_hostname_info(extract_path):
    global machine_info 
    #get hostname from \live_response\network\hostname
    try:
        with open(extract_path+"\\live_response\\network\\hostname.txt", "r") as f:
            machine_info["hostname"]=f.read().strip()
    except:
        machine_info["hostname"]="Unknown"
    #get hostname full from \live_response\network\hostname_-f
    try:
        with open(extract_path+"\\live_response\\network\\hostname_-f.txt", "r") as f:
            machine_info["hostname_full"]=f.read().strip()
    except:
        machine_info["hostname_full"]="Unknown"

def get_inet_info(extract_path):
    global machine_info
    machine_info["interfaces"]=[]
    with open(extract_path+'\\live_response\\network\\ifconfig_-a.txt') as f:
    #read the file line by line storing each block on one variable where a block is separated by a blank line
        interface=["","",""]
        for line in f:
            #check if the line is not empty
            if line.startswith(' '):
                #append the line to the block
                interface[1]+=line
                continue
            elif line!="\n":
                interface[0]=line.split("      ")[0]
                interface[1]+=line.split("      ")[1]
                continue
            #append the block to the list of blocks
            #extract the ip and mask for each interface with regex
            ip=re.findall(r'inet addr:(\d+\.\d+\.\d+\.\d+)',interface[1])
            ip=ip[0]
            mask=re.findall(r'Mask:(\d+\.\d+\.\d+\.\d+)',interface[1])
            mask=mask[0]
            #convert mask format from xxx.xxx.xxx.xxx to /xx
            mask_cidr=IPv4Network('0.0.0.0/'+mask).prefixlen
            interface[2]=ip+"/"+str(mask_cidr)
            #store the interfaces in the machine_info dictionary
            machine_info["interfaces"].append((interface[0],interface[2]))
            interface=["","",""]

def get_listening_ports(extract_path):
    global machine_info
    #get the listening ports from \live_response\network\netstat_-lpeanut.txt
    machine_info["listening_ports"]=[]
    with open(extract_path+'\\live_response\\network\\netstat_-lpeanut.txt') as f:
        for line in f:
            if "tcp" in line:
                if "LISTEN" in line:
                    #exreact the port number with a regex for the first x.x.x.x:port
                    rex=re.findall(r'(\d+\.\d+\.\d+\.\d+:\d+)',line)
                    machine_info["listening_ports"].append("tcp\\"+rex[0])
            elif "udp" in line:
                if "LISTEN" in line:
                    print("LISTEN",line)
                    rex=re.findall(r'(\d+\.\d+\.\d+\.\d+:\d+)',line)
                    machine_info["listening_ports"].append("udp\\"+rex[0])

def get_disk_info(extract_path):
    global machine_info
    #get the disk information from \live_response\disk\df_-h.txt
    machine_info["disk"]=[]
    with open(extract_path+'\\live_response\\storage\\df_-h.txt') as f:
        #ignore first line
        f.readline()
        for line in f:
            line=line.split(" ")
            #extract the information
            disk={
                "filesystem":line[0],
                "size":line[1],
                "used":line[2],
                "avail":line[3],
                "use":line[4],
                "mounted":line[5]
            }
            machine_info["disk"].append(disk)

def get_uptime_info(extract_path):
    global machine_info
    #get the uptime information from \live_response\system\uptime.txt
    with open(extract_path+'\\live_response\\system\\uptime.txt') as f:
        line=f.readline().split(",")
        #extract the information
        machine_info["uptime"]=line[0]

def get_os_release_info(extract_path):
    global machine_info
    #get the os release info from /[ROOT]/etc/os-release
    with open(extract_path+'\\etc\\os-release') as f:
        for line in f:
            if "PRETTY_NAME" in line:
                machine_info["os"]=line.split("=")[1].strip().replace('"','')

def execute(config):
    extract_path=config["drive_path"]
    try:
        get_hostname_info(extract_path)
    except Exception as e:
        print (e)
    try:    
        get_inet_info(extract_path)
    except Exception as e:
        pass
    try:
        get_listening_ports(extract_path)
    except Exception as e:
        pass
    try:
        get_disk_info(extract_path)
    except Exception as e:
        print(e)
    try:
        get_uptime_info(extract_path)
    except Exception as e:
        pass
    try:
        get_os_release_info(extract_path)
    except Exception as e:
        pass
    #store the machine info in a json file
    with open(config["drive_path"]+"\\JSONs\\machineinfo.json", "w") as file1:
        file1.write(str(machine_info))
    #transform the machine info to a csv format 
    out="key,value\n"
    for key in machine_info:
        if type(machine_info[key])==list:
            i=0
            for item in machine_info[key]:
                if type(item)==dict:
                    #format json oneline 
                    out+=key+" "+str(i)+",\""+str(item).replace("{","").replace("}","").replace(",",";")+"\"\n"
                #check if tuple
                elif type(item)==tuple:
                    out+=key+" "+str(i)+",\""+str(item[0])+":"+str(item[1])+"\"\n"
                else:
                    out+=key+" "+str(i)+",\""+str(item)+"\"\n"
                i+=1
        else:
            out+=key+",\""+str(machine_info[key])+"\"\n"
    with open(config["drive_path"]+"\\CSVs\\machineinfo.csv", "w") as file1:
        file1.write(out)

def get_dependencies():
    return([])

def get_outputs():
    return([("machineinfo.json",None),("machineinfo.csv",None)])

def get_type():
    return("machine_module")

def get_name():
    return("UAC_MachineInfo")

def get_machine_type():
    return("uac_linux")

def get_description():
    return("Parses the machine file into a json file")