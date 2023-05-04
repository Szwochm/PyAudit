import os
import json

def init_config_file():
    config_file = "pyauditconfig.json"
    print("Searching for pyauditconfig.json file...")
    
    # Check if the config file exists
    if os.path.isfile(config_file):
        # Config file exists, read the installedappspath field
        with open(config_file, "r") as f:
            config_data = json.load(f)
            installedappspath = config_data.get("installedappspath")
    else:
        # Config file does not exist, create a new one with default values
        print("pyauditconfig.json not found, creating config file...")
        installedappspath = os.getcwd()
        config_data = {"installedappspath": installedappspath}
        with open(config_file, "w") as f:
            json.dump(config_data, f)
    
    print("Installed apps path:", installedappspath)