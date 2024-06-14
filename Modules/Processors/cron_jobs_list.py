import os

def execute(config):
    #review all the possible cron files and extract the information from them into a csv
    # check if module already runned on this machine
    if os.path.isfile(config["drive_path"]+"\\CSVs\\linux_crons.csv"):
        return()
    crons="file,path,minute,hour,day,month,weekday,command\n"
    #read all files in /etc/cron.d
    try:
        for path in os.listdir(config["drive_path"]+"\\etc\\cron.d"):
            try:
                with open(config["drive_path"]+"\\etc\\cron.d\\"+path, "r") as f:
                    for line in f:
                        crons+=path+","+"\\etc\\cron.d\\"+path+","+",".join(line.split(" ")[:-1].strip())+line.split(" ")[-1]
            except:
                pass
    except:
        pass
    #read all files in /etc/crontab
    try:
        with open(config["drive_path"]+"\\etc\\crontab", "r") as f:
            for line in f:
                crons+="crontab,"+"\\etc\\crontab,"+",".join(line.split(" ")[:-1].strip())+line.split(" ")[-1]
    except:
        pass
    #read all files in /var/spool/cron/crontabs
    try:
        for path in os.listdir(config["drive_path"]+"\\var\\spool\\cron\\crontabs"):
            try:
                with open(config["drive_path"]+"\\var\\spool\\cron\\crontabs\\"+path, "r") as f:
                    for line in f:
                        crons+=path+","+"\\var\\spool\\cron\\crontabs\\"+path+","+",".join(line.split(" ")[:-1].strip())+line.split(" ")[-1]
            except:
                pass
    except:
        pass
    #read all files in /var/spool/cron/
    try:
        for path in os.listdir(config["drive_path"]+"\\var\\spool\\cron"):
            try:
                with open(config["drive_path"]+"\\var\\spool\\cron\\"+path, "r") as f:
                    for line in f:
                        crons+=path+","+"\\var\\spool\\cron\\"+path+","+",".join(line.split(" ")[:5])+","+" ".join(line.split(" ")[5:])
            except Exception as e:
                print(e)
                pass
    except:
        pass
    #get the files inside /etc/cron.*
    cron_trad={
        "daily":"0,8,*,*,*",
        "monthly":"0,8,1,*,*",
        "hourly":"0,*,*,*,*"
    }
    for path in os.listdir(config["drive_path"]+"\\etc"):
        if path.startswith("cron.") and os.path.isdir(config["drive_path"]+"\\etc\\"+path):
            #list files inside the folder
            for file in os.listdir(config["drive_path"]+"\\etc\\"+path):
                crons+=file+","+"\\etc\\"+path+"\\"+file+","+cron_trad[path.split(".")[1]]+",run "+"\\etc\\"+path+"\\"+file+"\n"

    #save the information to csv
    with open(config["drive_path"]+"\\CSVs\\linux_crons.csv", "w") as file1:
        file1.write(crons)





def get_dependencies():
    return([])

def get_outputs():
    return(["linux_crons"])

def get_type():
    return("machine_module")

def get_name():
    return("get_linux_crons")

def get_machine_type():
    return("linux")

def get_description():
    return("Extracts linux crons and its information")
