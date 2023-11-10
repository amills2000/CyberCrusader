import glob
import pandas as pd
import os
import sqlite3

def execute(config):
    machine=config["machine_name"]
    in_path=config["drive_path"]
    path=os.path.join(in_path, "CSVs")
    conn = sqlite3.connect(os.path.join(in_path, machine+".db"))
    for filename in glob.glob(os.path.join(path, "*.csv")):
        try:
            if (filename.split("\\")[-1]=="services.csv") or filename.split("\\")[-1]=="MFT.csv":
                read_file = pd.read_csv(os.path.join(path, filename),sep="|")
                read_file.to_sql(name=filename.split("\\")[-1].split(".")[0][:31], con=conn)
            else: 
                read_file = pd.read_csv(os.path.join(path, filename))
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
    return(["windows","linux"])

def get_description():
    return("Adds all small/medium sized csv to excel file")
