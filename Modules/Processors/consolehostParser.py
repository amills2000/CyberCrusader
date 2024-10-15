import os

def execute(config):
    ConsoleHostHistory="Command,user"
    #iterate all users 
    for user in os.listdir(config["drive_path"]+"\\Users"):
        #check if AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt exists
        if not os.path.isfile(config["drive_path"]+"\\Users\\"+user+"\\AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\PSReadline\\ConsoleHost_history.txt"):
            continue
        #read lines from file and add to ConsoleHostHistory
        with open(config["drive_path"]+"\\Users\\"+user+"\\AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\PSReadline\\ConsoleHost_history.txt", "r") as f:
            for line in f:
                #quote line if it contains comma
                if "," in line:
                    line="\""+line+"\""
                ConsoleHostHistory+=line+","+user+"\n"
    #write ConsoleHostHistory to file if more than header
    if len(ConsoleHostHistory)>len("Command,user"):
        with open(config["drive_path"]+"\\CSVs\\consolehost.csv", "w") as f:
            f.write(ConsoleHostHistory)


def get_dependencies():
    return([])

def get_outputs():
    return([("consolehost.csv","consolehost")])

def get_type():
    return("machine_module")

def get_name():
    return("consolehostParser")

def get_machine_type():
    return("windows")

def get_description():
    return("stores all commands executed in the consolehost_history.txt file by user")