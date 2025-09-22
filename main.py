#!/bin/python3
import json
from typing import TextIO
from os import getcwd, mkdir
import configparser
from pathlib import Path
from os.path import join as path_join
from shutil import rmtree

def json_file_filter(filename: str) -> json:
    """
        read json from filename
        :argument filename: json file to filter
        :return filtered json file: max armor and mech id. mech id is the same as file name.
    """
    json_file: json
    # Load the file
    json_file = json.load(open(filename, 'r'))

    """ Remove all unneeded entries by creating new json file
     json file is a dictionary. so temp_json is the new file.
     
     temp location in the list of locations, hardpoints need to be removed from that list.
     this is done in the for loop"""
    temp_json = {"Description": {}}
    temp_json["Description"]["Id"] = json_file["Description"]["Id"]

    temp_location_list = []

    for index in json_file['Locations']:
        del index['Hardpoints']
        del index['Tonnage']
        del index['InventorySlots']
        del index['InternalStructure']
        temp_location_list.append(index)

    temp_json['Locations'] = temp_location_list

    # temp_json['Locations'][0]['MaxArmor'] *= 2 - here for the double my armor. need to move to another func

    return temp_json

def folder_checker(settings: configparser) -> bool:
    """
    Verifies that each of the input and output folders exists.
    For input also verifies that the folders aren't empty.
    For output verifies it's empty.
    :param settings: 
    :return: 
    """
    # Get current working folder
    current = getcwd()

    # Check if input folders exists and not empty.
    for (key, value) in settings['paths_in'].items():
        if not value == "":
            # Create folder path, os independent
            path = Path(path_join(current, value))
            # Check if path is an empty folder or not a folder at all
            if not(path.is_dir() or any(path.iterdir())):
                raise value + " Is not a folder or is empty"

    # Delete and create output folder
    out_path = Path(path_join(current, settings['paths_out']['output']))
    if out_path.exists() and out_path.is_dir():
        rmtree(out_path)
    mkdir(out_path)

    # Check if multi exists.
    multi = settings['settings']['multi']
    if multi == "":
        raise "Multiplier is empty"

    # Check if multi is not a number
    try:
        float(multi)
    except ValueError:
        raise "Multiplier is not a number"

    # Check if multi bellow 1. Warn.
    if float(multi) < 1:
        print("Multi is lower than 1")

    return True


def read_settings() -> configparser:
    """
    Read settings from config.ini file
    :return: config parser object
    """
    settings = configparser.ConfigParser()
    settings.read("config.ini")

    return settings



def main():
    # Read Settings
    settings = read_settings()

    # Check if settings are correct
    if not folder_checker(settings):
        raise FileNotFoundError

    # Test with a specific chassisdef
    json_file_filter("UrbanWarfare/chassisdef_cataphract_CTF-0X.json")


if __name__ == "__main__":
    main()