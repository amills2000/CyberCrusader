import os
import argparse
import importlib
import traceback

# TERMINAL COLORS!

BOLD = "\033[1m"
NOCOLOR = "\033[0m"
HEADER = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
UNDERLINE ='\033[4m'


# ARGUMENTS

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help = "Triage path", required=False)
parser.add_argument("-m", "--modules", help = "list all modules", required=False, action='store_true')
args = parser.parse_args()

print(f'''\
  _________        ___ 
  \_   ___ \___ __ \_ |__   ___________
  /    \  \<   |  | | __ \_/ __ \_  __ \\
  \     \___\___  | | \_\ \  ___/|  | \/     version 0.1a
   \______  / ____| |___  /\___  >__|
          \/\/          \/     \/
  _________                                   ___
  \_   ___ \_______ __ __  ___________     __| _/___________
  /    \  \/\_  __ \  |  \/  ___/\__  \   / __ |/ __ \_  __ \\
  \     \____|  | \/  |  /\___ \  / __ \_/ /_/ \  ___/|  | \/
   \______  /|__|  |____//____  >(____  /\____ |\___  >__|
          \/                  \/      \/      \/    \/
''')

# Define the directory where Triages are located
dir_path=args.path

modules={}

root="./Modules"

# Ensure ANSI/VT100 Escape Codes are properly virtualized
os.system('') # This sets Console Mode to Enable Virtual Terminal processing

# Create tools folder if it does not exist
if not os.path.isdir(os.path.join(root,"tools")):
    print(f"{CYAN}[+] Create tools directory...{NOCOLOR}")
    os.mkdir(os.path.join(root,"tools"))

# Create a dictionary of machine modules based on the value of the get_machine_type where machine type can have multiple values
machine_modules={}

print(f"{CYAN}[+] Importing Modules...{NOCOLOR}")

# Dynamically import the Modules
for dir in os.listdir("./Modules"):
    if dir.startswith("__") or dir=="tools" or not os.path.isdir(os.path.join(root,dir)):
        continue
    for file in os.listdir(os.path.join(root,dir)):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = os.path.basename(file)[:-3]
            module = importlib.import_module("Modules."+dir+"."+module_name)
            module_type=module.get_type() # get the module type
            module_dependencies=module.get_dependencies() # get the module dependencies
            module_outputs=module.get_outputs() # get the module outputs

            # iterate over dependecies and add the module to the dictionary with the dependency as key inside the apropiate type
            for dependency in module_dependencies:
                if module_type in modules:
                    if dependency in modules[module_type]:
                        modules[module_type][dependency].append(module)
                    else:
                        modules[module_type][dependency]=[module]
                else:
                    modules[module_type]={dependency:[module]}

            if module_type == "machine_module":
                module_dependencies=module.get_dependencies() # get the module dependencies
                module_outputs=module.get_outputs() # get the module outputs
                module_machine_type=module.get_machine_type() # get the module machine type

                # iterate over dependecies and add the module to the dictionary with the dependency as key inside the apropiate type
                if type(module_machine_type) is not list:
                    module_machine_type=[module_machine_type]
                for machine_type in module_machine_type:
                    if machine_type in machine_modules:
                        machine_modules[machine_type].append(module)
                    else:
                        machine_modules[machine_type]=[module]

if args.modules:
    print(f"{CYAN}[+] Modules:{NOCOLOR}")
    for module_type in modules:
        print("\tType: "+module_type)
        for dependency in modules[module_type]:
            print("\t * Dependency: "+dependency)
            for module in modules[module_type][dependency]:
                print("\t    - "+module.get_name()+": "+module.get_description())
    print("\tType: Machine Modules:")
    for machine_type in machine_modules:
        print("\t * Machine Type: "+machine_type)
        for module in machine_modules[machine_type]:
            print("\t    - "+module.get_name()+": "+module.get_description())
    exit(0)

if not dir_path:
    print(f"{RED}[!] Please provide a triage path.{NOCOLOR}")
    exit(1)

def execute_extractor_modules(dir_path,modules):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path=os.path.join(root,file)
            file_extension=os.path.splitext(file_path)[1]
            if file_extension in modules["extractor_module"]:
                # exclude files in recycle bin folder
                if "Recycle.Bin" in file_path:
                    continue
                for module in modules["extractor_module"][file_extension]:
                    execute_extractor_modules(module.execute(file_path),modules)
        for dir in dirs:
            execute_extractor_modules(dir,modules)

execute_extractor_modules(dir_path,modules)

# Execute all the machine finder modules and store the machines and their paths in a dictionary 
# each module will return an array of tuples comntaining the machine name the type and its path

print(f"{CYAN}[+] Searching for machines...{NOCOLOR}")

machines={}
for module in modules["machine_finders"]["triage_path"]:
    for machine in module.execute(dir_path):
        if module.get_machine_type() in machines:
            if machine[0] in machines[module.get_machine_type()]:
                machines[module.get_machine_type()][machine[0]].append(machine[1])
            else:
                machines[module.get_machine_type()][machine[0]]=[machine[1]]
        else:
            machines[module.get_machine_type()]={machine[0]:[machine[1]]}

# Print all found machines
print(f"{GREEN}[+] Machines found:{NOCOLOR}")
for machine_type in machines:
    for machine in machines[machine_type]:
        print(f" * {BLUE}({machine_type}){NOCOLOR} {BOLD}{YELLOW}{machine}{NOCOLOR} at '"+str("', '".join(machines[machine_type][machine]))+"'")

def topological_sort(modules):
    visited = set()
    sorted_modules = []

    def dfs(module):
        visited.add(module)
        dependencies = module.get_dependencies()
        for dependency_name in dependencies:
            dependency = next((mod for mod in modules if mod.get_name() == dependency_name), None)
            if dependency and dependency not in visited:
                dfs(dependency)
        sorted_modules.append(module)

    for module in modules:
        if module not in visited:
            dfs(module)

    return sorted_modules

sorted_modules={}
for type in machine_modules:
    sorted_modules[type]=topological_sort(machine_modules[type])
    for module in sorted_modules[type]:
        # if dependency is "ALL" put module at the end of the list
        if "ALL" in module.get_dependencies():
            sorted_modules[type].remove(module)
            sorted_modules[type].append(module)

# Iterate over the machines and execute the modules in the correct order
for machine_type in machines:
    print(f"{CYAN}[+] Executing modules for all {machine_type} machines...{NOCOLOR}")
    for machine_name in machines[machine_type]:
        for machine_path in machines[machine_type][machine_name]:
            #creating output folders
            if not os.path.isdir(os.path.join(machine_path,"CSVs")):
                os.mkdir(os.path.join(machine_path,"CSVs"))
            if not os.path.isdir(os.path.join(machine_path,"JSONs")):
                os.mkdir(os.path.join(machine_path,"JSONs"))
            if not os.path.isdir(os.path.join(machine_path,"TXTs")):
                os.mkdir(os.path.join(machine_path,"TXTs"))
            print(f"[+] Executing modules for '{machine_name}' at '{machine_path}'.")
            for module in sorted_modules[machine_type]:
                print(f"{GREEN} * Executing module {module.get_name()}{NOCOLOR}")
                try:
                    module.execute({"drive_path":machine_path,"machine_name":machine_name})
                except Exception as e:
                    print(f"{RED}   => Error on module "+module.get_name()+": "+str(e)+NOCOLOR)
                    print(traceback.print_exception(e))
                    continue
