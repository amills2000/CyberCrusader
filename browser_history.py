import os
import sqlite3 
import csv 

def get_allbrowser_data_by_user(root_folder):
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
            if os.path.exists(history_paths):
                print("found:",history_paths)
                conn = sqlite3.connect(history_paths)
                conn.text_factory = str 
                cur = conn.cursor()
                for query in browsers[browser]["sqlite_queries"]:
                    data = cur.execute(browsers[browser]["sqlite_queries"][query])
                    data_got= cur.fetchall()
                    if(len(data_got)>0):
                        with open(os.path.join(root_folder,"CSVs",user+"_"+browser+"_"+query+".csv"), 'w', newline='', encoding="utf-8") as f:
                            writer = csv.writer(f)
                            writer.writerow(list(map(lambda x: x[0], data.description)))
                            writer.writerows(data_got)
                conn.close