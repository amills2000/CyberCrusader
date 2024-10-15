import glob
import pandas as pd
import os


def detect_csv_separator(filename,sample_size=1024):
    potential_delimiters = [',', '\t','|']  # Common CSV delimiters to check
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
    #list all files on firectory 
    for filename in os.listdir(path):
#   for filename in glob.glob(os.path.join(path, "*.csv")):
        if not filename.endswith(".csv"):
            continue
        try:
            filename=os.path.join(path, filename)
            # join if csv is not too big for excel
            #get number of lines
            num_lines = sum(1 for line in open(filename))
            #if os.path.getsize(filename) > 10000000:
            #    continue
            if num_lines > 1000000:
                continue
            separator = detect_csv_separator(filename)
            df = pd.read_csv(filename, sep=separator, on_bad_lines='skip',low_memory=False,skip_blank_lines=True,encoding='utf-8')
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
    return(["windows","linux","uac_linux"])

def get_description():
    return("Adds all small/medium sized csv to excel file")
