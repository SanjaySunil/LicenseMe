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
    
# Main
def main():
    with open('copy.json') as f:
        data = json.load(f)

        directory = "."
        # Get Copyright Text 
        copyright_file = "copy.json"

        extension = ".js"

        # Get Contents of Directory
        files = os.listdir(directory)

        if len(files) == 0:
            print("[ERROR]: No file found with extension " + extension)
            sys.exit(1)
            
        if not os.path.isdir(directory):
            print('[ERROR]: Not a valid directory!')
            print('Usage: python copyright.py <dir> <copyright.txt> <.extension>')
            sys.exit(1)

        try:
            fp = open(copyright_file, 'r')
            copyright_text = ''.join(fp.readlines())
            fp.close()
            add_copyright(directory, extension, copyright_text)
        except FileNotFoundError as er:
            print("[ERROR]: Please add file with copyright content.")
            sys.exit(1)

# Add Copyright
def add_copyright(directory, extension, copyright_text):
    with open('copy.json') as f:
        data = json.load(f)
        obj = os.listdir(directory)
        for f in obj:
            if os.path.isdir(directory + '/' + f):
                add_copyright(directory + '/' + f, extension, copyright_text)
            # Operate only files
            if os.path.isfile(directory + '/' + f) and f.endswith(extension):
                fp = open(directory + '/' + f, 'r')
                lines = fp.readlines()
                fp.close()
                complete_copyright = """/**
 * @file """ + f + """
 * @author """ + data["author"] + """
 * @license """ + data["license"] + """
 */
"""
                if complete_copyright not in (''.join(lines)):
                    lines.insert(0, ''.join(complete_copyright) + '\n')
                    fp = open(directory + '/' + f, 'r+')
                    fp.writelines(lines)
                    fp.close()
                    print("✔ COPYRIGHT Protected: " + f)
                else:
                    print("[ERROR]: " + directory + "/" + f + " already has copyright protection.")

main()