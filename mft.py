import pandas as pd
import datetime as datetime

def search_exe(cylr_path):
    df = pd.read_csv(cylr_path+"\CSVs\MFT.csv",sep='|')
    # parse date
    df['date'] = pd.to_datetime(df['$FILENAME Creation Time'], format='%Y-%m-%d %H:%M:%S')
    ext="BAT,BIN,CMD,COM,CPL,EXE,GADGET,INF1,INS,INX,ISU,JOB,JSE,LNK,MSC,MSI,MSP,MST,PAF,PIF,PS1,REG,RGS,SCR,SCT,SHB,SHS,U3P,VB,VBE,VBS,VBSCRIPT,WS,WSF,WSH".replace(",","|")
    df=df[df.File.str.contains('\.(?:'+ext+')$', case=False)]
    df.to_csv(cylr_path+"\CSVs\MFT_vip_ext.csv")

def search_sring_mft(cylr_path,stringtosearch):
    df = pd.read_csv(cylr_path+"\CSVs\MFT.csv",sep='|')
    # parse date
    df['date'] = pd.to_datetime(df['$FILENAME Creation Time'], format='%Y-%m-%d %H:%M:%S')
    df=df[df.File.str.contains(stringtosearch, case=False)]
    if len(df)>0:
        print(cylr_path)
        df.to_csv(cylr_path+"\CSVs\MFT_search.csv")

def search_suspicious_strings(cylr_path):
    search=""
    with open("suspicious_tools.txt") as f:
        content = f.readlines()
        # Show the file contents line by line.
        # We added the comma to print single newlines and not double newlines.
        # This is because the lines contain the newline character '\n'.
        for line in content:
            search=search+line.strip()+"|"
    search=search.rstrip('|')
    print(search)
    df = pd.read_csv(cylr_path+"\CSVs\MFT.csv",sep='|')
    # parse date
    df['date'] = pd.to_datetime(df['$FILENAME Creation Time'], format='%Y-%m-%d %H:%M:%S')
    df=df[df.File.str.contains('(?:'+search+')', case=False)]
    if len(df)>0:
        print(cylr_path)
        df.to_csv(cylr_path+"\CSVs\MFT_suspicious_tools.csv")