#  PyAudit: This program allows you to audit various aspects of your workstation all from one simple command line tool.
#  Made and tested on  Windows [Version 10.0.19044.2486]
#  Author: Szwochm

import wmi
import datetime


#Updated on command_getapps()
installed_apps = []

#
# sort_apps(List apps)
# helper function used by command_getapps() and import_apps
# Takes a list of apps and sorts them by name
#
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

#
# command_dne()
# called when an invalid (does not exit) command is attempted
# prints an error message to the console
# shows a help menu
#
def command_dne(userInput):
    commandNotValidMessage = f"""\n\n
    Error: The command you attempted \"{userInput}\" was not a valid command. Showing help menu.
    """
    print(commandNotValidMessage)
    command_help()
#
# command_help()
# prints a message displaying possible commands and their purpose
#
def command_help():
    helpMessage = """
    Help -

    help :- Show this help text
    apps -init :- Sends wmi query to Windows to get all installed applications and their versions. (This may take a while!)
    apps -c :- returns number of installed applications. \"apps -init\" must be run first!
    apps -l :- returns apps with their index, name, and version \"apps -init\" must be run first!
    apps -import :- attempts to import csv file and put into application database. Warning only checks that file is csv file and exists!
    sort - test should be removed.
    services :- list all running services (not implemented)

    """
    print(helpMessage)

#
# process_Input()
# Takes a string userInput and then executes a function based on what string was passed by the user.
#
def process_Input(userInput):
    if userInput == "help":
        command_help()

    elif userInput == "apps -init":
        command_getapps()
    elif userInput == "apps -c":
        command_countapps()
    elif userInput == "apps -l":
        command_listapps()
    elif userInput == "apps -import":
        import_apps()
    else:
        command_dne(userInput)

# main()
# Manages the shell
def main():
    exit = ["q","quit", "exit"]

    # Enter shell loop
    is_running = True
    userInput = None
    while(is_running):
        userInput = input("> ")
        if userInput in exit:
            return
        else:
            process_Input(userInput)
        
    
    


if __name__ == "__main__":
    main()