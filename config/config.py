import json
import os


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
    print("default options used due to", e)

class Config:
    def __init__(self):

        self.REG_DIMENSIONS = options.get("dimensions")
        self.MIN_DIMENSIONS = options.get("min_dimensions")
        self.MAX_DIMENSIONS = options.get("max_dimensions")

        self.VERSION = options.get("version") # Current app version
        self.SRC_DIR = options.get("source_directory") # Directory where all files will be pulled from

        self.LOG_MODE = options.get("log_mode")
        self.RUNTIME_LOG_PATH = options.get("runtime_log_path")
        
        self.DEFAULT_COUNTRY = wkst_config.get("default_country")
        self.DEFAULT_ENTRY_DIRECTORY = options.get("default_entry_directory")
        self.DEFAULT_FREQS_DIRECTORY = options.get("default_freqs_directory")

        self.EXPORT_SCHEMA_PATH = options.get("export_schema_path")
        self.EXPORT_TEMPLATE_PATH = options.get("export_template_path")

        self.ENTRIES = wkst_config.get("entries")
        self.DROPDOWN_OPTIONS = wkst_config.get("dropdown_options")

        self.LOCATION_DATA_PATH = options.get("location_data_path")
        self.TIMEZONE_DATA_PATH = options.get("timezone_data_path")

        self.FREQUENCY_KEYS = wkst_config.get("frequency_keys")

        self.SHEET_NAME = options.get("sheet_name")


        self.FREQUENCY_RUNTIME_JSON_STR = ""
        self.ENTRIES_RUNTIME_JSON_STR = ""
        

        for var, val in vars(self).items():
            if val == None:
                raise Exception("error 102: cannot find value for config variable '"+var+"'. Please check config files.")


        