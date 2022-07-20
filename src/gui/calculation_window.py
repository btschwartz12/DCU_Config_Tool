from datetime import datetime
import json
import tkinter as tk
from tkinter.filedialog import asksaveasfile
from config.config import Config
from src.processing.calc_steps.freqs_generator import FrequencyData
from src.processing.export_xml import ExportData, getXMLstr
from src.processing.wkst_calculator import StatusData, WorksheetCalculator

from src.gui.wkst_entry import WorksheetStatusEntry


dimensions="700x400"
CONFIG_FN = "config/wkst_config.json"



WKST_CONFIG = {}
with open(CONFIG_FN, 'r') as f:
    WKST_CONFIG.update(json.load(f))

class CalculationWindow(tk.Toplevel):
    """This is the window that is shown every time the user has successfully loaded their
    entries and frequencies. THis will show the status of the configuration, generate the output XML,
    and export it accordingly"""
    def __init__(self, DCU_PAGE, config: Config, entry_data, frequency_data: FrequencyData):
        tk.Toplevel.__init__(self)
        self.config = config

        self.DCU_PAGE = DCU_PAGE
        self.entry_data = entry_data
        self.FREQUENCY_DATA: FrequencyData = frequency_data


        self.__buildGUI()

        self.status.set("Waiting to calculate...")

        self.grab_set()

    def __buildGUI(self):
        """This will setup the view for the window"""
        self.geometry(dimensions)

        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X)

        tk.Label(top_frame, text="Calculations", font=('Times', 13), bg='pink').pack(fill=tk.X)
        tk.Button(top_frame, text="Calculate", bg='red', command = self.__calculate).pack(fill=tk.X, expand=True)

        status_frame = tk.Frame(self)
        status_frame.pack(fill=tk.BOTH, expand=True, anchor=tk.S)

        self.HEADEND_status_entry = WorksheetStatusEntry(status_frame, self.config, "Headend Certificate Information Supplied by Utility")
        self.HEADEND_status_entry.setValue("Waiting...")
        self.HEADEND_status_entry.pack(fill=tk.X, padx=5)

        self.DTLS_status_entry = WorksheetStatusEntry(status_frame, self.config, "DTLS Certificate Information")
        self.DTLS_status_entry.setValue("Waiting...")
        self.DTLS_status_entry.pack(fill=tk.X, padx=5)

        self.BYPASS_status_entry = WorksheetStatusEntry(status_frame, self.config, "DTLS Bypass Allowed [DTLS_FIELD_TRIAL=False]")
        self.BYPASS_status_entry.setValue("Waiting...")
        self.BYPASS_status_entry.pack(fill=tk.X, padx=5)

        self.DCU_status_entry = WorksheetStatusEntry(status_frame, self.config, "DCU Configuration")
        self.DCU_status_entry.setValue("Waiting...")
        self.DCU_status_entry.pack(fill=tk.X, padx=5)

        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill=tk.X)

        self.status = tk.StringVar()
        tk.Label(bottom_frame, textvariable=self.status).pack(fill=tk.BOTH, expand=True)
        tk.Button(bottom_frame, text="Export", bg='yellow', command=self.__export).pack(fill=tk.X, expand=True, anchor=tk.S)

    def __calculate(self):
        """This will take the user entries and frequencies, and create an instance of a WorksheetCalculator. 
        The calculator will be able to generate all relevent data pertaining to the creation of the xml. 
        Upon calculations, the calculator will generate the status of the configuration, and present that to the screen."""

        self.calculator = WorksheetCalculator(self.config, self.entry_data, self.FREQUENCY_DATA)
        self.calculator.calculate()

        status_data: StatusData = self.calculator.STATUS_DATA

        self.HEADEND_status_entry.setValue(status_data.Headend_Certificate_Information_Supplied_by_Utility)
        self.DTLS_status_entry.setValue(status_data.DTLS_Certificate_Information)
        self.BYPASS_status_entry.setValue(status_data.DTLS_Bypass_Allowed_DTLS_FIELD_TRIAL_false)
        self.DCU_status_entry.setValue(status_data.DCU_Configuration)

        self.status.set("Successfully generated XML")

    def __export(self):
        """This will take the previously generated data from the calculator and fetch the 
        calculator's ExportData. The ExportData will then be converted to a string, and written
        to a specified file"""
        print("exporting")
        EXPORT_DATA: ExportData = self.calculator.getExportData()
        xml_str = getXMLstr(EXPORT_DATA, self.config)

        now = datetime.now()
        fn = "DCU2+XLS_"+str(now.strftime('%Y%m%d-%H%M%S'))

        name = asksaveasfile(mode='w', defaultextension='.xml', initialfile=fn, initialdir=self.config.SRC_DIR).name

        if name is not None:

            with open (name, 'w+') as f:
                f.write(xml_str)
                print("successfully exported to "+fn)

            self.status.set("Successfully exported XML")
            # self.wkst_page.grab_set()
            # self.destroy()






