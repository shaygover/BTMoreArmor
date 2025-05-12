#!/bin/python3
import json
from typing import TextIO

# Constants
MAX_ARMOR = 1.48

def json_file_filter(filename: str) -> json:
    """
        read json from filename
        :argument filename: json file to filter
        :return filtered json file: max armor and mech id. mech id is the same as file name.
    """
    json_file: json
    # Load the file
    json_file = json.load(open(filename, 'r'))

    """ Remove all unneeded entries bu creating new json file
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




def main():
    json_file_filter("UrbanWarfare/chassisdef_cataphract_CTF-0X.json")


if __name__ == "__main__":
    main()