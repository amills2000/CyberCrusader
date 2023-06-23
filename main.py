import pkgutil
import importlib

from zipfile import ZipFile 
import argparse
import os

import Modules

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help = "Triage path", required=False)
parser.add_argument("-m", "--modules", help = "list all modules", required=False, action='store_true')
args = parser.parse_args()

# define the directory where Triages are located
dir_path=args.path

modules={}

root="./Modules"

#create tools folder if it does not exist
if not os.path.isdir(os.path.join(root,"tools")):
    os.mkdir(os.path.join(root,"tools"))

# create a dictionary of machine modules based on the value of the get_machine_type where machine type can have multiple values
machine_modules={}
#import the modules in the folder
for dir in os.listdir("./Modules"):
    # import all modules in directory
    if dir.startswith("__") or dir=="tools" or not os.path.isdir(os.path.join(root,dir)):
        continue
    for file in os.listdir(os.path.join(root,dir)):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = os.path.basename(file)[:-3]
            module = importlib.import_module("Modules."+dir+"."+module_name)
            # get the module type
            module_type=module.get_type()
            # get the module dependencies
            module_dependencies=module.get_dependencies()
            # get the module outputs
            module_outputs=module.get_outputs()
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
                # get the module dependencies
                module_dependencies=module.get_dependencies()
                # get the module outputs
                module_outputs=module.get_outputs()
                # get the module machine type
                module_machine_type=module.get_machine_type()
                # iterate over dependecies and add the module to the dictionary with the dependency as key inside the apropiate type
                if type(module_machine_type) is not list:
                    module_machine_type=[module_machine_type]
                for machine_type in module_machine_type:
                    if machine_type in machine_modules:
                        machine_modules[machine_type].append(module)
                    else:
                        machine_modules[machine_type]=[module]

if args.modules:
    print("Modules:")
    for module_type in modules:
        print("\tType: "+module_type)
        for dependency in modules[module_type]:
            print("\t\tDependency: "+dependency)
            for module in modules[module_type][dependency]:
                print("\t\t\t"+module.get_name()+": "+module.get_description())
    print("\tType: Machine Modules:")
    for machine_type in machine_modules:
        print("\t\tMachine Type: "+machine_type)
        for module in machine_modules[machine_type]:
            print("\t\t\t"+module.get_name()+": "+module.get_description())

    exit()
if not dir_path:
    print("Please provide a triage path")
    exit()
def execute_extractor_modules(dir_path,modules):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path=os.path.join(root,file)
            file_extension=os.path.splitext(file_path)[1]
            if file_extension in modules["extractor_module"]:
                #exclude files in recycle bin folder
                if "Recycle.Bin" in file_path:
                    continue
                for module in modules["extractor_module"][file_extension]:
                    execute_extractor_modules(module.execute(file_path),modules)
        for dir in dirs:
            execute_extractor_modules(dir,modules)

execute_extractor_modules(dir_path,modules)

#execute all the machine finder modules and store the machines and their paths in a dictionary each module will return an array of tuples comntaining the machine name the type and its path
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

#iterate over the machines and execute the modules in the correct order
for machine_type in machines:
    print("Executing modules for all machines of type "+machine_type)
    for machine_name in machines[machine_type]:
        for machine_path in machines[machine_type][machine_name]:
            #creating output folders
            if not os.path.isdir(os.path.join(machine_path,"CSVs")):
                os.mkdir(os.path.join(machine_path,"CSVs"))
            if not os.path.isdir(os.path.join(machine_path,"JSONs")):
                os.mkdir(os.path.join(machine_path,"JSONs"))
            if not os.path.isdir(os.path.join(machine_path,"TXTs")):
                os.mkdir(os.path.join(machine_path,"TXTs"))
            print("Executing modules for machine "+machine_name+" in path "+machine_path)
            for module in sorted_modules[machine_type]:
                print("Executing module "+module.get_name())
                try:
                    module.execute({"drive_path":machine_path})
                except Exception as e:
                    print("Error on module "+module.get_name()+": "+str(e))
                    continue
                print("Module "+module.get_name()+" executed")
            print("Modules for machine "+machine_name+" in path "+machine_path+" executed")
        print("All modules executed for machine "+machine_name)
    print("All modules executed for all machines of type "+machine_type)

