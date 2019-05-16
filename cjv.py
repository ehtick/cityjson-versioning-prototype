#!/usr/local/bin/python3

import json
import sys
import commands

# Code to have colors at the console output
from colorama import init, Fore, Back, Style
init()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a (versioned) CityJSON file")
        quit()

    # The filename of the CityJSON file to be analysed
    versioned_filename = sys.argv[1]

    if len(sys.argv) < 3:
        print("Please provide a command.")
        quit()

    command_name = sys.argv[2]

    print("Opening %s..." % versioned_filename)

    # Parse the CityJSON file through the json library
    cityjson_data = open(versioned_filename)
    try:
        citymodel = json.load(cityjson_data)
    except:
        print("Oops! This is not a valid JSON file!")
        quit()
    cityjson_data.close()

    args = {}
    args["citymodel"] = citymodel

    if "versioning" not in citymodel:
        print(Fore.RED + "The file provided is not a versioned CityJSON!")
        quit()

    if command_name == "log": 
        if len(sys.argv) > 3:
            args["ref"] = sys.argv[3]
    elif command_name == "checkout":
        args["version_name"] = sys.argv[3]
        args["output_file"] = sys.argv[4]
    
    command = commands.factory.get_command(command_name, **args)
    
    if command == None:
        print("'%s' is not a valid command. Please try one of: log." % command)
        quit()

    command.execute()

    # TODO: Validate "versioning" property (should have versions, branches and tags)
