#  PyAudit: This program allows you to audit various aspects of your workstation all from one simple command line tool.
#  Made and tested on  Windows [Version 10.0.19044.2486]
#  Author: Szwochm
import sys
import os
import tkinter as tk
from tkinter import filedialog
import initconfig as init

# contains all application enumeration functions
import applicationsEnumerate as app

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
    



#Updated on command_getapps()
installed_apps = []

#
# sort_apps(List apps)
# helper function used by command_getapps() and import_apps
# Takes a list of apps and sorts them by name
#


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
    services :- list all running services (not implemented)

    """
    print(helpMessage)

def command_setInstalledAppsDirectory():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    return directory
#
# process_Input()
# Takes a string userInput and then executes a function based on what string was passed by the user.
#
def process_Input(userInput):
    if userInput == "help":
        command_help()

    elif userInput == "apps -init":
        app.command_getapps()
    elif userInput == "apps -c":
        app.command_countapps()
    elif userInput == "apps -l":
        app.command_listapps()
    elif userInput == "apps -import":
        app.import_apps()
        
    elif userInput == "apps setPath":
        d = command_setInstalledAppsDirectory()
        print("Selected path" + d)
    else:
        command_dne(userInput)

# main()
# Manages the shell
def main():
    exit = ["q","quit", "exit"]
    banner = """
█▀█ █▄█ ▄▀█ █░█ █▀▄ █ ▀█▀   ▄▄   █░█░█ █ █▄░█ █▀▄ █▀█ █░█░█ █▀
█▀▀ ░█░ █▀█ █▄█ █▄▀ █ ░█░   ░░   ▀▄▀▄▀ █ █░▀█ █▄▀ █▄█ ▀▄▀▄▀ ▄█
    """
    init.init_config_file()
    print(banner)
    command_help()

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