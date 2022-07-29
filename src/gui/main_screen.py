# main_screen.py
# 6/20/22
# Ben Schwartz
#
# Holds the DcuWorksheetPage, which is the main screen that
# is shown throughout the usage of the tool

from datetime import datetime
import json
import os
from pprint import pformat
import tkinter as tk
from tkinter import messagebox
from typing import OrderedDict

from config.config import Config


from src.gui.wkst_entry import EntryType, WorksheetEntry
from src.processing.calc_steps.freqs_generator import FrequencyData, getFrequencyData
from src.processing.calculator import WorksheetCalculator
from src.utils.filepicker import FilePicker
from src.utils.scrollframe import VerticalScrolledFrame
from src.utils.utils import EntryException

NOT_READY_COLOR = 'red'
READY_COLOR = 'green'

CUST_NAME = "Customer Name"
CUST_ID = "Aclara Customer ID"
CONFIG_ID = "Customer Configuration Id"

class DcuWorksheetPage(tk.Frame):
    """This is the first page that is shown in the app, and will allow the user 
    to input certain data that will be used in further calculations. 
    The user has the ability to upload previously created entry data, and once finished
    they can begin the calculations and exporting"""
    def __init__(self, master, config: Config):
        tk.Frame.__init__(self, master)
        self.config = config

        self.WKST_ENTRIES_FN = "" # Filename if the user imported previous entries
        self.FREQUENCIES_FN = ""

        self.LOCATION_DATA = {}
        self.TIME_ZONE_DATA = {}
        with open(config.LOCATION_DATA_PATH, 'r') as f:
            self.LOCATION_DATA.update(json.load(f))
        with open(config.TIMEZONE_DATA_PATH, 'r') as f:
            self.TIME_ZONE_DATA.update(json.load(f))

        self.entries = {}
        self.status = tk.StringVar()


        self.__buildGUI()

        self.entries["Tool Version"].setValue(config.VERSION)

    def __buildGUI(self):
        """This will create the view of the entire page."""

        """Top view holds the name of the reading"""
        top_frame = tk.Frame(self)
        tk.Label(top_frame, text="Customer Worksheet", font=('Times', 15)).pack()

        file_picker_frame = tk.Frame(top_frame)
        file_picker_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5,20))
        file_picker_frame.grid_rowconfigure(0, weight=1)
        file_picker_frame.grid_columnconfigure(0, weight=1, uniform='group1')
        file_picker_frame.grid_columnconfigure(1, weight=1, uniform='group1')

        worksheet_frame = tk.Frame(file_picker_frame)
        worksheet_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=5)

        frequency_frame = tk.Frame(file_picker_frame)
        frequency_frame.grid(row=0, column=1, sticky=tk.NSEW, padx=5)

        self.worksheet_fp = FilePicker(worksheet_frame, self.config, title="Worksheet Import (.json)", extension='.json', command=self.__loadEntries, bg=NOT_READY_COLOR)
        self.worksheet_fp.pack(fill=tk.BOTH, expand=True)
        self.worksheet_fp.loadDir(self.config.DEFAULT_ENTRY_DIRECTORY)

        self.frequency_fp = FilePicker(frequency_frame, self.config, title="Frequency Import (.xlsx or .json)", extension=('.json', '.xlsx'), command=self.__loadFrequencies, bg=NOT_READY_COLOR)
        self.frequency_fp.pack(fill=tk.BOTH, expand=True)
        self.frequency_fp.loadDir(self.config.DEFAULT_FREQS_DIRECTORY)

        self.worksheet_color_box = tk.Label(worksheet_frame, text="", fg='white', bg=NOT_READY_COLOR)
        self.worksheet_color_box.pack(fill=tk.X, expand=True, anchor=tk.S)
        self.frequency_color_box = tk.Label(frequency_frame, text="", fg='white', bg=NOT_READY_COLOR)
        self.frequency_color_box.pack(fill=tk.X, expand=True, anchor=tk.S)

        top_frame.pack(fill=tk.X)
        
        """Middle view"""
        middle_frame = tk.Frame(self) # Placeholder
        middle_frame.pack(fill=tk.BOTH, expand=True)

        scroll_frame = VerticalScrolledFrame(middle_frame)
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        self.main_display = tk.Frame(scroll_frame)
        self.main_display.pack(fill=tk.BOTH, expand=True)

        """Status view"""
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill=tk.X, anchor=tk.S)
        tk.Label(bottom_frame, textvariable=self.status, fg='red').pack(fill=tk.X, anchor=tk.N)
        # Option to revert changes, has not been implemented
        btn_frame = tk.Frame(bottom_frame)
        btn_frame.pack(fill=tk.X, expand=True, anchor=tk.S)
        btn_frame.grid_rowconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(0, weight=1, uniform='group1')
        btn_frame.grid_columnconfigure(1, weight=1, uniform='group1')

        tk.Button(btn_frame, text="Examine Frequencies", command=self.__displayFrequencies, bg='#00137C', fg='white').grid(row=0, column=0, sticky=tk.NSEW)
        tk.Button(btn_frame, text="Calculate & Export", command=self.__calculateAndExport, bg='yellow').grid(row=0, column=1, sticky=tk.NSEW)

        self.__loadEntryViews()
    
    def __loadEntryViews(self):
            """This will look at the entries defined in the config file, and build WorksheetEntry objects for each 
            entry object. The created entry will then be added to a map (self.entries) that is used for lookup later"""
            entries = self.config.ENTRIES
            dropdowns = self.config.DROPDOWN_OPTIONS
            self.states_by_country = dropdowns["State"]

            for i, entry in enumerate(entries):
                
                name = entry["name"]
                entry_type = EntryType(entry["type"])
                is_editable = bool(entry["editable"])
                is_required = bool(entry["required"])
                comment = entry.get("comment")
                default_value = entry.get("default_value")
                dropdown_options = None

                if entry_type == EntryType.DROPDOWN:
                    try:
                        dropdown_options = dropdowns[name]
                    except Exception as e:
                        raise Exception("error 892: cannot find dropdown options for "+name)

                    if dropdown_options is None: # This means the options are defined in a config file
                        dropdown_options = self.__getDropdownOptions(name)
                        
                entry_frame = WorksheetEntry(self.main_display, self, self.config, name, entry_type, is_editable, is_required, dropdown_options, count=(i+1), comment=comment, default_value=default_value)

                self.entries[name] = entry_frame

                entry_frame.pack(fill=tk.X, padx=(5, 20))

            self.entries["Country"].combobox.bind("<<ComboboxSelected>>", self.__setStates)
    
    def __loadEntries(self, fn=None):
        """This is called every time the user clicks on the load worksheet button. 
        This will take the .json that is attempting to be imported, 
        make sure it is well formatted, and then populate all of the WorksheetEntries
        with its values"""
        if fn is None:
            if not self.worksheet_fp.is_selected():
                return
            fn = self.worksheet_fp.getSelectedFilePath()

        data = {}
        with open(fn, 'r') as f:
            data = json.load(f)

        if not isinstance(data, dict):
            messagebox.showerror("Invalid data format", "Incompatible data format found in "+fn+": \n\nFound: "+str(type(data))+"\nShould be: dict")
            self.updateView()
            return
        
        for key in data.keys():
            if key not in self.entries.keys():
                messagebox.showerror("Invalid key name", "Unknown key name found in "+fn+": \n       "+key+"\n\nCorrect keys: "+pformat(list(self.entries.keys()), indent=2))
                self.updateView()
                return

        for name, value in data.items():  
            try:
                self.entries[name].setValue(value)
            except Exception as e:
                messagebox.showerror("Incompatiable data", "Poor data found for key: "+name+"\n\n"+str(e))
                self.updateView()
                return

        if data["Tool Version"] != self.config.VERSION:

            error_msg = "Tool version found in import file: "+data["Tool Version"]+"\n\nCurrent tool version: "+self.config.VERSION
            error_msg += "\n\nDevices configured with different tools can be incompatible in the field. Please contact engineering for more information. Do you wish to override?"
            will_override = messagebox.askyesno("Incompatible tool version", error_msg)
            if not will_override:
                self.updateView()
                return

        self.WKST_ENTRIES_FN = fn

        self.updateView()
    
    def __loadFrequencies(self, fn=None):
        """This is called every time the user clicks on the load freqcencies button.
        This will look at the import file, and will call upon the getFrequencyData() function
        to generate the frequencies"""
        
        if fn is None:
            if not self.frequency_fp.is_selected():
                return
            fn = self.frequency_fp.getSelectedFilePath()

        try:
            FREQUENCY_DATA: FrequencyData = getFrequencyData(self.config, fn)
        except Exception as e:
            messagebox.showerror("Bad frequency data", "Cannot procss frequency data from "+str(fn)+"\n\n"+str(e))
            self.updateView()
            return

        self.FREQUENCIES_FN = fn
        self.__FREQUENCY_DATA = FREQUENCY_DATA
            
        self.__initFrequencies()
    
    def __initFrequencies(self):
            """This will capture the generated frequency data, and inspect to make sure
            that the user-entered ID and name match the frequencies. If not, a message is
            shown. this will also make other update to the view, and display the frequencies once
            finished."""

            name_entry: WorksheetEntry = self.entries[CUST_NAME]
            id_entry: WorksheetEntry = self.entries[CUST_ID]

            entered_name = name_entry.getValue()
            entered_id = id_entry.getValue()

            # Checking match for name, overwriting if necessary
            if entered_name == "":
                name_entry.setValue(self.__FREQUENCY_DATA.CUSTOMER_NAME)
            elif entered_name != self.__FREQUENCY_DATA.CUSTOMER_NAME:
                messagebox.showwarning("Warning", "Mismatching Customer Names\n\nEntered name: "+entered_name+"\nName found in frequency file: "+self.__FREQUENCY_DATA.CUSTOMER_NAME+"\n\nFrequency file name will overwrite.")
                name_entry.setValue(self.__FREQUENCY_DATA.CUSTOMER_NAME)
            
            # Checking match for ID, overwriting if necessary
            if entered_id == '':
                id_entry.setValue(self.__FREQUENCY_DATA.CUSTOMER_ID)
            elif entered_id != self.__FREQUENCY_DATA.CUSTOMER_ID:
                messagebox.showwarning("Warning", "Mismatching Customer IDs\n\nEntered id: "+str(entered_id)+"\nID found in frequency file: "+str(self.__FREQUENCY_DATA.CUSTOMER_ID)+"\n\nFrequency file id will overwrite.")
                id_entry.setValue(self.__FREQUENCY_DATA.CUSTOMER_ID)
            
            # Set frequency status to OK
            self.frequency_color_box.config(bg=READY_COLOR)
            self.status.set("")
            # Make updates to the view
            self.updateView()
            # Initially show the frequencies
            self.__displayFrequencies()
       
    def __displayFrequencies(self):
        """This will show a popup window detailing the imported frequencies that are going 
        to be used for calculation"""

        if self.FREQUENCIES_FN == '':
            self.status.set("Please load frequencies")
            return

        msg_str = "Frequencies from "+self.FREQUENCIES_FN+":\n\n"+json.dumps(self.__FREQUENCY_DATA.getOrderedDict(), indent=2)
        if self.__FREQUENCY_DATA.unassigned_frequencies != []:
            freqs = self.__FREQUENCY_DATA.unassigned_frequencies
            msg_str += "\n\nWARNING: There are "+str(len(freqs))+" unassigned frequencies:\n"
            msg_str += "\n"+str(self.__FREQUENCY_DATA.unassigned_frequencies)+"\n\n"
            msg_str += "Please consider assigning them and re-load the import file."
        
        messagebox.showinfo("Successfully Imported Frequencies", msg_str)

    def updateView(self, update_fps=True) -> None:
        """This is called whenever the user attempts to load a import file.
        This will ensure that an invalid file is not shown on the screen
        after attempting to be loaded"""

        # Making sure an incrorrect filename is not displayed
        if update_fps:
            if self.WKST_ENTRIES_FN != '':
                self.worksheet_fp.fn.set(os.path.basename(self.WKST_ENTRIES_FN))
            else:
                self.worksheet_fp.reset()
            if self.FREQUENCIES_FN != '':
                self.frequency_fp.fn.set(os.path.basename(self.FREQUENCIES_FN))
            else:
                self.frequency_fp.reset()

        status_str = ""

        # Making sure that if the frequency data is loaded, then only 
        # the name and ID from that file are shown
        cust_id_entry = self.entries.get(CUST_ID)
        name_entry = self.entries.get(CUST_NAME)

        if self.FREQUENCIES_FN != "":

            if cust_id_entry is not None and name_entry is not None:
                if cust_id_entry.getValue() != self.__FREQUENCY_DATA.CUSTOMER_ID or name_entry.getValue() != self.__FREQUENCY_DATA.CUSTOMER_NAME:
                    cust_id_entry.setValue(self.__FREQUENCY_DATA.CUSTOMER_ID)
                    name_entry.setValue(self.__FREQUENCY_DATA.CUSTOMER_NAME)
                    status_str = "Frequency Name/ID has overwritten entered data"

        # Making sure that if the ID is set than the config ID is updated
        
        if cust_id_entry is not None:
            cust_id = cust_id_entry.getValue()
            if cust_id != '':
                config_id_entry = self.entries[CONFIG_ID]
                config_id_entry.entry.config(state=tk.NORMAL)
                config_id_entry.entry.set(str(cust_id)+self.config.VERSION)
                config_id_entry.entry.config(state=tk.DISABLED)


        # Making sure the color box for the worksheet file picker is correct
        try:
            self.getEntryData()
            self.worksheet_color_box.config(bg=READY_COLOR)
        except EntryException as e:
            self.worksheet_color_box.config(bg=NOT_READY_COLOR)
        except Exception as e:
            raise e

        self.status.set(status_str)


    def getEntryData(self, ordered=False):
        """This is called every time the tool needs a dict of all the entries,
        weather it be for saving or calculating. This will loop through all entries,
        make sure they are well-formed, and return a dict with the corresponding data"""
        if ordered:
            data = OrderedDict()
        else:
            data = {}
        for name, entry in self.entries.items():
            if entry.is_required and not entry.isSelected():
                raise EntryException(name, "Required field has not been specified")
            try:
                val = entry.getValue()
                data[name] = val
            except Exception as e:
                raise EntryException(name, str(e))

        return data
    
    def __calculateAndExport(self):
            """This is called every time the user clicks the calculate and export button.
            It will first try to fetch the user entries, and show an error message if not
            all required fields are selected. If the entry data looks good, it will then show
            the CalculationWindow"""

            if self.FREQUENCIES_FN == "":
                self.status.set("Please load frequencies")
                return

            try:
                entry_data = self.getEntryData()
                self.config.ENTRIES_RUNTIME_JSON_STR = json.dumps(self.getEntryData(ordered=True), indent=2)
            except EntryException as e:
                messagebox.showerror("Invalid entries", e.error_msg+"'\n\n'"+e.entry_name+"'")
    
            freq_data = self.__FREQUENCY_DATA
            calculator = WorksheetCalculator(self.config, entry_data, freq_data)
            calculator.calculate()


    def __getDropdownOptions(self, name) -> list:
        """This is called whenever the dropdown options are defined in the config file.
        This will look at the relevent data, and return a list of all possible options
        for the corresponding WorksheetEntry"""
        dropdown_options = []

        if name == "Time Zone":
            dropdown_options = list(self.TIME_ZONE_DATA.keys())
        elif name == "Country":
            dropdown_options = list(self.LOCATION_DATA.keys())
        elif name == "State":
            dropdown_options = list(self.LOCATION_DATA[self.config.DEFAULT_COUNTRY]["states"].keys())
        
        return dropdown_options

    def __setStates(self, eventObj):
        """This is called every time the user selects a different country.
        Because each country has different states, the dropdown options for the state
        WorksheetEntry must be updated"""
        country = self.entries["Country"].getValue()
        dropdown_options = []
        dropdown_options = list(self.LOCATION_DATA[country]["states"].keys())
        self.entries["State"].combobox.config(values=dropdown_options)
        self.entries["State"].combobox.current(0)                
    
    # Menubar that will be modified
    def create_menubar(self, parent):
        menubar = tk.Menu(parent, bd=3, relief=tk.RAISED, activebackground="#80B9DC")
        ## Filemenu
        filemenu = tk.Menu(menubar, tearoff=0, relief=tk.RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.quit)  

        ## proccessing menu
        save_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="TBD", menu=save_menu)

        ## help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About")
        return menubar

    

        

 