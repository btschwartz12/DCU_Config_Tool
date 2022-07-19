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
        self.SRC_DIR = options.get("SOURCE_DIRECTORY") # Directory where all files will be pulled from
        
        self.DEBUG_MODE = options.get("debug_mode")
        self.DEBUG_SAMPLE_FREQS_JSON_RPATH = options.get("sample_freqs_json_fn")
        self.DEBUG_SAMPLE_ENTRIES_JSON_RPATH = options.get("sample_entries_json_fn")

        self.EXPORT_SCHEMA_RPATH = wkst_config.get("output_schema_rpath")
        self.EXPORT_TEMPLATE_JSON_RPATH = wkst_config.get("example_output_json_rpath")

        self.ENTRIES = wkst_config.get("entries")
        self.DROPDOWN_OPTIONS = wkst_config.get("dropdown_options")

        for var, val in vars(self).items():
            if val == None:
                raise Exception("error 102: cannot find value for config variable '"+var+"'. Please check config files.")