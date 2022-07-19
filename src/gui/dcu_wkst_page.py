
# GUI

from datetime import datetime
import json
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile

from click import edit
from config.config import Config

from src.gui.calculation_window import CalculationWindow

from src.gui.wkst_entry import WorksheetEntry
from src.utils.filepicker import FilePicker
from src.utils.scrollframe import VerticalScrolledFrame
from src.utils.utils import EntryType


DEFAULT_COUNTRY = "United States"

LOCATION_DATA_FN = "data/location_data.json"
TIME_ZONE_DATA_FN = "data/time_zone_data.json"

class EntryException(Exception):
    def __init__(self, name, msg):
        self.entry_name = name
        self.error_msg = msg


wkst_config = {}
with open('config/wkst_config.json', 'r') as f:
    wkst_config.update(json.load(f))

class DcuWorksheetPage(tk.Frame):
    def __init__(self, master, config: Config):
        tk.Frame.__init__(self, master)
        self.config = config

        self.WKST_FN = ""

        self.LOCATION_DATA = {}
        self.TIME_ZONE_DATA = {}

        with open(LOCATION_DATA_FN, 'r') as f:
            self.LOCATION_DATA.update(json.load(f))
        with open(TIME_ZONE_DATA_FN, 'r') as f:
            self.TIME_ZONE_DATA.update(json.load(f))

        self.entries = {}
        self.status = tk.StringVar()

        self.__buildGUI()

    def __buildGUI(self):

        """Top view holds the name of the reading"""
        top_frame = tk.Frame(self)
        tk.Label(top_frame, text="Customer Worksheet", font=('Times', 15)).pack()

        self.file_picker = FilePicker(top_frame, self, title="Worksheet Import", extension='json', command=self.loadFile)
        self.file_picker.pack(fill=tk.X, padx=20, pady=(5,15))

        file_dir = 'data/wkst_entries'
        self.file_picker.loadDir(file_dir)

        

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
        tk.Button(bottom_frame, text="Calculate & Export", command=self.__calculateAndExport, bg='yellow').pack(fill=tk.X, expand=True, anchor=tk.S)

        self.__loadEntries()

    def __calculateAndExport(self):

        try:
            entry_data = self.getEntryData()
            window = CalculationWindow(self, self.config, entry_data)
            window.mainloop()
        except EntryException as e:
            messagebox.showerror("Failed to fetch entry data", "'"+e.entry_name+"'\n\n"+e.error_msg)
        


    def loadFile(self, fn=None):
        
        if fn is None:
            fn = self.file_picker.getSelectedFilePath()

        self.WKST_FN = fn

        data = {}
        with open(fn, 'r') as f:
            data = json.load(f)
            
        self.initEntries(data)

        
    def initEntries(self, data):
        
        for name, value in data.items():
            try:
                self.entries[name].setValue(value)
            except Exception as e:
                raise e
            
        self.update()



    def __loadEntries(self):

        entries = self.config.ENTRIES
        dropdowns = self.config.DROPDOWN_OPTIONS
        self.states_by_country = dropdowns["State"]

        for i, entry in enumerate(entries):
            
            name = entry["name"]
            entry_type = EntryType(entry["type"])
            is_editable = bool(entry["editable"])
            is_required = bool(entry["required"])
            comment = entry.get("comment")
            dropdown_options = None


            if entry_type == EntryType.DROPDOWN:
                try:
                    dropdown_options = dropdowns[name]
                except Exception as e:
                    raise Exception("error 892: cannot find dropdown options for "+name)

                if dropdown_options is None: # This means the options are defined in a config file
                    dropdown_options = self.getDropdownOptions(name)
                    


            entry_frame = WorksheetEntry(self.main_display, self, self.config, name, entry_type, is_editable, is_required, dropdown_options, count=(i+1), comment=comment)

            self.entries[name] = entry_frame

            entry_frame.pack(fill=tk.X, padx=(5, 20))

        self.entries["Country"].combobox.bind("<<ComboboxSelected>>", self.setStates)

        if self.config.DEBUG_MODE == True:
            self.loadFile(self.config.DEBUG_SAMPLE_ENTRIES_JSON_RPATH)

    def getDropdownOptions(self, name) -> list:
        dropdown_options = []

        if name == "Time Zone":
            dropdown_options = list(self.TIME_ZONE_DATA.keys())
        elif name == "Country":
            dropdown_options = list(self.LOCATION_DATA.keys())
        elif name == "State":
            dropdown_options = list(self.LOCATION_DATA[DEFAULT_COUNTRY]["states"].keys())
        
        return dropdown_options

    def setStates(self, eventObj):
        country = self.entries["Country"].getValue()
        dropdown_options = []
        dropdown_options = list(self.LOCATION_DATA[country]["states"].keys())
        self.entries["State"].combobox.config(values=dropdown_options)
        self.entries["State"].combobox.current(0)

    def getEntryData(self):

        if self.config.DEBUG_MODE == True:
            return {}
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

    def logout(self):
        print("logout")

    def saveCurrent(self):
        data = self.getEntryData()
        
        with open(self.WKST_FN, 'w') as f:
            json.dump(data, f, indent=4)
            print("successfully written to "+self.WKST_FN)

    def saveAs(self):
        data = self.getEntryData()
        
        now = datetime.now()
        fn = "CustomerWorksheet_"+str(now.strftime('%Y%m%d-%H%M%S'))

        name = asksaveasfile(mode='w', defaultextension='.json', initialfile=fn, initialdir='C:/Users/70060/Documents/SRFN_Config_Tool/').name

        if name is not None:
            with open(name, 'w') as f:
                json.dump(data, f, indent=4)
                print("successfully written to "+name)

    # Menubar that will be modified
    def create_menubar(self, parent):
        menubar = tk.Menu(parent, bd=3, relief=tk.RAISED, activebackground="#80B9DC")
        ## Filemenu
        filemenu = tk.Menu(menubar, tearoff=0, relief=tk.RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Logout", command=self.logout) 
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.quit)  

        ## proccessing menu
        save_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Save", menu=save_menu)
        save_menu.add_command(label="Save Current", command=self.saveCurrent)
        save_menu.add_separator()
        save_menu.add_command(label="Save As", command=self.saveAs)
        

        ## help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About")
        return menubar

    

        

 


    

