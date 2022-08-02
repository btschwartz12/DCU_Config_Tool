import json
import os
import sys
from tkinter import messagebox


options_fn = os.path.join(os.getcwd(), 'config', 'options.json')
excel_tool_fn = os.path.join(os.getcwd(), 'config', 'wkst_config.json')

options = {  } # Can add default options
wkst_config = {  } # Can add default options

try:
    with open(options_fn) as f:
        options.update(json.load(f))
    with open(excel_tool_fn) as f:
        wkst_config.update(json.load(f))
except Exception as e:
    messagebox.showerror("Config Error", "Cannot find config files.\nPlease ensure options.json and wkst_config.json are in the config directory.\n\nerror msg:\n\n+" + str(e))
    exit(1)

def getResourcePath(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Config:
    def __init__(self):

        self.VERSION = options.get("version") # Current app version
        self.SRC_DIR = options.get("source_directory") # Directory where all files will be pulled from

        self.LOG_MODE =         options.get("log_mode")
        self.RUNTIME_LOG_PATH = options.get("runtime_log_path")
        self.SHEET_NAME =       options.get("sheet_name")

        self.DEFAULT_ENTRY_DIRECTORY = options.get("default_entry_directory")
        self.DEFAULT_FREQS_DIRECTORY = options.get("default_freqs_directory")

        self.DEFAULT_COUNTRY =  wkst_config.get("default_country")
        self.ENTRIES =          wkst_config.get("entries")
        self.DROPDOWN_OPTIONS = wkst_config.get("dropdown_options")
        self.FREQUENCY_KEYS =   wkst_config.get("frequency_keys")

        for var, val in vars(self).items():
            if val == None:
                raise Exception("error 102: cannot find value for config variable '"+var+"'. Please check config files.")

        if not os.path.exists(self.SRC_DIR):
            self.SRC_DIR = os.path.abspath('.')
            messagebox.showwarning("Config directory error", "Source directory does not exist. Please check config files. Using current directory instead: "+self.SRC_DIR, icon='warning')
        
        self.LOCATION_DATA_PATH =   getResourcePath("data/location_data.json")
        self.TIMEZONE_DATA_PATH =   getResourcePath("data/time_zone_data.json")
        self.EXPORT_SCHEMA_PATH =   getResourcePath("data/DCU+2XLS.xsd")
        self.EXPORT_TEMPLATE_PATH = getResourcePath("data/DCU2+XLS_TEMPLATE.xml")
        self.LOGO_PATH =            getResourcePath("data/aclara.png")
        
        if not os.path.exists(self.DEFAULT_ENTRY_DIRECTORY) or not os.path.exists(self.DEFAULT_FREQS_DIRECTORY):
            self.DEFAULT_ENTRY_DIRECTORY = os.path.join(self.SRC_DIR, self.DEFAULT_ENTRY_DIRECTORY)
            self.DEFAULT_FREQS_DIRECTORY = os.path.join(self.SRC_DIR, self.DEFAULT_FREQS_DIRECTORY)
            if not os.path.exists(self.DEFAULT_ENTRY_DIRECTORY) or not os.path.exists(self.DEFAULT_FREQS_DIRECTORY):
                self.DEFAULT_ENTRY_DIRECTORY = getResourcePath("SAMPLE_IMPORT_DATA")
                self.DEFAULT_FREQS_DIRECTORY = getResourcePath("SAMPLE_IMPORT_DATA")
                messagebox.showwarning("Config directory error", "Default entry directory or default frequency directory does not exist. Please check config files. Using hard-coded default data instead: "+self.DEFAULT_ENTRY_DIRECTORY, icon='warning')
        

        self.FREQUENCY_RUNTIME_JSON_STR = ""
        self.ENTRIES_RUNTIME_JSON_STR = ""