# wkst_calculator.py
# 6/20/22
# Ben Schwartz
#
# Holds the WorksheetCalculator, which calculates 
# data for each step and combines them to generate
# the configuration status and the export XML

from dataclasses import dataclass
from datetime import datetime
from email import message
import json
import os
from tkinter import filedialog, messagebox

import xmlschema

from config.config import Config
from src.processing.calc_steps.DTLS_generator import DtlsData, getDtlsData
from src.processing.calc_steps.entry_generator import UserEntries, getUserEntries
from src.processing.calc_steps.freqs_generator import FrequencyData
from src.processing.calc_steps.status_generator import Status, StatusData, getStatusData
from src.processing.calc_steps.step10_calculation import Step10Data, getStep10Data
from src.processing.calc_steps.step11_calculation import Step11Data, getStep11Data
from src.processing.calc_steps.step4_calculation import Step4Data, getStep4Data
from src.processing.calc_steps.step5_calculation import Step5Data, getStep5Data
from src.processing.calc_steps.step6_calculation import Step6Data, getStep6Data
from src.processing.calc_steps.step7_calculation import Step7Data, getStep7Data
from src.processing.calc_steps.step8_calculation import Step8Data, getStep8Data
from src.processing.calc_steps.step9_calculation import Step9Data, getStep9Data
from src.utils.utils import toStr


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

        with open(self.config.LOCATION_DATA_PATH, 'r') as f:
            self.LOCATION_DATA.update(json.load(f))
        with open(self.config.TIMEZONE_DATA_PATH, 'r') as f:
            self.TIME_ZONE_DATA.update(json.load(f))

    def __processData(self) :

        if not self.config.LOG_MODE:
        
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
            STEP_10_DATA: Step10Data = getStep10Data(USER_ENTRIES, FREQUENCY_DATA)
            STEP_11_DATA: Step11Data = getStep11Data(DTLS_DATA, TIME_ZONE_DATA, USER_ENTRIES, FREQUENCY_DATA, STEP_10_DATA)

        else:
            if not os.path.exists(self.config.RUNTIME_LOG_PATH):
                self.config.RUNTIME_LOG_PATH = os.path.join(os.path.abspath('.'), "runtime_calcs.txt")
                messagebox.showerror("Log Error", "Log .txt file path not valid. Creating new log file at: "+self.config.RUNTIME_LOG_PATH)
            
            with open(self.config.RUNTIME_LOG_PATH, 'w+') as f:
                f.write("CALCULATION LOG FOR RUN: "+datetime.now().strftime('%Y/%m/%d-%H:%M:%S'))
                USER_ENTRIES: UserEntries = getUserEntries(self.entry_data_dict)
                f.write("\n\n\n\t\t\t***USER ENTRIES***\n\n"+json.dumps(USER_ENTRIES.getOrderedDict(), indent=2)); f.flush()
                FREQUENCY_DATA: FrequencyData = self.FREQUENCY_DATA
                f.write("\n\n\n\t\t\t***FREQUENCY DATA***\n\n"+json.dumps(FREQUENCY_DATA.getOrderedDict(), indent=2)); f.flush()
                DTLS_DATA: DtlsData = getDtlsData(USER_ENTRIES, self.LOCATION_DATA)
                f.write("\n\n\n\t\t\t***DTLS DATA***\n\n"+json.dumps(DTLS_DATA.getOrderedDict(), indent=2)); f.flush()
                TIME_ZONE_DATA: dict = self.TIME_ZONE_DATA[USER_ENTRIES.Time_Zone_r14]
                f.write("\n\n\n\t\t\t***TIME ZONE DATA***\n\n"+json.dumps(TIME_ZONE_DATA, indent=2)); f.flush()
                STEP_4_DATA: Step4Data = getStep4Data(USER_ENTRIES, FREQUENCY_DATA)
                f.write("\n\n\n\t\t\t***STEP 4***\n\n"+json.dumps(STEP_4_DATA.getOrderedDict(), indent=2)); f.flush()
                STEP_5_DATA: Step5Data = getStep5Data(STEP_4_DATA)
                f.write("\n\n\n\t\t\t***STEP 5***\n\n"+json.dumps(STEP_5_DATA.getOrderedDict(), indent=2)); f.flush()
                STEP_6_DATA: Step6Data = getStep6Data(FREQUENCY_DATA, STEP_4_DATA, STEP_5_DATA)
                f.write("\n\n\n\t\t\t***STEP 6***\n\n"+json.dumps(STEP_6_DATA.getOrderedDict(), indent=2)); f.flush()
                STEP_7_DATA: Step7Data = getStep7Data(FREQUENCY_DATA, STEP_5_DATA, STEP_6_DATA)
                f.write("\n\n\n\t\t\t***STEP 7***\n\n"+json.dumps(STEP_7_DATA.getOrderedDict(), indent=2)); f.flush()
                STEP_8_DATA: Step8Data = getStep8Data(FREQUENCY_DATA, STEP_4_DATA, STEP_5_DATA, STEP_6_DATA, STEP_7_DATA)
                f.write("\n\n\n\t\t\t***STEP 8***\n\n"+json.dumps(STEP_8_DATA.getOrderedDict(), indent=2)); f.flush()
                STEP_9_DATA: Step9Data = getStep9Data(FREQUENCY_DATA, STEP_5_DATA, STEP_6_DATA)
                f.write("\n\n\n\t\t\t***STEP 9***\n\n"+json.dumps(STEP_9_DATA.getOrderedDict(), indent=2)); f.flush()
                STEP_10_DATA: Step10Data = getStep10Data(USER_ENTRIES, FREQUENCY_DATA)
                f.write("\n\n\n\t\t\t***STEP 10***\n\n"+json.dumps(STEP_10_DATA.getOrderedDict(), indent=2)); f.flush()
                STEP_11_DATA: Step11Data = getStep11Data(DTLS_DATA, TIME_ZONE_DATA, USER_ENTRIES, FREQUENCY_DATA, STEP_10_DATA)
                f.write("\n\n\n\t\t\t***STEP 11***\n\n"+json.dumps(STEP_11_DATA.getOrderedDict(), indent=2)); f.flush()

        self.__EXPORT_DATA: ExportData = ExportData(USER_ENTRIES, STEP_7_DATA, STEP_8_DATA, STEP_9_DATA, STEP_11_DATA)
        self.__STATUS_DATA: StatusData = getStatusData(USER_ENTRIES, DTLS_DATA, STEP_4_DATA)

    def calculate(self):
        """This will call upon processData() to do all the calculations for each step. If
        an error is found, a message is shown and the user will go back to the main screen."""
        try:
            self.__processData()
        except Exception as e:
            error_msg = "Error during calculation\n\n"+str(e)
            if self.config.LOG_MODE:
                error_msg += "\n\nPlease check the log file located in "+self.config.RUNTIME_LOG_PATH+" to inspect calculation steps."
            else:
                error_msg += "\n\nPlease inspect calculations, or turn on log_mode in options.json"
            error_msg += "\n\nContact Engineering."
            messagebox.showerror("Calculation Error", error_msg)
            return

        # Showing status messages if there is a fail or warning
        if self.__STATUS_DATA.Headend_Certificate_Information_Supplied_by_Utility_STATUS == Status.FAIL:
            self.__showFailMessage(self.__STATUS_DATA.Headend_Certificate_Information_Supplied_by_Utility)
            return
        elif self.__STATUS_DATA.Headend_Certificate_Information_Supplied_by_Utility_STATUS == Status.WARNING:
            self.__showWarningMessage(self.__STATUS_DATA.Headend_Certificate_Information_Supplied_by_Utility)
            return
        
        if self.__STATUS_DATA.DTLS_Certificate_Information_STATUS == Status.FAIL:
            self.__showFailMessage(self.__STATUS_DATA.DTLS_Certificate_Information)
            return
        elif self.__STATUS_DATA.DTLS_Certificate_Information_STATUS == Status.WARNING:
            self.__showWarningMessage(self.__STATUS_DATA.DTLS_Certificate_Information)
            return

        if self.__STATUS_DATA.DTLS_Bypass_Allowed_STATUS == Status.FAIL:
            self.__showFailMessage(self.__STATUS_DATA.DTLS_Bypass_Allowed)
            return
        elif self.__STATUS_DATA.DTLS_Bypass_Allowed_STATUS == Status.WARNING:
            self.__showWarningMessage(self.__STATUS_DATA.DTLS_Bypass_Allowed)
            return

        if self.__STATUS_DATA.DCU_Configuration_STATUS == Status.FAIL:
            self.__showFailMessage(self.__STATUS_DATA.DCU_Configuration)
            return
        elif self.__STATUS_DATA.DCU_Configuration_STATUS == Status.WARNING:
            self.__showWarningMessage(self.__STATUS_DATA.DCU_Configuration)
            return

        # At this point, no warnings or errors have been detected,
        # and the user may now export
        self.__showExportMessage()
        

    
    def __showFailMessage(self, message):
        fail_msg = "A fatal error occurred during configuration:\n\n*****\n"+message+"\n*****\n\nPlease fix the problem, and try again."
        messagebox.showerror("Config Status error", fail_msg)
    def __showWarningMessage(self, message):
        warning_msg = "During configuration, a warning was detected:\n\n*****\n"+message+"\n*****\n\nDo you wish to proceed?"
        will_proceed = messagebox.askyesno("Warning", warning_msg, icon='warning')
        if will_proceed:
            self.__showExportMessage()
        else:
            pass
    def __showExportMessage(self):
        message = "Successfully generated DCU2+XLS .xml\n\n"
        message += "Do you wish to create an archive folder containing the .xml, user entries, frequency data, and worksheet status?"
        message += "\n\n(Select 'Yes' to generate archive folder)"
        message += "\n(Select 'No' to just export the .xml)"
        message += "\n(Select 'Cancel' to go back to worksheet)"

        will_archive = messagebox.askyesnocancel("Success", message, icon='info')

        
        
        if will_archive:
            self.__export(user_wants_archive=True)
        elif will_archive is None:
            pass
        else:
            self.__export(user_wants_archive=False)

    def getExportData(self):
        return self.__EXPORT_DATA

    def getStatusData(self):
        return self.__STATUS_DATA

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
            data = self.__STATUS_DATA.getData()
            data["@generated"] = time_str
            json.dump(data, f, indent=2)

        xml_fn = os.path.join(dir, "DCU2+XLS_"+time_fn_str+".xml")
        with open(xml_fn, 'w+') as f:
            f.write(xml_str)

        
            
    def __export(self, user_wants_archive):
        """This will take the previously generated data from the calculator and fetch the 
        calculator's ExportData. The ExportData will then be converted to a string, and written
        to a specified file"""

        try:
            xml_str = self.__getXMLstr()
        except Exception as e:
            messagebox.showerror("Export error", str(e))
            return

        now = datetime.now()
        datetime_fn_str = now.strftime('%Y%m%d-%H%M%S')
        datetime_str = now.strftime('%Y/%m/%d-%H:%M:%S')

        if user_wants_archive:
            
            archive_parent_dir = filedialog.askdirectory(title='Select Archive Destination', initialdir=self.config.SRC_DIR)

            if archive_parent_dir != '':
                
                archive_dir = os.path.join(archive_parent_dir, "DCU2+XLS_Archive_"+datetime_fn_str)
                os.mkdir(archive_dir)

                self.__archive(archive_dir, datetime_str, datetime_fn_str, xml_str)
                messagebox.showinfo("Successfully archived and exported", "Successfully written archive and export files to:\n\n"+archive_dir)
                return
        else:
            fn = "DCU2+XLS_"+datetime_fn_str
            name = filedialog.asksaveasfile(mode='w', defaultextension='.xml', initialfile=fn, initialdir=self.config.SRC_DIR)
            if name is not None:
                name = name.name # So tk is happy
                with open (name, 'w+') as f:
                    f.write(xml_str)
                messagebox.showinfo("Successfully exported", "Successfully written export file to:\n\n"+str(os.path.abspath(fn)))
                return
            

    def __getXMLstr(self) -> str:
        """This will take the data generated from all of the calculations, and create 
        an XML for export. It will first take an example output to get the correct keys, 
        populate with correct values, and convert back into XML using the xmlschema module."""
        XML_DICT = {}

        data: ExportData = self.__EXPORT_DATA

        try:
            schema = xmlschema.XMLSchema(self.config.EXPORT_SCHEMA_PATH)
            template_data = schema.to_dict(self.config.EXPORT_TEMPLATE_PATH)
            XML_DICT.update(template_data)
        except Exception as e:
            raise Exception("error 550: error parsing export template\n\n"+str(e)+"\n\nPlease check export schema and template.")

        try:
            XML_DICT["metadata"]["CustomerID"] = toStr(data.USER_ENTRIES.Aclara_Customer_ID_r28)
            XML_DICT["metadata"]["CustomerName"] = toStr(data.USER_ENTRIES.Customer_Name_r2)
            XML_DICT["metadata"]["Drawing"] = toStr(data.USER_ENTRIES.DCU_Drawing_Number_r26)
            XML_DICT["metadata"]["Product"] = toStr(data.USER_ENTRIES.DCU_Product_Number_r27)

            XML_DICT["common"]["appSecurityAuthMode"] = toStr(data.DATA_11.appSecurityAuthMode_r159)
            XML_DICT["common"]["dtlsNetworkHESubject"] = toStr(data.DATA_11.dtlsNetworkHESubject_r160)
            XML_DICT["common"]["dtlsNetworkMSSubject"] = toStr(data.DATA_11.dtlsNetworkMSSubject_r161)
            XML_DICT["common"]["dtlsNetworkRootCA"] = toStr(data.DATA_11.dtlsNetworkRootCA_r162)
            XML_DICT["common"]["flashSecurityEnabled"] = toStr(data.DATA_11.Flash_Security_Enabled_r157)
            XML_DICT["common"]["ipHEContext"] = toStr(data.DATA_11.ipHEContext_r163)
            XML_DICT["common"]["macChannelSets"] = toStr(data.DATA_11.macChannelSets_r156) 
            XML_DICT["common"]["macChannelSetsSTAR"] = toStr(data.DATA_11.macChannelSetsSTAR_r155)
            XML_DICT["common"]["macNetworkId"] = toStr(data.DATA_11.macNetworkId_r164)
            XML_DICT["common"]["phyAvailableFrequencies"] = toStr(data.DATA_11.phyAvailableFrequencies_r152)
            XML_DICT["common"]["realtimeThreshold"] = toStr(data.DATA_11.realtimeThreshold_r166)
            XML_DICT["common"]["shipMode"] = toStr(data.DATA_11.shipMode_r168)

            SLOT_2_DICT = {
                "@slot": "2",
                "comDeviceGatewayConfig": toStr(data.DATA_8.comDeviceGatewayConfig_r130),
                "phyRxFrequencies": toStr(data.DATA_8.phyRxFrequencies_r131), 
                "phyTxFrequencies": toStr(data.DATA_8.phyTxFrequencies_r132),
                "phyRxDetection": toStr(data.DATA_8.phyRxDetection_r133),
                "phyRxFraming": toStr(data.DATA_8.phyRxFraming_r134),
                "phyRxMode": toStr(data.DATA_8.phyRxMode_r135)
            }

            SLOT_3_DICT = {
                "@slot": "3",
                "comDeviceGatewayConfig": toStr(data.DATA_7.comDeviceGatewayConfig_r122),
                "phyRxFrequencies": toStr(data.DATA_7.phyRxFrequencies_r123),
                "phyTxFrequencies": toStr(data.DATA_7.phyTxFrequencies_r124),
                "phyRxDetection": toStr(data.DATA_7.phyRxDetection_r125),
                "phyRxFraming": toStr(data.DATA_7.phyRxFraming_r126),
                "phyRxMode": toStr(data.DATA_7.phyRxMode_r127)
            }

            XML_DICT["SRFNI-XCVR"] = [SLOT_2_DICT, SLOT_3_DICT]

            XML_DICT["EXPORT-FORMAT"] = toStr(data.USER_ENTRIES.Tool_Version_r29)

            XML_DICT["SRFNI-METER"]["comDeviceGatewayConfig"] = toStr("EP")
            XML_DICT["SRFNI-METER"]["EPRxFrequencies"] = toStr(data.DATA_9.EP_Rx_SRFN_Except_DA_r143)
            XML_DICT["SRFNI-METER"]["EPTxFrequencies"] = toStr(data.DATA_9.EP_Tx_SRFN_Except_DA_r138)

            XML_DICT["SRFNI-DA"]["comDeviceGatewayConfig"] = toStr("EP")
            XML_DICT["SRFNI-DA"]["EPRxFrequencies"] = toStr(data.DATA_9.EP_Rx_SRFN_DA_Except_DA_r144)
            XML_DICT["SRFNI-DA"]["EPTxFrequencies"] = toStr(data.DATA_9.EP_Tx_SRFN_DA_Except_DA_r139)

            XML_DICT["STARI-METER"]["comDeviceGatewayConfig"] = toStr("EP")
            XML_DICT["STARI-METER"]["EPRxFrequenciesSTAR7200"] = toStr(data.DATA_9.EP_Rx_STAR7200_r145)
            XML_DICT["STARI-METER"]["EPTxFrequenciesSTAR7200"] = toStr(data.DATA_9.EP_Tx_STAR7200_r140)
            XML_DICT["STARI-METER"]["EPRxFrequenciesSTAR2400"] = toStr(data.DATA_9.EP_Rx_STAR2400_r146)
            XML_DICT["STARI-METER"]["EPTxFrequenciesSTAR2400"] = toStr(data.DATA_9.EP_Tx_STAR2400_r141)
            XML_DICT["STARI-METER"]["EPRxFrequenciesSTAR2400Legacy"] = toStr(data.DATA_9.EP_Rx_STAR2400Legacy_r147)
            XML_DICT["STARI-METER"]["EPTxFrequenciesSTAR2400Legacy"] = toStr(data.DATA_9.EP_Tx_STAR2400Legacy_r142)
        except Exception as e:
            raise Exception("error 553: error writing to export xml\n\n"+str(e)+"\n\nPlease check that keys match in calculator.py and .xml")

        try:
            xml_str = xmlschema.etree_tostring(schema.to_etree(XML_DICT))
            return xml_str
        except Exception as e:
            raise Exception("error 554: error converting dict to xml\n\n"+str(e)+"\n\nPlease check that keys match in calculator.py and .xml")

        

        

            

        