import py7zr
import os


def execute(path):
    print("Extracting "+path)
    extract_path=os.path.join(path.split(".")[0])
    if os.path.isdir(extract_path):
        return(extract_path)
    with py7zr.SevenZipFile(path, mode='r') as z_ref:
        failes_extractions=""
        try:
            z_ref.extractall(path=extract_path)
        except Exception as e:
            failes_extractions=failes_extractions+str(e)+"\n"
        if len(failes_extractions)>0:
            with open(os.path.join(extract_path,"failed extractions.txt"), "w") as file1:
                file1.writelines(failes_extractions)
        return(extract_path)

def get_dependencies():
    return([".7z"])

def get_outputs():
    return(["extracted"])

def get_type():
    return("extractor_module")

def get_name():
    return("7z_extractor")

def get_description():
    return("Extracts 7z files")
