import glob
import pandas as pd
import os

def execute(config):
    machine=config["machine_name"]
    in_path=config["drive_path"]
    print("join excel " + machine)
    path=os.path.join(in_path, "CSVs")
    writer = pd.ExcelWriter(os.path.join(in_path, machine+".xlsx"), engine = 'xlsxwriter')
    for filename in glob.glob(os.path.join(path, "*.csv")):
        try:
            if filename.split("\\")[-1]=="MFT.csv":
                continue
            if filename.split("\\")[-1]=="services.csv":
                read_file = pd.read_csv(os.path.join(path, filename),sep="|")
                read_file.to_excel(writer, sheet_name = filename.split("\\")[-1].split(".")[0][:31])
            else: 
                read_file = pd.read_csv(os.path.join(path, filename))
                read_file.to_excel(writer, sheet_name = filename.split("\\")[-1].split(".")[0][:31].replace(".","_"))
        except Exception as e:
            print(e)
    writer.close()

def get_dependencies():
    return(["all"])

def get_outputs():
    return(["all.csv"])

def get_type():
    return("machine_module")

def get_name():
    return("to_excel_machine_csvs")

def get_machine_type():
    return("windows")

def get_description():
    return("Adds all small/medium sized csv to excel file")
