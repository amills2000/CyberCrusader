import os


def execute(config):
    path=config["drive_path"]
    #copy the scheduled_tasks
    os.system(f"copy {path}\\scheduled_tasks.csv {path}\\CSVs")       

def get_dependencies():
    return([])

def get_outputs():
    return([])

def get_type():
    return("machine_module")

def get_name():
    return("LiveResponseSheduledTasks")

def get_machine_type():
    return("windows_live_response")

def get_description():
    return("Copies the Scheduled Tasks file into a CSV file")


if __name__ == "__main__":
    config={"drive_path":r"path"}
    execute(config)