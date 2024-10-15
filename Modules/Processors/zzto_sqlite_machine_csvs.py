import glob
import pandas as pd
import os
import sqlite3

def execute(config):
    machine=config["machine_name"]
    in_path=config["drive_path"]
    path=os.path.join(in_path, "CSVs")
    conn = sqlite3.connect(os.path.join(in_path, machine+".db"))
    for filename in os.listdir(path):
#   for filename in glob.glob(os.path.join(path, "*.csv")):
        if not filename.endswith(".csv"):
            continue
        filename=os.path.join(path, filename)
        try:
            if (filename.split("\\")[-1]=="services.csv") or filename.split("\\")[-1]=="MFT.csv":
                read_file = pd.read_csv(os.path.join(path, filename),sep="|", on_bad_lines='skip',low_memory=False)
                read_file.to_sql(name=filename.split("\\")[-1].split(".")[0][:31], con=conn)
            else: 
                read_file = pd.read_csv(os.path.join(path, filename), on_bad_lines='skip',low_memory=False)
                read_file.to_sql(name=filename.split("\\")[-1].split(".")[0][:31], con=conn)
        except Exception as e:
            pass
    conn.close()

def get_dependencies():
    return(["all"])

def get_outputs():
    return(["all.csv"])

def get_type():
    return("machine_module")

def get_name():
    return("to_sqlite_machine_csvs")

def get_machine_type():
    return(["windows","linux","uac_linux"])

def get_description():
    return("Adds all small/medium sized csv to excel file")
