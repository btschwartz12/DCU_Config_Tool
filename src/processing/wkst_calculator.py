

from abc import abstractclassmethod
from dataclasses import dataclass, fields
from datetime import datetime
import json
from pprint import pformat, pprint
from re import S
import re
from tkinter import messagebox
from typing import OrderedDict
from unittest.util import strclass

import xmlschema
from src.processing.calc_steps.DTLS_generator import DtlsData, getDtlsData
from src.processing.calc_steps.entry_generator import UserEntries, getUserEntries

from src.processing.calc_steps.freqs_generator import FrequencyData, getFrequencyData
from src.processing.calc_steps.step10_calculation import Step10Data, getStep10Data
from src.processing.calc_steps.step11_calculation import Step11Data, getStep11Data
from src.processing.calc_steps.step4_calculation import Step4Data, getStep4Data
from src.processing.calc_steps.step5_calculation import Step5Data, getStep5Data
from src.processing.calc_steps.step6_calculation import Step6Data, getStep6Data
from src.processing.calc_steps.step7_calculation import Step7Data, getStep7Data
from src.processing.calc_steps.step8_calculation import Step8Data, getStep8Data
from src.processing.calc_steps.step9_calculation import Step9Data, getStep9Data
from src.processing.export_xml import ExportData
from src.utils.utils import toStr



LOCATION_DATA_FN = "data/location_data.json"
TIME_ZONE_DATA_FN = "data/time_zone_data.json"


@dataclass
class StatusData:
    Headend_Certificate_Information_Supplied_by_Utility: str = None
    DTLS_Certificate_Information: str = None
    DTLS_Bypass_Allowed_DTLS_FIELD_TRIAL_false: str = None
    DCU_Configuration: str = None

    def getValList(self):
        vals = []
        for field in fields(self):
            vals.append(getattr(self, field.name))
        return vals

# HERE7 make an interface that has all of the steps and functions, then implement 
# main calculator in main file then all steps can be seperate files

class WorksheetCalculator:
    def __init__(self, controller, entry_data):
        self.controller = controller

        self.entry_data_dict: dict = entry_data

        self.LOCATION_DATA = {}
        self.TIME_ZONE_DATA = {}
        
        with open(LOCATION_DATA_FN, 'r') as f:
            self.LOCATION_DATA.update(json.load(f))
        with open(TIME_ZONE_DATA_FN, 'r') as f:
            self.TIME_ZONE_DATA.update(json.load(f))

    def calculate(self, debug=False, freq_fn=None) :

        try:
            FREQUENCY_DATA: FrequencyData = getFrequencyData(debug, freq_fn)
        except Exception as e:
            messagebox.showerror("error 492: cannot obtain frequency data", str(e))
            return

        USER_ENTRIES: UserEntries = getUserEntries(self.entry_data_dict)
        DTLS_DATA: DtlsData = getDtlsData(USER_ENTRIES, self.LOCATION_DATA)
        TIME_ZONE_DATA: dict = self.TIME_ZONE_DATA[USER_ENTRIES.Time_Zone_r14]
        STEP_4_DATA: Step4Data = getStep4Data(USER_ENTRIES, FREQUENCY_DATA)
        STEP_5_DATA: Step5Data = getStep5Data(STEP_4_DATA)
        STEP_6_DATA: Step6Data = getStep6Data(FREQUENCY_DATA, STEP_4_DATA, STEP_5_DATA)
        STEP_7_DATA: Step7Data = getStep7Data(FREQUENCY_DATA, STEP_5_DATA, STEP_6_DATA)
        STEP_8_DATA: Step8Data = getStep8Data(FREQUENCY_DATA, STEP_4_DATA, STEP_5_DATA, STEP_6_DATA, STEP_7_DATA)
        STEP_9_DATA: Step9Data = getStep9Data(FREQUENCY_DATA, STEP_5_DATA, STEP_6_DATA)
        STEP_10_DATA: Step10Data = getStep10Data(FREQUENCY_DATA)
        STEP_11_DATA: Step11Data = getStep11Data(DTLS_DATA, TIME_ZONE_DATA, USER_ENTRIES, FREQUENCY_DATA, STEP_10_DATA)

        with open('WKST_SAMPLES/runtime_calcs.txt', 'w+') as f:
            f.write("\n\n\n               ***USER ENTRIES***\n\n"+json.dumps(USER_ENTRIES.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n               ***FREQUENCY DATA***\n\n"+json.dumps(FREQUENCY_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n               ***STEP 4***\n\n"+json.dumps(STEP_4_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n               ***STEP 5***\n\n"+json.dumps(STEP_5_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n               ***STEP 6***\n\n"+json.dumps(STEP_6_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n               ***STEP 7***\n\n"+json.dumps(STEP_7_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n               ***STEP 8***\n\n"+json.dumps(STEP_8_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n               ***STEP 9***\n\n"+json.dumps(STEP_9_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n               ***STEP 10***\n\n"+json.dumps(STEP_10_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n               ***STEP 11***\n\n"+json.dumps(STEP_11_DATA.getOrderedDict(), indent=2)); f.flush()
        
        self.EXPORT_DATA: ExportData = ExportData(USER_ENTRIES, STEP_7_DATA, STEP_8_DATA, STEP_9_DATA, STEP_11_DATA)
        self.STATUS_DATA: StatusData = self.__getStatusData(USER_ENTRIES, DTLS_DATA, STEP_4_DATA)

    def getExportData(self):
        return self.EXPORT_DATA
        

    def __getStatusData(self, USER_ENTRIES: UserEntries, DTLS_DATA: DtlsData, DATA_4: Step4Data) -> StatusData:
        
        STATUS_DATA = StatusData()

        # Row 32
        result = None

        if USER_ENTRIES.Utility_Head_End_Certificate_Source_r12 == "Manufacturer":
            result = "None"
        else:
            result = "DER X.509v3 security certificate chain (SHA-256 ECC P-256).  Security certificate chain must include a common root certificate authority and can optionally include one subordinate certificate authority. Each certificate must be 450 bytes or less in size"

        STATUS_DATA.Headend_Certificate_Information_Supplied_by_Utility = result
        # Row 33
        result = None

        result = DTLS_DATA.status

        STATUS_DATA.DTLS_Certificate_Information = result
        # Row 34
        result = None

        if USER_ENTRIES.DTLS_Bypass_Mode_Allowed_r13:
            result = "Firmware Build Switch Allowed"
        else:
            result = "Firmware Build Switch Not Allowed"

        STATUS_DATA.DTLS_Bypass_Allowed_DTLS_FIELD_TRIAL_false = result
        # Row 35
        result = None

        if (DATA_4.SRFN_Receiver_Channels_r68 + DATA_4.STAR_Receiver_Channels_Minimum_r67 + DATA_4.DCU_Transmitter_Count_r66) > DATA_4.DCU_Receive_Channels_Available_r65:
            result = "Error: More Radio Assets Needed"
        else:
            result = toStr(DATA_4.DCU_Configuration_Description_r81)

        STATUS_DATA.DCU_Configuration = result

        return STATUS_DATA


        
