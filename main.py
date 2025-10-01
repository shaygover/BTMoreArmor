#!/bin/python3
import json
from typing import TextIO
from os import getcwd, mkdir, scandir, chdir
import configparser
from pathlib import Path
from os.path import join as path_join
from shutil import rmtree

def json_filter(filename: Path, multi) -> json:
    """
        read json from filename
        :argument filename: json file to filter
        :argument multi: Multiplier for armor
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

    temp_location_list = list()

    for index in json_file['Locations']:
        del index['Hardpoints']
        del index['Tonnage']
        del index['InventorySlots']
        del index['InternalStructure']
        temp_location_list.append(index)

    temp_json['Locations'] = temp_location_list

    # Apply multi. Might be better to use loop, some of them might not exist for all mechs.
    # I'm assuming that all front exist. Will check for back. Rounding to nearest 10.
    temp_json['Locations'][0]['MaxArmor'] = int(round(float(temp_json['Locations'][0]['MaxArmor']) * float(multi), -1))
    temp_json['Locations'][1]['MaxArmor'] = int(round(float(temp_json['Locations'][1]['MaxArmor']) * float(multi), -1))
    temp_json['Locations'][2]['MaxArmor'] = int(round(float(temp_json['Locations'][2]['MaxArmor']) * float(multi), -1))
    temp_json['Locations'][3]['MaxArmor'] = int(round(float(temp_json['Locations'][3]['MaxArmor']) * float(multi), -1))
    temp_json['Locations'][4]['MaxArmor'] = int(round(float(temp_json['Locations'][4]['MaxArmor']) * float(multi), -1))
    temp_json['Locations'][5]['MaxArmor'] = int(round(float(temp_json['Locations'][5]['MaxArmor']) * float(multi), -1))
    temp_json['Locations'][6]['MaxArmor'] = int(round(float(temp_json['Locations'][6]['MaxArmor']) * float(multi), -1))
    temp_json['Locations'][7]['MaxArmor'] = int(round(float(temp_json['Locations'][7]['MaxArmor']) * float(multi), -1))

    # Back armor. Only for Center and Torso. Check first if -1.
    if int(temp_json['Locations'][2]['MaxRearArmor']) != -1:
        temp_json['Locations'][2]['MaxRearArmor'] = (
            int(round(float(temp_json['Locations'][2]['MaxRearArmor']) * float(multi), -1)))
    if int(temp_json['Locations'][3]['MaxRearArmor']) != -1:
        temp_json['Locations'][3]['MaxRearArmor'] = (
            int(round(float(temp_json['Locations'][3]['MaxRearArmor']) * float(multi), -1)))
    if int(temp_json['Locations'][4]['MaxRearArmor']) != -1:
        temp_json['Locations'][4]['MaxRearArmor'] = (
            int(round(float(temp_json['Locations'][4]['MaxRearArmor']) * float(multi), -1)))

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
    # path_join returns an OS neutral path
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
        print("Multiplier is lower than 1")

    return True


def read_settings() -> configparser:
    """
    Read settings from config.ini file
    :return: config parser object
    """
    settings = configparser.ConfigParser()
    settings.read("config.ini")

    return settings


def read_chassisdefs(settings) -> dict:
    """
    Reads all chassisdefs data from files.
    Updates if existing mechs found.
    Read order:
    Base, (DLCs: Flashpoint, HeavyMetal, UrbanWarfare), Mods
    :param settings: settings as configeparser class
    :return:
    """
    chassisdefs_dict = dict()

    # Get current working folder
    current_path = getcwd()

    # Create base folder path and get list of files inside.
    path = Path(path_join(current_path, settings['paths_in']['base']))
    # Code from chatgpt.
    files = [entry.path for entry in scandir(path) if entry.is_file()]

    # Add all other folders if they exist
    if settings['paths_in']['flashpoint'] != "":
        path = Path(path_join(current_path, settings['paths_in']['flashpoint']))
        files += ([entry.path for entry in scandir(path) if entry.is_file()])

    if settings['paths_in']['heavymetal'] != "":
        path = Path(path_join(current_path, settings['paths_in']['heavymetal']))
        files += ([entry.path for entry in scandir(path) if entry.is_file()])

    if settings['paths_in']['urbanwarfare'] != "":
        path = Path(path_join(current_path, settings['paths_in']['urbanwarfare']))
        files += ([entry.path for entry in scandir(path) if entry.is_file()])

    if settings['paths_in']['mods'] != "":
        path = Path(path_join(current_path, settings['paths_in']['mods']))
        files += ([entry.path for entry in scandir(path) if entry.is_file()])


    # Iterate on files
    for file in files:
        temp_json = json_filter(Path(file), settings["settings"]["multi"])

        # if key exist delete it. This may happen if there's a modded version.
        # Since mods is read after base (and DLCs) we can just delete the existing version
        if temp_json["Description"]["Id"] in chassisdefs_dict.keys():
            del chassisdefs_dict[temp_json["Description"]["Id"]]

        chassisdefs_dict[temp_json["Description"]["Id"]] = temp_json

    return chassisdefs_dict


def json_writer(chassisdefs, out_path):
    """
    Writes all chassisdefs jsons to files
    :param chassisdefs: dictionary containing all jsons
    :param out_path: output folder name
    :return: nothing
    """
    # Get current working folder
    current = getcwd()

    # Change dir to output folder
    chdir(out_path)

    for chassisdef in chassisdefs.values():
        file = open(chassisdef["Description"]["Id"] + ".json", "w", encoding="utf-8")
        # indent and separators will write it to file like BattleTech orig config files
        json.dump(chassisdef, file, indent=4, separators=(",", ": "))
        file.close()

    pass


def main():
    # Read Settings
    settings = read_settings()

    # Check if settings are correct
    folder_checker(settings)

    # Read all chassisdefs to a dictionary
    chassisdefs = {}
    chassisdefs = read_chassisdefs(settings)

    # Write to files
    json_writer(chassisdefs, settings['paths_out']['output'])


if __name__ == "__main__":
    main()