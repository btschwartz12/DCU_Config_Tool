
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



from src.utils.filepicker import AutoSelectEntry
from src.utils.utils import EntryType, isInt



# Have 2 mutually exclusive checkboxes

class WorksheetEntry(tk.Frame):
    def __init__(self, master, dcu_page, controller, name: str, entry_type: EntryType, editable:bool, required:bool, dropdown_options, count=None, comment=None):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.name = name
        self.type = entry_type
        self.is_ediable = editable
        self.is_required = required
        self.status = dcu_page.status
        self.comment=comment
        if dropdown_options is not None:
            self.dropdown_options = dropdown_options


        self.count = count
        
        if count % 2 == 0:
            self.color_str = '#00137C'
        else:
            self.color_str = 'black'

        # style = ttk.Style()
        # self.option_add('*TCombobox*Listbox.foreground', self.color_str)
        # style.configure("Colored.TCombobox", foreground=self.color_str)


        self.__buildGUI()

    def __buildGUI(self):

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.X, expand=True, side=tk.LEFT)

        main_frame.columnconfigure(0, weight=1, uniform='group1')
        main_frame.columnconfigure(1, weight=1, uniform='group1')
        main_frame.rowconfigure(0, weight=1)

        
        # Name
        name_frame = tk.Frame(main_frame)
        name_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=(0,5))
        
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
        self.__buildEntryFrame()

        # Help button
        info_button = tk.Button(self, text='i', fg='blue', command=self.help)
        info_button.config(command=self.help)
        info_button.pack(expand=False, side=tk.RIGHT)


    def help(self):
        help_str = ""

        if self.comment is None:
            help_str = "No addidional information exists for "+self.name
            if not self.is_required:
                help_str = self.name+" is OK to leave empty"
        else:
            help_str = self.comment

        messagebox.showinfo("Entry Information", help_str)

    def updateValue(self, event=None):
        if self.type == EntryType.STRING:
            pass
        elif self.type == EntryType.BOOLEAN:
            
            self.checkbox_str.set("Yes" if self.entry.get() else "No")

        elif self.type == EntryType.DROPDOWN:
            pass
        elif self.type == EntryType.NUMBER:
            pass

    def __buildEntryFrame(self):

        if self.type == EntryType.STRING:
            self.entry = AutoSelectEntry(self.entry_frame, foreground=self.color_str, justify='center')
            self.entry.pack(fill=tk.BOTH, expand=True)
        
        elif self.type == EntryType.BOOLEAN:
            self.entry = tk.IntVar()
            self.checkbox_str = tk.StringVar()
            self.checkbox_str.set("No")
            tk.Checkbutton(self.entry_frame, variable=self.entry, command=self.updateValue, textvariable=self.checkbox_str, fg=self.color_str).pack(fill=tk.BOTH, expand=True)
        
        elif self.type == EntryType.DROPDOWN:
            self.entry = tk.StringVar()
            
            self.combobox = ttk.Combobox(self.entry_frame, textvariable=self.entry, justify=tk.CENTER, values=self.dropdown_options, foreground=self.color_str, state='readonly')
            self.combobox.option_add('*TCombobox*Listbox.Justify', 'center')
            self.combobox.unbind_class("TCombobox", "<MouseWheel>")
            self.combobox.pack(fill=tk.BOTH, expand=True)
            self.combobox.current(0)

        elif self.type == EntryType.NUMBER:
            self.entry = AutoSelectEntry(self.entry_frame, foreground=self.color_str, command=self.checkEntryIsInt, justify='center')
            self.entry.pack(fill=tk.BOTH, expand=True)
            
    def checkEntryIsInt(self, event=None):
        val = self.entry.get()
        if val == "":
            return
        if not isInt(val):
            self.status.set(self.name+" must have an integer input")
            self.entry.set("")
        else:
            self.status.set("")
        
    def getValue(self):
        if self.type == EntryType.STRING:
            return self.entry.get()
        elif self.type == EntryType.BOOLEAN:
            return bool(self.entry.get())
        elif self.type == EntryType.DROPDOWN:
            return self.entry.get()
            
        elif self.type == EntryType.NUMBER:
            self.checkEntryIsInt()
            return int(self.entry.get())

    def isSelected(self):
        if self.type == EntryType.STRING:
            return self.entry.get() != ""
        elif self.type == EntryType.BOOLEAN:
            return True
        elif self.type == EntryType.DROPDOWN:
            return True
        elif self.type == EntryType.NUMBER:
            return self.entry.get() != ""

    def setValue(self, value):
        if self.type == EntryType.STRING:
            self.entry.set(value)
        elif self.type == EntryType.BOOLEAN:
            try:
                self.entry.set(bool(value))
                self.checkbox_str.set("Yes" if value else "No")
            except ValueError:
                raise Exception("error 321: "+str(value)+" is not a boolean value")
        elif self.type == EntryType.DROPDOWN:
            if value not in self.dropdown_options:
                raise Exception("error 322: "+str(value)+" is not a valid option for "+self.name)
            self.entry.set(value)
            
        elif self.type == EntryType.NUMBER:
            try:
                self.entry.set(int(value))
            except ValueError as e:
                raise Exception("error 323: "+str(value)+" is not an integer\n\n"+str(e))


class WorksheetStatusEntry(tk.Frame):
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

        # # Help button
        # info_button = tk.Button(self, text='i', fg='blue', command=self.help)
        # info_button.config(command=self.help)
        # info_button.pack(expand=False, side=tk.RIGHT)

    def help(self):
        pass


    def setValue(self, value):
        self.entry_box.config(state=tk.NORMAL)
        self.entry_box.delete('1.0', tk.END)
        self.entry_box.insert('1.0', value)
        self.entry_box.config(state=tk.DISABLED)
        