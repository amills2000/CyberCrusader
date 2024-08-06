import os
def execute(config):
    #check if module already runned on this machine
    if os.path.isfile(config["drive_path"]+"\\CSVs\\linux_bash_history.csv"):
        return()
    #extract the bash history of each user and store it on a csv file with user,command
    if config["machine_type"]=="uac_linux":
        root_path=config["drive_path"]+"\\[root]"
    else:
        root_path=config["drive_path"]
    bash_history="user,command\n"
    #iterate all home directories
    for path in os.listdir(root_path+"\\home"):
        #check if the user has a .bash_history file
        if not os.path.isfile(root_path+"\\home\\"+path+"\\.bash_history"):
            continue
        #iterate the file and extract the commands
        try:
            with open(root_path+"\\home\\"+path+"\\.bash_history", "r") as f:
                for line in f:
                    bash_history+=path+","+line.strip()+"\n"
        except:
            pass
    #save the bash history to a csv
    with open(config["drive_path"]+"\\CSVs\\linux_bash_history.csv", "w") as f:
        f.write(bash_history)


def get_dependencies():
    return([])

def get_outputs():
    return(["linux_bash_history"])

def get_type():
    return("machine_module")

def get_name():
    return("get_linux_bash_history")

def get_machine_type():
    return(["linux","uac_linux"])

def get_description():
    return("Extracts linux bash history and its information")
