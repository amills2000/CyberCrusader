import subprocess
import os
import pandas as pd

CONNECT_EVENT_ID="25"
DISCONECT_EVENT_ID="24"
TIMESTAMP_POS=0
DETECTIONS_POS=1
EVENT_ID_POS=2
COMPUTER_POS=3
IP_ADDRESS_POS=4
USERNAME_POS=5
PROVIDER_POS=6
LOGON_TYPE_POS=7
RECORD_ID_POS=8
DOMAIN_POS=9


def parse_rdp_attacks(path):
    #read the rdp_attacks.csv file line by line
    df=pd.DataFrame(columns=["initial_timestamp", "end_timestamp", "source_hostname", "source_ip", "destination", "user"])
    with open(path, "r") as f:
        #create a dataframe to store the initial_timestamp, end_timespamp, source_hostname, source_ip, destination, user
        prev_line=[]
        prev_id=""
        first_line=True
        for line in f:
            #skip first line
            if first_line:
                first_line=False
                continue
            splited_line=line.strip().split(",")
            #print(prev_line)
            #print(splited_line)
            #check if the event is a connection event
            if splited_line[EVENT_ID_POS]==CONNECT_EVENT_ID:
                #store previous line on df
                if len(prev_line)>0:
                    df_new_row = pd.DataFrame({
                        "initial_timestamp":prev_line[TIMESTAMP_POS],
                        "end_timestamp":"",
                        "source_hostname":prev_line[COMPUTER_POS],
                        "source_ip":prev_line[IP_ADDRESS_POS],
                        "destination":splited_line[COMPUTER_POS],
                        "user":prev_line[USERNAME_POS]
                    }, index=[0])
                    df=pd.concat([df, df_new_row], ignore_index=True)
                prev_line=splited_line
                prev_id=splited_line[EVENT_ID_POS]
            elif splited_line[EVENT_ID_POS]==DISCONECT_EVENT_ID:
                if prev_id==CONNECT_EVENT_ID and prev_line[USERNAME_POS]==splited_line[USERNAME_POS]:
                    df_new_row = pd.DataFrame({
                        "initial_timestamp":prev_line[TIMESTAMP_POS],
                        "end_timestamp":splited_line[TIMESTAMP_POS],
                        "source_hostname":prev_line[COMPUTER_POS],
                        "source_ip":prev_line[IP_ADDRESS_POS],
                        "destination":splited_line[COMPUTER_POS],
                        "user":prev_line[USERNAME_POS]
                    }, index=[0])
                    df=pd.concat([df, df_new_row], ignore_index=True)
                    prev_line=[]
                    prev_id=""
                else:
                    df_new_row = pd.DataFrame({
                        "initial_timestamp":"",
                        "end_timestamp":splited_line[TIMESTAMP_POS],
                        "source_hostname":splited_line[COMPUTER_POS],
                        "source_ip":splited_line[IP_ADDRESS_POS],
                        "destination":splited_line[COMPUTER_POS],
                        "user":splited_line[USERNAME_POS]
                    }, index=[0])
                    df=pd.concat([df, df_new_row], ignore_index=True)
                    prev_line=[]
                    prev_id=""
        #store the last line
        if len(prev_line)>0 and prev_id==CONNECT_EVENT_ID:
            df_new_row = pd.DataFrame({
                "initial_timestamp":prev_line[TIMESTAMP_POS],
                "end_timestamp":"",
                "source_hostname":prev_line[COMPUTER_POS],
                "source_ip":prev_line[IP_ADDRESS_POS],
                "destination":splited_line[COMPUTER_POS],
                "user":prev_line[USERNAME_POS]
            }, index=[0])
            df=pd.concat([df, df_new_row], ignore_index=True)
        elif len(prev_line)>0 and prev_id==DISCONECT_EVENT_ID:
            df_new_row = pd.DataFrame({
                "initial_timestamp":"",
                "end_timestamp":prev_line[TIMESTAMP_POS],
                "source_hostname":prev_line[COMPUTER_POS],
                "source_ip":prev_line[IP_ADDRESS_POS],
                "destination":splited_line[COMPUTER_POS],
                "user":prev_line[USERNAME_POS]
            }, index=[0])
            df=pd.concat([df, df_new_row], ignore_index=True)
    return(df) 

def execute(home,machines):
    #iterate all windows machines and look for rdp_attacks.csv files
    #create a dataframe to store the initial_timestamp, end_timespamp, source_hostname, source_ip, destination, user
    df=pd.DataFrame(columns=["initial_timestamp", "end_timestamp", "source_hostname", "source_ip", "destination", "user"])
    for machine in machines:
        #check if the machine has a rdp_attacks.csv file
        for path in machines[machine]:
            if os.path.isfile(path+"\\CSVs\\rdp_attacks.csv"):
                #read the file and append it to the dataframe
                df = pd.concat([df, parse_rdp_attacks(path+"\\CSVs\\rdp_attacks.csv")])
    #store the dataframe to csv and json
    df.to_csv(home+".\\merged_results\\CSVs\\rdp_timeline.csv", index=False)

def get_dependencies():
    return(["ALL"])

def get_outputs():
    return(["machine"])

def get_type():
    return("merger_module")

def get_name():
    return("RDP_aggregator")

def get_machine_type():
    return("windows")

def get_description():
    return("Uses the output of the RDP rule of chainsaw to aggregate the information of the RDP sessions")