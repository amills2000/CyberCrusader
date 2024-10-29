import os
import pandas as pd


def execute(config):
    path=config["drive_path"]
    #load the Get-ProcessList
    try:
        df = pd.read_csv(os.path.join(path,"PWSH-Get-ProcessList.csv"))
    except:
        print("No Get-ProcessList.csv file found")
        return
    df = df.merge(df[['ProcessID', 'Name']], how='left', left_on='ParentProcessId', right_on='ProcessID', suffixes=('', '_Parent'))

    #store df as csv
    print(path)
    df.to_csv(os.path.join(path,"CSVs\Get-ProcessList_enriched.csv"),index=False)
            

def get_dependencies():
    return([])

def get_outputs():
    return([])

def get_type():
    return("machine_module")

def get_name():
    return("LiveResponseProcessList")

def get_machine_type():
    return("windows_live_response")

def get_description():
    return("Enriches the ProcessList file into a CSV file")


if __name__ == "__main__":
    config={"drive_path":r"Test path"}
    execute(config)