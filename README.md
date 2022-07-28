# DCU Configuration - XML Creation Tool

This simple application will allow a user to input certain fields and import frequencies to generate the .xml file used to configure the DCU.

## **Installation**

- Install [python](https://www.python.org/downloads/)
- Install pip using the link below or these commands:
```bash
python -m pip install --upgrade pip
pip install get-pip.py
```
- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following modules:

```console
pip install openpyxl
pip install xmlschema
```

## **Setup**

Locate the options.json file, and ensure these fields are set correctly:

```python
'source_directory' # Where the project lives on your machine
'version' # The current version of the tool

'sheet_name' # The name of the sheet that holds frequency data, if the user opts to load frequencies from an Excel workbook

'''For the following fields, you may include just the relative path if they are relative to the indicated source directory'''

'export_schema_path' # The path to the .xsd that corresponds to the exported DCU .xml
'export_template_path' # The path to the .xml that is a blank version of the exported DCU .xml
'location_data_path' # The path to the .json that holds relevent data for locations (city, state, country)
'timezone_data_path' # The path to the .json that holds relevent data for each time zone
'default_entry_directory' # The path to the directory that will initially be used by the user to find and load entry files
'default_freqs_directory' # The path to the directory that will initially be used by the user to find and load frequency files

```

### **Additional Setup** 

The following does not need to be modified to properly run the program, but must be changed if:

- The user wants to change the default country shown
- There is a change to the names of keys in the frequency file
- There is a change to the displayed entry fields
- There is a change to the entry fields that have dropdown options

If one of these is true, locate the wkst_config.json file, and ensure these fields are set correctly:

```python

'default_country' # The country displayed in the entry field at startup
'frequency_keys' # The names of the keys corresponding to the customer name & id, frequency, and frequency use. If these are different in the frequency file that will be imported, change them here
'entries' # A list of entry fields that will be shown on the screen. Each entry field has the following properties:
    - 'name' # Name of the entry shown on the screen
    - 'type' # Weather it's a string/number entry, a checkbox, or a dropdown
    - 'editable' # Weather or not the user may edit the field
    - 'required' # Weather or not the field is required to perform calculations
    - 'comment' # An optional field that will indicate the message displayed if the user clicks on the entry's info button
'dropdown_options' # A map where the keys correspond to entry fields that have dropdown options, and values indicating what the dropdown options are. If the options are defined in another file, it is set to null.
```

## **Usage**

After ensuring that the setup step has been completed correctly, run these commands:

```bash
$ cd <Directory that contains src/ + app.py>
$ python.exe app.py
```

## **Handling Errors**

During the execution of the program, there are several instances where an error can occur. Here is a list of potential errors, and steps to take to possibly fix them.

- **Invalid data format** - One of the imported files (entries or frequencies) is not formatted correctly. The entry file should be a dictionary, and the frequency file should be a list of frequency dictionary objects.

- **Invalid key name** - In the entry or frequency file, there is an unrecognized key name. Ensure that the imported file key's correspond to the keys indicated in the wkst_config.json file.

- **Incompatible data** - In the entry file, a specified value has an unexpected type. Ensure that the value types in the entry file match those indicated in the wkst_config.json file

- **Bad frequency data** - During the proccessing of the frequency file, either the data is formatted incorrectly, a required key was not found, or an unexpected value type was parsed. Check the format of the imported frequency file, and the required keys in the wkst_config.json file. If a spreadsheet is being used, make sure that the headers are in row A, and each row below is a frequency object that has all required keys set.

- **Invalid entries** - When not all required entry fields have been properly specified. Ensure that all entry fields have the correct value, and attempt to calculate again.

- **Invalid entry** - When the data entered for a specific entry is invalid, usually when a number-only entry has non-numbers entered into it. Ensure that the data being entered matches the type specified in the wkst_config.json file, and try again.

- **Calculation Error** - When there is an error during calculations, usually when a non-sensible set of user entries is used during calculation. This is the most difficult error to fix. Try turing on the log_mode option in the options.json file, and specify the .txt file that the log will be written to. In the log file, it will contain all of the step calculations up to the point where the error occurred. If the bug is still not apparent, inspect the code for that specific step to ensure that the calculations match up with the Excel tool. 

- **Config error** - When the calculated status of the configuration is not good enough to safely export the DCU .xml file. Check the status message provided for further instruction.

## **Contributing**

TBD, a git repository still needs to be created

## **Contact**

If you want to contact me, you can reach me at BSchwartz@hubbell.com

## **Licence**

This project uses the MIT License.