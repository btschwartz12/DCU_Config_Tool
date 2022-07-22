# wkst_calculator.py
# 6/20/22
# Ben Schwartz
#
# Holds the WorksheetCalculator, which calculates 
# data for each step and combines them to generate
# the configuration status and the export XML

from dataclasses import dataclass
from datetime import datetime
import json

from config.config import Config
from src.gui.wkst_status_entry import Status
from src.processing.calc_steps.DTLS_generator import DtlsData, getDtlsData
from src.processing.calc_steps.entry_generator import UserEntries, getUserEntries
from src.processing.calc_steps.freqs_generator import FrequencyData
from src.processing.calc_steps.status_generator import StatusData, getStatusData
from src.processing.calc_steps.step10_calculation import Step10Data, getStep10Data
from src.processing.calc_steps.step11_calculation import Step11Data, getStep11Data
from src.processing.calc_steps.step4_calculation import Step4Data, getStep4Data
from src.processing.calc_steps.step5_calculation import Step5Data, getStep5Data
from src.processing.calc_steps.step6_calculation import Step6Data, getStep6Data
from src.processing.calc_steps.step7_calculation import Step7Data, getStep7Data
from src.processing.calc_steps.step8_calculation import Step8Data, getStep8Data
from src.processing.calc_steps.step9_calculation import Step9Data, getStep9Data


@dataclass 
class ExportData:
    USER_ENTRIES: UserEntries
    DATA_7: Step7Data
    DATA_8: Step8Data
    DATA_9: Step9Data
    DATA_11: Step11Data

class WorksheetCalculator:
    """This is used by the CalculationWindow, and will take in frequency data and
    user entries to generate the ExportData, making use of all step calculations."""
    def __init__(self, config: Config, entry_data, frequency_data: FrequencyData):
        self.config = config

        self.entry_data_dict: dict = entry_data
        self.FREQUENCY_DATA = frequency_data

        self.LOCATION_DATA = {}
        self.TIME_ZONE_DATA = {}

        with open(self.config.LOCATION_DATA_RPATH, 'r') as f:
            self.LOCATION_DATA.update(json.load(f))
        with open(self.config.TIMEZONE_DATA_RPATH, 'r') as f:
            self.TIME_ZONE_DATA.update(json.load(f))

    def calculate(self) :

        USER_ENTRIES: UserEntries = getUserEntries(self.entry_data_dict)
        FREQUENCY_DATA: FrequencyData = self.FREQUENCY_DATA

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

        with open(self.config.RUNTIME_LOG_RPATH, 'w+') as f:
            f.write("CALCULATION LOG FOR RUN: "+datetime.now().strftime('%Y/%m/%d-%H:%M:%S'))
            f.write("\n\n\n\t\t\t***USER ENTRIES***\n\n"+json.dumps(USER_ENTRIES.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n\t\t\t***FREQUENCY DATA***\n\n"+json.dumps(FREQUENCY_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n\t\t\t***STEP 4***\n\n"+json.dumps(STEP_4_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n\t\t\t***STEP 5***\n\n"+json.dumps(STEP_5_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n\t\t\t***STEP 6***\n\n"+json.dumps(STEP_6_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n\t\t\t***STEP 7***\n\n"+json.dumps(STEP_7_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n\t\t\t***STEP 8***\n\n"+json.dumps(STEP_8_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n\t\t\t***STEP 9***\n\n"+json.dumps(STEP_9_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n\t\t\t***STEP 10***\n\n"+json.dumps(STEP_10_DATA.getOrderedDict(), indent=2)); f.flush()
            f.write("\n\n\n\t\t\t***STEP 11***\n\n"+json.dumps(STEP_11_DATA.getOrderedDict(), indent=2)); f.flush()
        
        self.__EXPORT_DATA: ExportData = ExportData(USER_ENTRIES, STEP_7_DATA, STEP_8_DATA, STEP_9_DATA, STEP_11_DATA)
        self.__STATUS_DATA: StatusData = getStatusData(USER_ENTRIES, DTLS_DATA, STEP_4_DATA)

    def getExportData(self):
        return self.__EXPORT_DATA

    def getStatusData(self):
        return self.__STATUS_DATA



        

    