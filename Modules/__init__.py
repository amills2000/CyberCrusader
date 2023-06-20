import os
import glob


# Get a list of all Python module files in the current directory
#module_files = glob.glob(os.path.join(os.path.dirname(__file__), "./*/*.py"))

# Exclude the "__init__.py" file itself
#module_files = [f for f in module_files if not f.endswith("__init__.py")]

#print(module_files)

# Import all modules
#for module_file in module_files:
#    module_name = os.path.basename(module_file)[:-3]  # Remove the ".py" extension
#    __import__(module_name, globals(), locals(), level=1)
    
