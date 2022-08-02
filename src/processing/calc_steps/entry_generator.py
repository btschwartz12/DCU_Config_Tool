# entry_generator.py
# 6/20/22
# Ben Schwartz
#
# Defines the user entries data structure and offers a
# constructor with a dict parameter

from dataclasses import dataclass

from src.utils.utils import StepData

@dataclass
class UserEntries(StepData):
    Customer_Name_r2: str
    Contact_Name_r3: str
    Country_r4: str
    State_r5: str
    City_r6: str
    Street_Address_r7: str
    Zip_Code_r8: int
    Telephone_Number_r9: str
    Email_r10: str
    Account_Manager_r11: str
    Utility_Head_End_Certificate_Source_r12: str
    DTLS_Bypass_Mode_Allowed_r13: bool
    Time_Zone_r14: str
    Daily_Shift_Time_r15: str
    Automatic_Demand_Reset_r16: str
    Outage_Last_Gasp_Delay_r17: str
    Restoration_Delay_r18: str
    System_Includes_STAR_2400_Legacy_devices_r19: bool
    System_Includes_STAR_2400_devices_r20: bool
    System_Includes_STAR_7200_devices_r21: bool
    System_Includes_SRFN_Devices_r22: bool
    System_Includes_SRFN_Dedicated_DA_Recv_Channel_r23: bool
    DCU_T_Boards_r24: int
    DCU_Single_Transmit_T_Board_Firmware_r25: str
    Aclara_Customer_ID_r28: int
    Tool_Version_r29: str
    Customer_Configuration_Id_r30: str
    DCU_Drawing_Number_r26: int = None
    DCU_Product_Number_r27: int = None


def getUserEntries(user_entry_dict: dict) -> UserEntries:
        """This will take the user entries dict and convert it to a
        UserEntries dataclass object, so that they can be accessed later""" 
        data = user_entry_dict

        entry_data = UserEntries(data["Customer Name"], data["Contact Name"], data["Country"], 
                                data["State"], data["City"], data["Street Address"], data["Zip Code"],
                                data["Telephone Number"], data["Email"], data["Account Manager"], 
                                data["Utility Head End Certificate Source"], data["DTLS Bypass Mode Allowed"],
                                data["Time Zone"], data["Daily Shift Time (hours after midnight local)"],
                                data["Automatic Demand Reset [1 day]"], data["Outage Last Gasp Delay [30s, Default: 30s]"],
                                data["Restoration Delay [15s, Default: 15s]"], data["System Includes STAR 2400 Legacy devices"],
                                data["System Includes STAR 2400 devices"], data["System Includes STAR7200 devices"],
                                data["System Includes SRFN Devices"], data["System Includes SRFN Dedicated DA Recv Channel"],
                                data["DCU T-Boards [DCU2+]"], data["DCU Single Transmit T-Board Firmware"],
                                data["Aclara Customer ID"], data["Tool Version"], data["Customer Configuration Id"])
        
        if data["DCU Drawing Number (from Fusion)"] != 0:
            entry_data.DCU_Drawing_Number = data["DCU Drawing Number (from Fusion)"]
        if data["DCU Product Number (the Y number)"] != 0:
            entry_data.DCU_Product_Number= data["DCU Product Number (the Y number)"]

        return entry_data