import glob
import pandas as pd
import os
from io import StringIO

def detect_csv_separator(filename,sample_size=1024):
    potential_delimiters = [',', '\t', ';','|']  # Common CSV delimiters to check
    delimiter_count = {}

    with open(filename, 'r') as file:
        sample = file.read(sample_size)

    for delimiter in potential_delimiters:
        delimiter_count[delimiter] = sample.count(delimiter)

    most_common_delimiter = max(delimiter_count, key=delimiter_count.get)
    return most_common_delimiter

def execute(config):
    machine=config["machine_name"]
    in_path=config["drive_path"]
    path=os.path.join(in_path, "CSVs")
    writer = pd.ExcelWriter(os.path.join(in_path, machine+".xlsx"), engine = 'xlsxwriter')
    for filename in glob.glob(os.path.join(path, "*.csv")):
        try:
            # join if csv is not too big for excel
            if os.path.getsize(filename) > 10000000:
                continue
            separator = detect_csv_separator(filename)
            df = pd.read_csv(filename, sep=separator)
            #if only headers continue
            if len(df) < 2:
                continue
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
