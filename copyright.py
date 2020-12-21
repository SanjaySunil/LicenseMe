"""
Author: Sanjay Sunil (D3VSJ)
File: copyright.py
Description: Your handy tool for licensing and protecting your code.
License: GPL-3.0
"""

# Imports
import sys
import os
import json
import logging
from datetime import datetime

# Location to Config File
config = 'config.json'

# Clean debug.log before next run.
def deleteCurrentLog():
    with open(config) as x:
        data = json.load(x)
        if data['settings']['createSessionLog'] == True:
            if os.path.exists("debug.log"):
                os.remove("debug.log")

# Create Debug Reports
def debugLogger(message):
    with open(config) as x:
        data = json.load(x)
        if data['settings']['createSessionLog'] == True:
            logger = open("debug.log", "a")
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            logger.write("["+dt_string+"]: " + message)
            logger.close()

# Main
with open(config) as x:
    data = json.load(x)
    def main():
        # Get Copyright Text 
        # copyright_file = "copy.txt"

        # Root Directory
        directory = data['directory']
        # Extension
        extension = ".js"
        # Get Contents of Directory
        files = os.listdir(directory)

        # Tests
        if len(files) == 0:
            # No files in directory.
            error_message = "[ERROR]: No file found with extension " + extension +"\n"
            print("[ERROR]: No file found with extension " + extension)

            debugLogger(error_message)
            sys.exit(1)
                
        if not os.path.isdir(directory):
            # Error: The directory does not exist.
            error_message = "[ERROR]: Not a valid directory!\n"
            print('[ERROR]: Not a valid directory!')

            debugLogger(error_message)
            sys.exit(1)

        if data['options']['includeAuthorName'] == False and data['options']['includeLicense'] == False and data['options']['includeFileName'] == False:
            # Error: You cannot have all LicenseMe options as false. This is because nothing would be added to the license on the files.
            error_message = "[ERROR] You cannot have all LicenseMe options as false!\n"
            print("[ERROR] You cannot have all LicenseMe options as false!")

            debugLogger(error_message)
            sys.exit(1)

        add_copyright(directory, extension)

        # To be implemented later for custom copyright.

        #try:
        #    
        #    fp = open(copyright_file, 'r')
        #    copyright_text = ''.join(fp.readlines())
        #    fp.close()
        #    
        #    add_copyright(directory, extension)
        #
        #except FileNotFoundError as er:
        #    print("[ERROR]: Please add file with copyright content.")
        #    sys.exit(1)
        
    # Add Copyright Function
    def add_copyright(directory, extension):
        obj = os.listdir(directory)
        for f in obj:
            if os.path.isdir(directory + '/' + f):
                add_copyright(directory + '/' + f, extension)
            # Operate only files
            if os.path.isfile(directory + '/' + f) and f.endswith(extension):
                fp = open(directory + '/' + f, 'r')
                lines = fp.readlines()
                fp.close()

                # Building process of Copyright Text.
                complete_copyright = ""
                complete_copyright += "/**"
                # Adding options from config file to Copyright Text.
                if data['options']['includeFileName'] == True: 
                    complete_copyright += "\n * @file " + f
                if data['options']['includeAuthorName'] == True:
                    complete_copyright += "\n * @author " + data["author"]
                if data['options']['includeLicense'] == True:
                    complete_copyright += "\n * @license " + data["license"]
                
                complete_copyright += "\n */\n"

                # Implement Copyright
                if complete_copyright not in (''.join(lines)):
                    lines.insert(0, ''.join(complete_copyright) + '\n')
                    fp = open(directory + '/' + f, 'r+')
                    fp.writelines(lines)
                    fp.close()

                    # Read showFilePath setting
                    if data['settings']['showFilePath'] == True:
                        # Success message with File Path.
                        print("[LicenseMe]: Licensed " + directory + "/" + f + ".")
                    elif data['settings']['showFilePath'] == False:
                        # Success message without File Path.
                        print("[LicenseMe]: Licensed " + f + ".")
                    else:
                        # Display invalid settings error.
                        error_message = "[ERROR]: Invalid settings for showFilePath!\n"
                        print("[ERROR]: Invalid settings for showFilePath!")

                        debugLogger(error_message)
                        exit()

                else:
                    # File has already been licensed.
                    error_message = "[ERROR]: " + directory + "/" + f + " has already been licensed!\n"
                    print("[ERROR]: " + directory + "/" + f + " has already been licensed!")

                    debugLogger(error_message)

deleteCurrentLog()
main()

a = input("\nPress Enter key to exit ...")

if a:
    exit(0)