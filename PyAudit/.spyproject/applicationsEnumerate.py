# applicationsEnumerate.py
# all application enumeration logic will be here.

import sys
try:
    import wmi
except ImportError:
    print("The 'wmi' module is not installed. Please run 'pip install wmi' to install it.")
    sys.exit()

try:
    import datetime
except ImportError:
    print("The 'datetime' module is not installed. Please run 'pip install datetime' to install it.")
    sys.exit()
    
    
def sort_apps():
    global installed_apps
    installed_apps = sorted(installed_apps, key=lambda x: x[0])

#
# command_countapps()
# check to see if you installed_apps array has entries. Prints error message if empty otherwise prints number of applications 
#
def command_countapps():
    global installed_apps
    if not installed_apps:
        print("Installed apps empty! Try running \"apps -init\" or \"apps -import\" ?")
        return 0
    else:
        numApps = len(installed_apps)
        s = f"You have {numApps} applications installed!"
        print(s)
        return numApps

#
# command_listapps()
# list all applications by their index values. apps -init must be run first! Does not use wmi queries so should be faster
#
def command_listapps():
    global installed_apps
    numApps = command_countapps()

    #if numApps returns 0, command_countapps will print out an error for the user
    if numApps == 0:
        return
    counter = 0
    for app in installed_apps:
        s = f" {counter}: {app[0]}, {app[1]} "
        print(s)
        counter += 1
    


def import_apps():
    global installed_apps
    if(command_countapps != 0):
        while (1):
            warningInput = input("Warning, app database is not empty, if you proceed existing database will be deleted. Proceed? (y/N)")
            if warningInput == "y" or warningInput == "Y":
                break
            elif warningInput == "n" or warningInput == "N":
                return
            else:
                print("Not a valid entry, please enter y or n")
    filename = input('Enter filename:')
            
    if not filename.endswith(".csv"):
        print("Error: The file {} is not a CSV file.".format(filename))
        return []

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: The file {} does not exist.".format(filename))
        return []

    installed_apps = []
    for line in lines:
        app, version = line.strip().split(",")
        installed_apps.append((app, version))
    sort_apps()
    return installed_apps

#
# command_getapps()
#  Uses wmi query to show every installed application and version on windows.
#  Microsoft plans to depreciate wmi in the future.
#  saves apps to a textfile and to a list for future use
#       
def command_getapps():
    global installed_apps

    #Clear out the old list
    installed_apps = []
    c = wmi.WMI()
    for app in c.Win32_Product():
     if app.Name:
        installed_apps.append((app.Name, app.Version))

    sort_apps()

    # Get the current date and time
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")


    # Save the list to a CSV file with a timestamp in the name
    # Print app,version to console

    filename = "installed_apps_{}.csv".format(timestamp)
    with open(filename, "w") as f:
        for app, version in installed_apps:
            line = "{}, Version: {}".format(app, version)
            print(line)
            f.write("{}\n".format(line))