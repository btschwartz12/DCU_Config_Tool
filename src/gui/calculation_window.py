# calculation_window.py
# 6/20/22
# Ben Schwartz
#
# Holds the CalculationWindow, which is the GUI for the 
# DCU XML generator.

from datetime import date, datetime
from enum import Enum
import json
import os
from re import L
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from typing import OrderedDict
from config.config import Config
from src.gui.wkst_status_entry import WorksheetStatusEntry
from src.processing.calc_steps.freqs_generator import FrequencyData
from src.processing.calc_steps.status_generator import Status, StatusEntryName
from src.processing.calc_steps.xml_generator import ExportData, getXMLstr
from src.processing.wkst_calculator import StatusData, WorksheetCalculator

DIMENSIONS = "800x315"

class CalculationWindow(tk.Toplevel):
    """This is the window that is shown every time the user has successfully loaded their
    entries and frequencies. THis will show the status of the configuration, generate the output XML,
    and export it accordingly."""
    def __init__(self, config: Config, entry_data, frequency_data: FrequencyData):
        tk.Toplevel.__init__(self)
        self.config = config

        self.entry_data = entry_data
        self.FREQUENCY_DATA: FrequencyData = frequency_data


        self.__buildGUI()

        self.status.set("Waiting to calculate...")

        self.grab_set()

    def __buildGUI(self):
        """This will setup the view for the window"""
        self.geometry(DIMENSIONS)

        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X)

        tk.Label(top_frame, text="Calculations", font=('Times', 13), bg='pink').pack(fill=tk.X)
        tk.Button(top_frame, text="Calculate", bg='red', command = self.__calculate).pack(fill=tk.X, expand=True)

        status_frame = tk.Frame(self)
        status_frame.pack(fill=tk.BOTH, expand=True, anchor=tk.S)

        self.status_entries = {
            StatusEntryName.HE_CERT_UTILITY: WorksheetStatusEntry(status_frame, self.config, StatusEntryName.HE_CERT_UTILITY.value),
            StatusEntryName.DTLS_CERT: WorksheetStatusEntry(status_frame, self.config, StatusEntryName.DTLS_CERT.value),
            StatusEntryName.DTLS_BYPASS: WorksheetStatusEntry(status_frame, self.config, StatusEntryName.DTLS_BYPASS.value),
            StatusEntryName.DCU_CONFIG: WorksheetStatusEntry(status_frame, self.config, StatusEntryName.DCU_CONFIG.value)
        }

        for entry in self.status_entries.values():
            entry.setValue("waiting...")
            entry.pack(fill=tk.X, padx=5)

        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill=tk.X)

        self.status = tk.StringVar()
        tk.Label(bottom_frame, textvariable=self.status).pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(bottom_frame)
        btn_frame.pack(fill=tk.X, expand=True, anchor=tk.S)
        # btn_frame.grid_rowconfigure(0, weight=1)
        # btn_frame.grid_columnconfigure(0, weight=1, uniform='group1')
        # btn_frame.grid_columnconfigure(1, weight=1, uniform='group1')

        # tk.Button(btn_frame, text="Archive", bg='gray', command=self.__archive).grid(row=0, column=0, sticky=tk.NSEW)
        self.export_btn = tk.Button(btn_frame, text="Export", bg='yellow', command=self.__export)
        self.export_btn.pack(fill=tk.BOTH, expand=True)
        # self.export_btn.grid(row=0, column=1, sticky=tk.NSEW)

    def __calculate(self):
        """This will take the user entries and frequencies, and create an instance of a WorksheetCalculator. 
        The calculator will be able to generate all relevent data pertaining to the creation of the xml. 
        Upon calculations, the calculator will generate the status of the configuration, and present that to the screen."""

        self.calculator = WorksheetCalculator(self.config, self.entry_data, self.FREQUENCY_DATA)
        
        try:
            self.calculator.calculate()
        except Exception as e:
            messagebox.showerror("Error during calculation", "\n\n"+str(e))
            self.destroy()
            return

        self.STATUS_DATA: StatusData = self.calculator.getStatusData()

        self.status_entries[StatusEntryName.HE_CERT_UTILITY].setValue(self.STATUS_DATA.Headend_Certificate_Information_Supplied_by_Utility)
        self.status_entries[StatusEntryName.DTLS_CERT].setValue(self.STATUS_DATA.DTLS_Certificate_Information)
        self.status_entries[StatusEntryName.DTLS_BYPASS].setValue(self.STATUS_DATA.DTLS_Bypass_Allowed)
        self.status_entries[StatusEntryName.DCU_CONFIG].setValue(self.STATUS_DATA.DCU_Configuration)

        self.status_entries[StatusEntryName.HE_CERT_UTILITY].setStatus(self.STATUS_DATA.Headend_Certificate_Information_Supplied_by_Utility_STATUS)
        self.status_entries[StatusEntryName.DTLS_CERT].setStatus(self.STATUS_DATA.DTLS_Certificate_Information_STATUS)
        self.status_entries[StatusEntryName.DTLS_BYPASS].setStatus(self.STATUS_DATA.DTLS_Bypass_Allowed_STATUS)
        self.status_entries[StatusEntryName.DCU_CONFIG].setStatus(self.STATUS_DATA.DCU_Configuration_STATUS)

        export_status: Status = Status.PASS

        for entry in self.status_entries.values():
            if entry.status == Status.FAIL:
                export_status = Status.FAIL
                break
            elif entry.status == Status.WARNING:
                export_status = Status.WARNING

            
        if export_status == Status.PASS:
            self.status.set("Successfully generated XML, ready for export")
            self.export_btn.config(state=tk.NORMAL)
        elif export_status == Status.WARNING:
            self.status.set("Successfully generated XML, but warning detected. Proceed with caution")
            self.export_btn.config(state=tk.NORMAL)
        elif export_status == Status.FAIL:
            self.status.set("Illegal status detected, cannot generate XML")
            self.export_btn.config(state=tk.DISABLED)

    def __archive(self, dir, time_str, time_fn_str, xml_str):
        """This will take all of the input / export data from the current tool instance
        and store in a folder, for future access

            - XML
            - freqs used
            - user entries
            - status
        """
        entry_fn = os.path.join(dir, 'USER_ENTRIES.json')
        with open(entry_fn, 'w+') as f:
            data = json.loads(self.config.ENTRIES_RUNTIME_JSON_STR)
            data["@generated"] = time_str
            json.dump(data, f, indent=2)

        freq_fn = os.path.join(dir, 'FREQUENCIES.json')
        with open(freq_fn, 'w+') as f:
            if self.config.FREQUENCY_RUNTIME_JSON_STR == "":
                raise Exception("error 336: cannot find frequency data")
            data = json.loads(self.config.FREQUENCY_RUNTIME_JSON_STR)
            data.append({"@generated": time_str})
            json.dump(data, f, indent=2)

        status_fn = os.path.join(dir, "STATUS.json")
        with open(status_fn, 'w+') as f:
            data = self.STATUS_DATA.getData()
            data["@generated"] = time_str
            json.dump(data, f, indent=2)

        xml_fn = os.path.join(dir, "DCU2+XLS_"+time_fn_str+".xml")
        with open(xml_fn, 'w+') as f:
            f.write(xml_str)

        
            
    def __export(self):
        """This will take the previously generated data from the calculator and fetch the 
        calculator's ExportData. The ExportData will then be converted to a string, and written
        to a specified file"""
        print("exporting")
        EXPORT_DATA: ExportData = self.calculator.getExportData()
        xml_str = getXMLstr(EXPORT_DATA, self.config)

        question_str =  "Yes - create an archive folder containing:\n"
        question_str += "\t- generated DCU2+XLS .xml file\n"
        question_str += "\t- frequency data .json file\n"
        question_str += "\t- entered data .json file\n"
        question_str += "\t- status .json file\n"
        question_str += "\nNo - only export generated DCU2+XLS .xml file"

        user_wants_archive = messagebox.askyesno("Archive?", question_str)

        now = datetime.now()
        datetime_fn_str = now.strftime('%Y%m%d-%H%M%S')
        datetime_str = now.strftime('%Y/%m/%d-%H:%M:%S')

        if user_wants_archive:
            
            

            # messagebox.showinfo("Archive Created", "An archive folder has been created in:\n\n"+os.path.dirname(initial_dir_path)+"\n\nWith the name:\n\n"+os.path.basename(initial_dir_path)+"\n\n"+"Click OK, and select a destination for the archive folder.")

            archive_parent_dir = filedialog.askdirectory(title='Select Archive Destination', initialdir=self.config.SRC_DIR)

            if archive_parent_dir is not None:
                
                archive_dir = os.path.join(archive_parent_dir, "DCU2+XLS_Archive_"+datetime_fn_str)
                os.mkdir(archive_dir)

                self.__archive(archive_dir, datetime_str, datetime_fn_str, xml_str)
                messagebox.showinfo("Successfully archived and exported", "Successfully written archive and export files to:\n\n"+archive_dir)
                self.destroy()
        else:
            fn = "DCU2+XLS_"+datetime_fn_str
            name = asksaveasfile(mode='w', defaultextension='.xml', initialfile=fn, initialdir=self.config.SRC_DIR).name
            if name is not None:
                with open (name, 'w+') as f:
                    f.write(xml_str)
                messagebox.showinfo("Successfully exported", "Successfully written export file to:\n\n"+fn)
                self.destroy()
            


