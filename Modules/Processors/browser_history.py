import os
import sqlite3 
import csv 

def get_chromiumbrowser_data_by_user(root_folder):
    browsers={
        "Chrome":{
            "history_path":"\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History",
            "sqlite_queries":{
                "history":"SELECT * FROM urls",
                "downloads":"SELECT * FROM downloads"
            }
        },
        "edge":{
            "history_path":"\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History",
            "sqlite_queries":{
                "history":"SELECT * FROM urls",
                "downloads":"SELECT * FROM downloads"
            }
        }
    }
    users_folder=os.listdir(os.path.join(root_folder,"Users"))
    for user in users_folder:
        #extract chrome data
        for browser in browsers:
            history_paths=os.path.join(root_folder,"Users",user)+browsers[browser]["history_path"]
            try:
                if os.path.exists(history_paths):
                    conn = sqlite3.connect(history_paths)
                    conn.text_factory = str 
                    cur = conn.cursor()
                    for query in browsers[browser]["sqlite_queries"]:
                        data = cur.execute(browsers[browser]["sqlite_queries"][query])
                        data_got= cur.fetchall()
                        #add columns to data_got user + browser + query
                        data_got = list(map(lambda x: (user,browser,query)+x, data_got))
                        headers=list(map(lambda x: x[0], data.description))
                        #add extra headers
                        headers=["user","browser","query"]+headers
                        if(len(data_got)>0):
                            with open(os.path.join(root_folder,"CSVs","browserhistory_"+query+".csv"), 'w', newline='', encoding="utf-8") as f:
                                writer = csv.writer(f)
                                writer.writerow(headers)
                                writer.writerows(data_got)
                    conn.close
            except Exception as e:
                pass

def execute(config):
    get_chromiumbrowser_data_by_user(config["drive_path"])

def get_dependencies():
    return()

def get_outputs():
    return([("browserhistory_history.csv","browser_history"),("browserhistory_downloads.csv","browser_history")])

def get_type():
    return("machine_module")

def get_name():
    return("browser_history")

def get_machine_type():
    return("windows")

def get_description():
    return("parses browser history")
