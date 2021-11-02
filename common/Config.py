import configparser
import os
import sys
from tkinter import messagebox
from common import Values

item_dict = None
file_name=Values.CONFIG_FILE_NAME
section_list = []

"""This function reads the section from the config.ini file"""
def read_section(section):
    global file_name
    cfg = configparser.ConfigParser()
    file_exists = os.path.isfile(file_name)
    if (file_exists):
        global item_dict
        try:
            cfg.read(file_name)
            items = cfg.items(section)
            for values in items:
                item_dict[values[0]] = values[1]
                #print('Key : {}, Value: {}'.format(values[0],values[1]))
        except configparser.NoOptionError as ex:
            print(ex)
    else:
        messagebox.showerror('Error', 'Config File Not Found')

"""Read the value of the key from the dictionary first. If no item is available
then read from the config.ini file. If it finds the key after reading the config file then
add the key to the dictionary. If not found then raise an error saying "key not found"""
def get_setting(section=Values.DATABASE_SECTION,key=None):
    global item_dict, file_name
    if item_dict is None:
        item_dict = {}
        section_list.append(section)
        print('Reading Config FIle')
        read_section(section)
    else:
        """
        check if the section is already read.
        If read then check for the key and return key val
        If not read then read the file with section and return key val.
        """
        if section_list.count(section)==0:
            #section not read. So read file
            #print('Reading Section {}'.format(section,))
            read_section(section)

    return get_value(key)

"""Returns value of the key from the dictionary. If not found shows error"""
def get_value(key):
    val = item_dict[key]
    if val is not None:
        return val
    else:
        messagebox.showerror("Error",'{} Not Found In Config File'.format(key, ))
        sys.exit(0)

