from zipfile import ZipFile 
import os


def execute(path):
    print("Extracting "+path)
    extract_path=os.path.join(path.split(".")[0])
    if os.path.isdir(extract_path):
        return(extract_path)
    with ZipFile(path, 'r') as zip_ref:
        failes_extractions=""
        for name in zip_ref.namelist():
            try:
                #if file is too big not extract
                if zip_ref.getinfo(name).file_size > 10000000000:
                    continue
                zip_ref.extract(name, extract_path)
            except Exception as e:
                failes_extractions=failes_extractions+"Extracting "+name+str(e)+"\n"
        if len(failes_extractions)>0:
            with open(os.path.join(extract_path,"failed extractions.txt"), "w") as file1:
                file1.writelines(failes_extractions)
        return(extract_path)

def get_dependencies():
    return([".zip"])

def get_outputs():
    return(["extracted"])

def get_type():
    return("extractor_module")

def get_name():
    return("zip_extractor")

def get_description():
    return("Extracts zip files")