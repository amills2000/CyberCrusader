import pandas as pd
import os
import json

def flatten_json(y):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + ': ')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + ': ')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    return out

def execute(config):
    out="Machine Name: "+config["machine_name"]+"\n"
    out+="Machine Path: "+config["drive_path"]+"\n"
    # get the machine info from json \JSONs\\machine_info.json
    if os.path.isfile(config["drive_path"]+"\\JSONs\\machine_info.json"):
        mach_info_dict = json.load(open(config["drive_path"]+"\\JSONs\\machine_info.json", 'r'))
        flattened = flatten_json(mach_info_dict)
        df = pd.json_normalize(flattened)
        df = df.transpose()
        df = df.reset_index()
        df.columns = ['key', 'value']
        df = df.sort_values(by=['key'])
        df = df.reset_index()
        df = df.drop(columns=['index'])
        df.to_csv(config["drive_path"]+"\\CSVs\\machine_info.csv", index=False)
        out+="Machine Info:\n"
        out+=df.to_string(index=False)+"\n"
    #get number of real rows in sigma.csv
    df = pd.read_csv(config["drive_path"]+"\\CSVs\\sigma.csv")
    out+="Sigma Rules: "+str(len(df.index))+"\n"

    #save on root path
    with open(config["drive_path"]+"\\TXTs\\report.txt", "w") as file1:
        file1.write(out)

def get_dependencies():
    return(["all"])

def get_outputs():
    return([("report.txt","report")])

def get_type():
    return("machine_module")

def get_name():
    return("machine_infor_report_windows")

def get_machine_type():
    return("windows")

def get_description():
    return("Create a Txt report with the summary of the machine")
