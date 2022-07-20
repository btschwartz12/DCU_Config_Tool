
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

# Have 2 mutually exclusive checkboxes
# make is_editable do something

COLORS = ('#00137C', 'black')

class WorksheetEntry(tk.Frame):
    """This represents each row of the Customer Worksheet entry page. 
    Each WorksheetEntry will have a name, a type (EntryType), and flags 
    indicating weather or not it is editable or required. For entries that
    have dropdown options, those are passed along in the constructor as well"""
    def __init__(self, master, DCU_PAGE, config: Config, name: str, entry_type: EntryType, editable:bool, required:bool, dropdown_options, count=None, comment=None):
        tk.Frame.__init__(self, master)
        self.config: Config = config 
        
        self.name: str = name # Name shown on right side
        self.type: EntryType = entry_type # The type of entry
        self.is_editable: bool = editable 
        self.is_required: bool = required

        self.DCU_PAGE = DCU_PAGE

        self.status: tk.StringVar = DCU_PAGE.status # Gives access to the DCU pages' status variable
        
        # Optional parameters
        self.comment=comment # Comment from the worksheet, will be shown with info button
        self.dropdown_options = dropdown_options # If possible dropdown options can be provided


        self.count = count # The count of the entry related to the other entries, used for printing count and alternating colors
        
        if count % 2 == 0: # For better readibility
            self.color_str = COLORS[0]
        else:
            self.color_str = COLORS[1]

        self.__buildGUI()

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

    def __updateCheckbox(self, event=None):
        """This is called every time the checkbox is clicked, and will
        update the checkbox"""
        if self.type == EntryType.BOOLEAN:
            pass
            # self.checkbox_str.set("Yes" if self.entry.get() else "No")
        else:
            print("error 770")
    
    def updateColorBox(self):
        self.DCU_PAGE.updateEntryColorBox()

    def __buildEntryFrame(self):
        """This is called during __buildGUI(), and will look at the EntryType of the entry and
        build the corresponding view. All EntryType's will still have a self.entry variable that 
        is used for further calculations"""
        if self.type == EntryType.STRING:
            self.entry = AutoSelectEntry(self.entry_frame, foreground=self.color_str, command=self.updateColorBox, justify='center')
            self.entry.pack(fill=tk.BOTH, expand=True)
        
        elif self.type == EntryType.BOOLEAN:
            self.entry = tk.IntVar()
            btn_frame = tk.Frame(self.entry_frame)
            btn_frame.pack()
            tk.Radiobutton(btn_frame, text="Yes", variable=self.entry, value=1, command=self.__updateCheckbox, fg=self.color_str).pack(side=tk.LEFT)
            tk.Radiobutton(btn_frame, text="No", variable=self.entry, value=0, command=self.__updateCheckbox, fg=self.color_str).pack(side=tk.LEFT)
        
        elif self.type == EntryType.DROPDOWN:
            self.entry = tk.StringVar()
            
            self.combobox = ttk.Combobox(self.entry_frame, textvariable=self.entry, justify=tk.CENTER, values=self.dropdown_options, foreground=self.color_str, state='readonly')
            self.combobox.option_add('*TCombobox*Listbox.Justify', 'center')
            self.combobox.unbind_class("TCombobox", "<MouseWheel>")
            self.combobox.pack(fill=tk.BOTH, expand=True)
            self.combobox.current(0)

        elif self.type == EntryType.NUMBER:
            self.entry = AutoSelectEntry(self.entry_frame, foreground=self.color_str, command=self.__checkEntryIsInt, justify='center')
            self.entry.pack(fill=tk.BOTH, expand=True)
            
    def __checkEntryIsInt(self, event=None):
        """This is called every time the user puts a value in an entry that has
        an number EntryType. If the input is not a number, then the entry is 
        made blank and the DCU_page status variable is set to a error message"""
        val = self.entry.get()
        if val == "":
            return
        if not isInt(val):
            self.status.set(self.name+" must have an integer input")
            self.entry.set("")
        else:
            self.status.set("")
        self.updateColorBox()
        
    def getValue(self):
        """This is called every time the user finishes putting in their entries,
        and the entries need to be exported for future use. Depending on the
        EntryType, the value will be returned"""
        if self.type == EntryType.STRING:
            return self.entry.get()
        elif self.type == EntryType.BOOLEAN:
            return bool(self.entry.get())
        elif self.type == EntryType.DROPDOWN:
            if self.entry.get() == 1: # Yes
                return True
            else: # No
                return False
        elif self.type == EntryType.NUMBER:
            self.__checkEntryIsInt()
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
                self.entry.set(not bool(value))
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
            
            


class WorksheetStatusEntry(tk.Frame):
    """This is the view that is shown in the calculation window, 
    which dictates a certain status for the configuration.
    
    WORK IN PROGRESS"""


    def __init__(self, master_frame, controller, name: str):
        tk.Frame.__init__(self, master_frame)
        self.controller = controller
        self.name = name
        

        # style = ttk.Style()
        # self.option_add('*TCombobox*Listbox.foreground', self.color_str)
        # style.configure("Colored.TCombobox", foreground=self.color_str)


        self.__buildGUI()

    def __buildGUI(self):

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.X)

        main_frame.columnconfigure(0, weight=1, uniform='group1')
        main_frame.columnconfigure(1, weight=1, uniform='group1')
        main_frame.rowconfigure(0, weight=1)

        
        # Name
        name_frame = tk.Frame(main_frame)
        name_frame.grid(row=0, column=0, sticky=tk.EW, padx=(0,5))
        
        
        tk.Label(name_frame, text=self.name, font=('Times',9)).pack(side=tk.LEFT)

        # Entry frame
        entry_frame = tk.Frame(main_frame, bg='green')
        entry_frame.grid(row=0, column=1, sticky=tk.EW, padx=5)

        self.entry_box = tk.Text(entry_frame, background='green', foreground='white', height=3)
        self.entry_box.config(state=tk.DISABLED)
        self.entry_box.pack(fill=tk.X, side=tk.LEFT)


    def setValue(self, value):
        self.entry_box.config(state=tk.NORMAL)
        self.entry_box.delete('1.0', tk.END)
        self.entry_box.insert('1.0', value)
        self.entry_box.config(state=tk.DISABLED)
        