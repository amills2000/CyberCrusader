import pandas as pd
import os, glob

def join_excel(in_path):
    path=os.path.join(in_path, "CSVs")
    writer = pd.ExcelWriter(os.path.join(in_path, "Excel.xlsx"), engine = 'xlsxwriter')
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