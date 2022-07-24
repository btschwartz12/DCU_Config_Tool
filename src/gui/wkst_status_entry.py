# wkst_status_entry.py
# 6/20/22
# Ben Schwartz
#
# Holds the WorksheetEntry, which is a view
# for each row of the first page.

from enum import Enum
import tkinter as tk

from src.processing.calc_steps.status_generator import Status


class WorksheetStatusEntry(tk.Frame):
    """This is the view that is shown in the calculation window, 
    which dictates a certain status for the configuration.
    
    WORK IN PROGRESS"""


    def __init__(self, master_frame, controller, name: str):
        tk.Frame.__init__(self, master_frame)
        self.controller = controller
        self.name = name
        

        self.status: Status


        self.__buildGUI()

    def __buildGUI(self):

        # Main view
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill=tk.BOTH)
        main_frame.columnconfigure(0, weight=1, uniform='group1')
        main_frame.columnconfigure(1, weight=1, uniform='group1')
        main_frame.rowconfigure(0, weight=1)
        # Status name
        name_frame = tk.Frame(main_frame)
        name_frame.grid(row=0, column=0, sticky=tk.EW, padx=(0,5))
        tk.Label(name_frame, text=self.name, font=('Times',9)).pack(side=tk.LEFT)
        # Status value
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

    def setStatus(self, status: Status):
        self.status = status
        self.entry_box.config(state=tk.NORMAL)
        self.entry_box.config(background=status.value[0], foreground=status.value[1])
        self.entry_box.config(state=tk.DISABLED)

    
        