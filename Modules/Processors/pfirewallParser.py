import os
import requests
from zipfile import ZipFile 
import subprocess
import pandas 

def execute(config):
    #open all files on \Windows\System32\LogFiles\Firewall
    #check if files already parsed
    if os.path.isfile(config["drive_path"]+"\\CSVs\\pfirewall.csv"):
        return()
    #create new df
    df=pandas.DataFrame(columns=["date","time","action","protocol","src-ip","dst-ip","src-port","dst-port","size","tcpflags","tcpsyn","tcpack","tcpwin","icmptype","icmpcode","info","path","pid"])
    #iterate all files
    try:
        for file in os.listdir(config["drive_path"]+"\\Windows\\System32\\LogFiles\\Firewall"):
            #open file
            with open(config["drive_path"]+"\\Windows\\System32\\LogFiles\\Firewall\\"+file, "r") as f:
                #read line by line
                for line in f:
                    #split line
                    line=line.split()
                    #check if line is valid
                    if len(line)==18:
                        #append line to df append does not exist
                        df.loc[len(df.index)]=line
        #from the df group by ip,dest_port,protocol,action and count
        df_summary = df.groupby(["src-ip", "dst-ip", "dst-port", "protocol", "action"]).agg({
            "date": ["min", "max"],
            "size": "count"
        }).reset_index()
        df_summary.columns = ["src-ip", "dst-ip", "dst-port", "protocol", "action", "first-seen-date", "last-seen-date", "first-seen-time", "last-seen-time", "count"]
        #save df_summary to csv
        df_summary.to_csv(config["drive_path"]+"\\CSVs\\pfirewallStats.csv")
        #save df to csv
        df.to_csv(config["drive_path"]+"\\CSVs\\pfirewall.csv") 
    except:
        pass
def get_dependencies():
    return([])

def get_outputs():
    return(["pfirewallStats.csv"])

def get_type():
    return("machine_module")

def get_name():
    return("pfirewallParser")

def get_machine_type():
    return("windows")

def get_description():
    return("Extract all the logs from the windows firewall logs and store them in a sqlite DB and extracts the statistics by src_ip")