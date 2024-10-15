import utmp
import os

def execute(config):
    res="time,type,pid,line,id,user,host,exit0,exit1,session,sec,usec,addr0,addr1,addr2,addr3,unused\n"
    # parse the wtmp file and save it to csv
    if os.path.isfile(config["drive_path"]+"\\CSVs\\parsed_wtmp.csv"):
        return()
    # open the file

    root_path=config["drive_path"]
    with open(root_path+"\\var\\log\\wtmp", 'rb') as fd:
        buf = fd.read()
        for entry in utmp.read(buf):
            res+=str(entry.time)+","+str(entry.type)+","+str(entry.pid)+","+str(entry.line)+","+str(entry.id)+","+str(entry.user)+","+str(entry.host)+","+str(entry.exit0)+","+str(entry.exit1)+","+str(entry.session)+","+str(entry.sec)+","+str(entry.usec)+","+str(entry.addr0)+","+str(entry.addr1)+","+str(entry.addr2)+","+str(entry.addr3)+","+str(entry.unused)+"\n"
    # save the csv
    with open(config["drive_path"]+"\\CSVs\\parsed_wtmp.csv", "w") as file1:
        file1.write(res)
def get_dependencies():
    return([])

def get_outputs():
    return([("parsed_wtmp.csv","parsed_wtmp")])

def get_type():
    return("machine_module")

def get_name():
    return("parse_wtmp_linux")

def get_machine_type():
    return(["linux"])

def get_description():
    return("Parses the wtmp file")
