# DCU Configuration - XML Creation Tool

This simple application will allow a user to input certain fields and import frequencies to generate `DCU2+XLS.xml`.

## **Installation**

For the application to run properly, you must have the executable downloaded on your machine (currently called `DCU Config Tool.exe`), and that there is a `config/` folder in the same directory as the executable, with two files: `options.json` and `wkst_config.json`. 

Verify that the fields of the config files are tailored to your machine and to your liking (see [Setup](#setup)).

To run the application, see [Usage](#usage).

If you want to see the source code, see [Downloading the Code](#downloading-the-code). 

If you want to re-build the executable on your machine, see [Creating the Executable](#creating-the-executable).

## **Downloading the Code**

This is optional and not required for proper use of the application.

However, if you want to see the source code or build your own executable, this step is required.

To download the code, you must have [git](https://git-scm.com/download/win) installed on your machine. Try the following command:

```bash
git --version
# If this does not print out a version number, download git from the link above, then proceed
```

Once git is installed, run these commands:

```bash
cd __ # Directory where you want the code
git clone https://github.com/btschwartz12/DCU_Config_Tool
cd DCU_Config_Tool
```

## **Setup**

Please ensure that the executable and `config/` directory are located in the same folder on your machine. If you chose to download the code, make sure your current working directory in the command line is `DCU_Config_Tool`.

Locate the `options.json` file in the  `config/` directory, and ensure these fields are set correctly:

```python
'source_directory' # Where the project lives on your machine. Only neccesary if you downloaded the code
'version' # The current version of the tool

'log_mode' # If you want to save the log of calculations
'runtime_log_path' # Where the log calculations will be written to

'sheet_name' # The name of the sheet that holds frequency data, if the user opts to load frequencies from an Excel workbook

'default_entry_directory' # The path to the directory that will initially be used by the user to find and load entry files. Can be left empty
'default_freqs_directory' # The path to the directory that will initially be used by the user to find and load frequency files. Can be left empty

```

### **Additional Setup** 

The following does not need to be modified to properly run the program, but must be changed if:

- The user wants to change the default country shown
- There is a change to the names of keys in the frequency file
- There is a change to the displayed entry fields
- There is a change to the entry fields that have dropdown options

If one of these is true, locate the `wkst_config.json` file in the  `config/` directory, and ensure these fields are set correctly:

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

Before using the tool, all of these must be true:

1. The executable and `config/` directory are located in the same folder on your machine.
2. The `config/` directory contains `options.json` and `wkst_config.json`, and are well formed, if they were modified (see [Setup](#setup) and [Additional Setup](#additional-setup))
3. If you chose to use your own entry and frequency data files, they are in a directory and that directory is recorded in the appropriate `options.json` field.

If these are true, click on the executable to run the application. 

For any errors experienced during runtime, see [Handling Errors](#handling-errors). 

## **Handling Errors**

During the execution of the program, there are several instances where an error can occur. Here is a list of potential errors, and steps to take to possibly fix them.

- **Config error** - The application cannot find the config files. Please ensure that the `config/` directory is in the same directory as the executable and contains `options.json` and `wkst_config.json`, and are well formed, if they were modified (see [Setup](#setup) and [Additional Setup](#additional-setup)).

- **Config error** - The application cannot find the source directory or the default entry/frequency directorys. This is not a fatal error, but will prevent the application from using the present working directory and it's own entry/frequency default data.

- **Invalid data format** - One of the imported files (entries or frequencies) is not formatted correctly. The entry file should be a dictionary, and the frequency file should be a list of frequency dictionary objects.

- **Invalid key name** - In the entry or frequency file, there is an unrecognized key name. Ensure that the imported file key's correspond to the keys indicated in the wkst_config.json file.

- **Incompatible data** - In the entry file, a specified value has an unexpected type. Ensure that the value types in the entry file match those indicated in the wkst_config.json file.

- **Bad frequency data** - During the proccessing of the frequency file, either the data is formatted incorrectly, a required key was not found, or an unexpected value type was parsed. Check the format of the imported frequency file, and the required keys in the wkst_config.json file. If a spreadsheet is being used, make sure that the headers are in row A, and each row below is a frequency object that has all required keys set.

- **Invalid entries** - When not all required entry fields have been properly specified. Ensure that all entry fields have the correct value, and attempt to calculate again.

- **Invalid entry** - When the data entered for a specific entry is invalid, usually when a number-only entry has non-numbers entered into it. Ensure that the data being entered matches the type specified in the wkst_config.json file, and try again.

- **Calculation error** - When there is an error during calculations, usually when a non-sensible set of user entries is used during calculation. This is the most difficult error to fix. Try turing on the log_mode option in the options.json file, and specify the .txt file that the log will be written to. In the log file, it will contain all of the step calculations up to the point where the error occurred. If the bug is still not apparent, inspect the code for that specific step to ensure that the calculations match up with the Excel tool. 

- **Config Status error** - When the calculated status of the configuration is not good enough to safely export the DCU .xml file. Check the status message provided for further instruction.

- **Export error** - When there is an error during the conversion of the template to a data structure so that the calculations can be loaded into it and transferred back to an .xml. Chack the message, ensure that the schema and template have been correctly specified in the options.json file, and that the key names in the template xml match those found in the getXMLstr() function of calculator.py.

## **Creating the Executable**

This is optional and not required for proper use of the application.

To create the executable, the source code must be downloaded to your machine (see [Downloading the Code](#downloading-the-code)), and your present working directory in the command line must be `DCU_Config_Tool/`. 

1. Install [Python (3+)](https://www.python.org/downloads/) and ensure you can open a python interpreter:
```bash
$ py
# Make sure that the below interpreter is opened. If not, download Python using the link above.
Python 3.10.5 (tags/v3.10.5:f377153, Jun  6 2022, 16:14:13) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```
2. Install [pip](https://pip.pypa.io/en/stable/) using the link or these commands:
```bash
$ pip --version
# If the above statement prints a version of pip, ignore the rest of the commands
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ py get-pip.py
$ py -m pip install --upgrade pip
```
3.  Use the pip to install the following modules:

```bash
$ pip install pyinstaller
$ pip install openpyxl
$ pip install xmlschema
```

4. Once you have installed these modules, run this command and ensure that all three of the above modules are installed and make note of their file location:

```bash
$ pip list -v
...
pyinstaller   5.3     ...\python\python310\lib\site-packages ...
xmlschema     2.0.1   ...\python\python310\lib\site-packages ...
openpyxl      3.0.10  ...\python\python310\lib\site-packages ...
...
```
5. Locate the `app.spec` file. This is the file that `pyinstaller` uses to create an executable. We are going to first fix the paths in this file, then modify the build script. Locate the `Analysis` attribute:

```python
a = Analysis(
    ['<YOUR_SOURCE_PATH>/DCU_Config_Tool/app.py'],
    ...
    datas=[('<YOUR_PYTHON_LIBRARY_PATH>/xmlschema', 'xmlschema/'), 
            ('<YOUR_PYTHON_LIBRARY_PATH>/openpyxl', 'openpyxl/'), 
            ('data/aclara.png', 'data/'),
            ('data/location_data.json', 'data/'),
            ('data/time_zone_data.json', 'data/'),
            ('data/DCU+2XLS.xsd', 'data/'),
            ('data/DCU2+XLS_TEMPLATE.xml', 'data/'),
            ('SAMPLE_IMPORT_DATA/sample_freqs.json', 'SAMPLE_IMPORT_DATA/'),
            ('SAMPLE_IMPORT_DATA/sample_wkst_entries.json', 'SAMPLE_IMPORT_DATA/'),
            ],
    ...
```
Find `<YOUR_SOURCE_PATH>`, and replace it the absolute path of where your source directory is located. (If you need help, try running the command `$ pwd`).

Find `<YOUR_PYTHON_LIBRARY_PATH>`, and replace it with the corresponding path from step 4. 

DO NOT MODIFY ANYTHING ELSE.

6. Locate the `buildScript.bat` batch file in the `scripts/` directory. Find Section 1, and initialize the name of your directory from step 5, and the name of the spec file. Section 2 will build the executable, and Section 3 will place the config files in the executable's directory.

7. Run the batch file on your machine:

```bash
$ ./scripts/buildScript.bat # This should take ~20 seconds
```
If an error occurs, contact the owner. 

8. After the executable has been tested or moved somewhere else, to clean all files generated by the process, run the clean script:

```bash
$ ./scripts/cleanScript.bat # Will remove all pyinstaller generated files and __pycache__ files
```

## **Contributing**

TBD, a correct git repository still needs to be decided

## **Contact**

If you want to contact me, you can reach me at BSchwartz@hubbell.com

## **Licence**

This project uses the MIT License.