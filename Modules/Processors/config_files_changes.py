import os

def compare_files(model, machine_file):
    with open(model, 'r') as f1, open(machine_file, 'r') as f2:
        set_model = set(line.strip() for line in f1)
        set_machine_file = set(line.strip() for line in f2)
    return (set_machine_file - set_model)
def execute(config):
    #get all available model files stored in the tools/linux_config_models
    model_files=os.listdir("./modules/tools/linux_config_models")
    #iterate recursively over the machine files and compare them with the model files if name matches
    #check if module already runned on this machine
    if os.path.isfile(config["drive_path"]+"\\CSVs\\linux_config_files.csv"):
        return()
    mismatched_files="file_path,value\n"
    for root, dirs, files in os.walk(config["drive_path"]):
        for file in files:
            if file in model_files:
                #compare the files and add the mismatched lines to the csv one line per mismatch
                mismatched_lines=compare_files("./modules/tools/linux_config_models/"+file, root+"\\"+file)
                for line in mismatched_lines:
                    mismatched_files+=root+"\\"+file+","+line+"\n"
                

    #save the mismatched files to a csv
    with open(config["drive_path"]+"\\CSVs\\linux_config_files.csv", "w") as f:
        f.write(mismatched_files)

def get_dependencies():
    return([])

def get_outputs():
    return(["linux_config_files"])

def get_type():
    return("machine_module")

def get_name():
    return("get_linux_config_files_mods")

def get_machine_type():
    return("linux")

def get_description():
    return("Compares linux config files with the model to check for modifications")
