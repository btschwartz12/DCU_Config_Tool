import os
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror

# Misc
from functools import partial

from config.config import Config


class FilePicker(tk.Frame):
    def __init__(self, frame, config: Config, title, extension, command=None, **kwargs):
        
        tk.Frame.__init__(self, frame, **kwargs)
        self.command = command # See runCommand()
        self.extension = extension
        self.config: Config = config
        self.buildGUI(title)

    
    def getSelectedFilePath(self):
        path = os.path.join(self.folder_entry.get(), self.fn.get())
        return path

    def getExtensionStr(self):
        s = ""
        if isinstance(self.extension, tuple):
            for ext in self.extension:
                s += ext + ' or '
            s = s[:len(s)-4]
        else:
            s = self.extension
        return s

    def buildGUI(self, title):
        
        # Label setup
        frame = tk.Frame(self)
        frame.pack(fill=tk.X, expand=tk.TRUE)

        tk.Label(frame, text=title, fg='blue').pack(fill=tk.X, anchor=tk.N)

        selection_frame = tk.Frame(self)
        frame = tk.Frame(selection_frame)
        frame.pack(fill=tk.X, expand=tk.TRUE)
        self.folder_entry = AutoSelectEntry(frame, command=self.browse)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=tk.TRUE)
        self.browse_btn = ttk.Button(frame, text='...', width=3, command=self.browse)
        self.browse_btn.pack(side=tk.LEFT)

        frame = tk.Frame(selection_frame)
        frame.pack(fill=tk.X, expand=tk.TRUE)
        self.fn = tk.StringVar()
        self.reset()
        self.filemenu = ttk.OptionMenu(frame, self.fn)
        self.filemenu.pack(side=tk.LEFT, fill=tk.X, expand=True)

        selection_frame.pack(fill=tk.X, expand=tk.TRUE)

        # Validate button
        self.validate_btn = ttk.Button(frame, text="Load", command=self.command)
        self.validate_btn.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.TRUE)

    def reset(self):
        self.fn.set("Select a "+self.getExtensionStr()+" file")

    def is_selected(self):
        cur_fn = self.fn.get()
        blank_fn = "Select a "+self.getExtensionStr()+" file"
        return cur_fn != blank_fn

    def disable(self):

        self.filemenu['state'] = 'disabled'
        self.folder_entry['state'] = 'disabled'
        self.validate_btn['state'] = 'disabled'
        
    def enable(self):
        self.filemenu['state'] = 'normal'
        self.folder_entry['state'] = 'normal'
        self.validate_btn['state'] = 'normal'

    # This function allows us to run a particular function when a file
    # is selected from the dropdown menu, for now, it is just load_file() from NicConfigPage class
    # A command is not necessarily needed, just helpful if needed in the future
    def runCommand(self, filename):


        # if self.command: # If there is a command, run it
        #     self.command(os.path.join(self.folder_entry.get(), filename))
        self.fn.set(filename) # Update view to show filename

        
    # This is the command binded to the '...' button, asks the user to 
    # select a directory, then will call loadDir() for that directory
    def browse(self, dir=None):
        if dir is None:
            dir = askdirectory(initialdir=self.config.SRC_DIR)
        if dir: # check for user cancelled
            try:
                self.loadDir(dir)
            except Exception as e:
                showerror("error", "%s is not a valid directory.\n%s"%(dir, e))
                self.folder_entry.delete(0, tk.END)
                self.folder_entry.insert(0, self.config.SRC_DIR)


    # This function will load the user-specified directory, update the view,
    # then find all xsd/xml files in that directory and add them to the
    # drop down menu
    def loadDir(self, dir):
        fns = os.listdir(dir)


        # Update directory selection view and get all XSD files
        self.folder_entry.set(dir)
        dir = [fn for fn in fns if fn.endswith(self.extension)]
        # Add files to the dropdown
        self.filemenu['menu'].delete(0, tk.END)
        for file in dir:
            self.filemenu['menu'].add_command(label=file, command=partial(self.runCommand, file))
        
        self.reset()


class AutoSelectEntry(ttk.Entry):

	elements = []

	def __init__(self, master, command=None, **kwargs):
		"""Entry widget that auto selects when focused
		command is a function to execute on value change"""
		ttk.Entry.__init__(self, master, **kwargs)
		self.command = command
		self.old_value = None
		self.elements.append(self)
		self.dirty = False

		self.bind('<FocusIn>', self.select_all)
		self.bind('<Return>', self.input_change)
		self.bind('<FocusOut>', self.input_change)

	def select_all(self, event=None):
		self.selection_range(0, tk.END)

	def input_change(self, event=None, value=None):
		if value is None:
			value = self.get()
		if self.command is not None:
			if value == self.old_value:
				return # check for a change; prevent command trigger when just tabbing through
			self.dirty = True
			self.old_value = value
			try:
				self.command(value)
			except Exception as e:
				raise e
			self.select_all()

	def set(self, text=None, run=False):
		if text is None:
			text = ""
		if len(str(text)) > 500:
			text = "<too long to display>"
		self.delete(0, tk.END)
		self.insert(0, text)
		self.old_value = text
		if run:
			self.input_change(text)
        