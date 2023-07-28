import glob
import pandas as pd
import os

def detect_csv_separator(filename):
    with open(filename, 'r') as file:
        # Read a sample of the file
        sample = file.read(1024)  # Adjust the sample size as needed

    # Use pandas to sniff the delimiter
    sniffer = pd.read_csv(pd.compat.StringIO(sample), delimiter=None)
    separator = sniffer._sep

    return separator

def execute(config):
    machine=config["machine_name"]
    in_path=config["drive_path"]
    print("join excel " + machine)
    path=os.path.join(in_path, "CSVs")
    writer = pd.ExcelWriter(os.path.join(in_path, machine+".xlsx"), engine = 'xlsxwriter')
    for filename in glob.glob(os.path.join(path, "*.csv")):
        try:
            # join if csv is not too big for excel
            if os.path.getsize(filename) > 10000000:
                continue
            separator = detect_csv_separator(filename)
            df = pd.read_csv(filename, sep=separator)
            df.to_excel(writer, sheet_name=os.path.basename(filename).split(".")[0], index=False)
            
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
