# wkst_entry.py
# 6/20/22
# Ben Schwartz
#
# Holds the WorksheetEntry, which is a view
# for each row of the first page.

from enum import Enum
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from config.config import Config
from src.utils.filepicker import AutoSelectEntry
from src.utils.utils import isInt

class EntryType(Enum):
    STRING = "string"
    BOOLEAN = "boolean"
    DROPDOWN = "dropdown"
    NUMBER = "number"

COLORS = ('#00137C', 'black')

class WorksheetEntry(tk.Frame):
    """This represents each row of the Customer Worksheet entry page. 
    Each WorksheetEntry will have a name, a type (EntryType), and flags 
    indicating weather or not it is editable or required. For entries that
    have dropdown options, those are passed along in the constructor as well"""
    def __init__(self, master, DCU_PAGE, config: Config, name: str, entry_type: EntryType, editable:bool, required:bool, dropdown_options, count=None, comment=None, default_value=None):
        tk.Frame.__init__(self, master)
        self.config: Config = config 
        
        self.name: str = name # Name shown on right side
        self.type: EntryType = entry_type # The type of entry
        self.is_editable: bool = editable 
        self.is_required: bool = required

        self.DCU_PAGE = DCU_PAGE

        # Optional parameters
        self.comment=comment # Comment from the worksheet, will be shown with info button
        self.dropdown_options = dropdown_options # If possible dropdown options can be provided


        self.count = count # The count of the entry related to the other entries, used for printing count and alternating colors
        
        if count % 2 == 0: # For better readibility
            self.color_str = COLORS[0]
        else:
            self.color_str = COLORS[1]

        self.__buildGUI()

        if default_value is not None:
            self.setValue(default_value)

    def __buildGUI(self):
        """This will create the view that holds the WorksheetEntry,
        including the name, entry spot, and info button"""
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.X, expand=True, side=tk.LEFT)
        # So there can be two equally sized halves
        main_frame.columnconfigure(0, weight=1, uniform='group1')
        main_frame.columnconfigure(1, weight=1, uniform='group1')
        main_frame.rowconfigure(0, weight=1)
        # Name
        name_frame = tk.Frame(main_frame)
        name_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=(0,5))
        # Getting name formatted prettily
        count_str = ""
        if self.count is not None:
            count_str = str(self.count)+".  "
            if self.count < 10:
                count_str += '  '
        name_str = count_str + self.name
        if not self.is_required:
            name_str += " (optional)"
        tk.Label(name_frame, text=name_str, font=('Times', 11), fg=self.color_str).pack(side=tk.LEFT)
        # Entry frame
        self.entry_frame = tk.Frame(main_frame)
        self.entry_frame.grid(row=0, column=1, sticky=tk.NSEW, padx=5)
        self.__buildEntryFrame() # Since different EntryTypes' are structured differently
        # Help button
        info_button = tk.Button(self, text='i', fg='blue', command=self.__help)
        info_button.config(command=self.__help)
        info_button.pack(expand=False, side=tk.RIGHT)

    def __buildEntryFrame(self):
        """This is called during __buildGUI(), and will look at the EntryType of the entry and
        build the corresponding view. All EntryType's will still have a self.entry variable that 
        is used for further calculations"""
        if self.type == EntryType.STRING:
            self.entry = AutoSelectEntry(self.entry_frame, foreground=self.color_str, command=self.updateValue, justify='center')
            self.entry.pack(fill=tk.BOTH, expand=True)
            if not self.is_editable:
                self.entry.config(state=tk.DISABLED)
                self.entry.bind('<Double-Button-1>', self.__showEditWarningMessage)
        
        elif self.type == EntryType.BOOLEAN:
            self.entry = tk.IntVar()
            btn_frame = tk.Frame(self.entry_frame)
            btn_frame.pack()
            self.yes_btn = tk.Radiobutton(btn_frame, text="Yes", variable=self.entry, value=1, fg=self.color_str)
            self.yes_btn.pack(side=tk.LEFT)
            self.no_btn = tk.Radiobutton(btn_frame, text="No", variable=self.entry, value=0, fg=self.color_str)
            self.no_btn.pack(side=tk.LEFT)

        elif self.type == EntryType.DROPDOWN:
            self.entry = tk.StringVar()
            
            self.combobox = ttk.Combobox(self.entry_frame, textvariable=self.entry, justify=tk.CENTER, values=self.dropdown_options, foreground=self.color_str, state='readonly')
            self.combobox.option_add('*TCombobox*Listbox.Justify', 'center')
            self.combobox.unbind_class("TCombobox", "<MouseWheel>")
            self.combobox.pack(fill=tk.BOTH, expand=True)
            self.combobox.current(0)

        elif self.type == EntryType.NUMBER:
            self.entry = AutoSelectEntry(self.entry_frame, foreground=self.color_str, command=self.updateValue, justify='center')
            self.entry.pack(fill=tk.BOTH, expand=True)
            if not self.is_editable:
                self.entry.config(state=tk.DISABLED)
                self.entry.bind('<Double-Button-1>', self.__showEditWarningMessage)
            
    def __checkEntryIsInt(self, event=None):
        """This is called every time the user puts a value in an entry that has
        an number EntryType. If the input is not a number, then the entry is 
        made blank and the DCU_page status variable is set to a error message"""
        val = self.entry.get()
        if val == "":
            return
        if not isInt(val):
            self.entry.set("")
            messagebox.showerror("Invalid entry", self.name+" must have an integer input")
        else:
            if not self.is_editable:
                self.entry.config(state=tk.NORMAL)
            if self.entry.get() != "":
                self.entry.set(int(val))
            if not self.is_editable:
                self.entry.config(state=tk.DISABLED) 
            
        
    def getValue(self):
        """This is called every time the user finishes putting in their entries,
        and the entries need to be exported for future use. Depending on the
        EntryType, the value will be returned"""
        if self.type == EntryType.STRING:
            return self.entry.get()
        elif self.type == EntryType.BOOLEAN:
            return bool(self.entry.get())
        elif self.type == EntryType.DROPDOWN:
            return self.entry.get()
        elif self.type == EntryType.NUMBER:
            if not isInt(self.entry.get()):
                self.entry.set('')
                return ''
            return int(self.entry.get())

    def isSelected(self):
        """This is called to confirm that each entry  
        is actually selected, before exporting the selections"""
        if self.type == EntryType.STRING:
            return self.entry.get() != ""
        elif self.type == EntryType.BOOLEAN:
            return True
        elif self.type == EntryType.DROPDOWN:
            return True
        elif self.type == EntryType.NUMBER:
            return self.entry.get() != ""

    def updateValue(self, value):
        """This is called every time a entry containing a string or number
        is changed. This allows non-editable fields to be correctly updated"""
        if self.type == EntryType.STRING:
            if not self.is_editable:
                self.entry.config(state=tk.NORMAL)
            self.entry.set(value)
            if not self.is_editable:
                self.entry.config(state=tk.DISABLED)

        elif self.type == EntryType.NUMBER:
            self.__checkEntryIsInt()

        self.DCU_PAGE.updateView(update_fps=False)

    def setValue(self, value):
        """This is called every time the user imports a previous
        configuration, and will fill in the entry appropriately"""
        if self.type == EntryType.STRING:
            if not self.is_editable:
                self.entry.config(state=tk.NORMAL)
            self.entry.set(value)
            if not self.is_editable:
                self.entry.config(state=tk.DISABLED)
        elif self.type == EntryType.BOOLEAN:
            try:
                self.entry.set(bool(value))
            except ValueError:
                raise Exception("error 321: "+str(value)+" is not a boolean value")
        elif self.type == EntryType.DROPDOWN:
            if value not in self.dropdown_options:
                raise Exception("error 322: "+str(value)+" is not a valid option for "+self.name)
            self.entry.set(value)
            
        elif self.type == EntryType.NUMBER:
            if not isInt(value):
                raise Exception("error 323: "+str(value)+" is not an integer\n\n")
            
            if not self.is_editable:
                self.entry.config(state=tk.NORMAL)
            self.entry.set(int(value))
            if not self.is_editable:
                self.entry.config(state=tk.DISABLED)

        
    def __help(self):
        """This dictates what is shown when the user clicks the info
        button. If there is a comment provided with the entry,
        that is shown. If not, a unhelpful message is shwon"""
        help_str = ""

        if self.comment is None:
            help_str = "No addidional information exists for "+self.name
            if not self.is_required:
                help_str = self.name+" is OK to leave empty"
        else:
            help_str = self.comment

        messagebox.showinfo("Entry Information", help_str)

    def __showEditWarningMessage(self, event=None):
        """This will allows the user to edit non-editable fields, but shows a warning message before
        enabling. The tool version or customer configuration ID still cannot be edited."""
        
        if self.name == "Tool Version" or self.name == "Customer Configuration Id":
            return
        messagebox.showwarning("Warning", "You may now edit this field.\n\nPlease ensure this directly corresponds to the frequency file.")
        self.entry.config(state=tk.NORMAL)

        
            
            


