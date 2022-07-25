# status_generator.py
# 6/20/22
# Ben Schwartz
#
# Defines the data structure associated with the calculations for
# the StatusData, which is used to display on the screen the configuration
# status and determine if the user is allowed to export

from dataclasses import dataclass
from enum import Enum
from src.processing.calc_steps.DTLS_generator import DtlsData

from src.processing.calc_steps.entry_generator import UserEntries
from src.processing.calc_steps.step4_calculation import Step4Data
from src.utils.utils import toStr


class Status(Enum):
    PASS = ('green', 'white')
    WARNING = ('yellow', 'black')
    FAIL = ('red', 'white')

class StatusEntryName(Enum):
    HE_CERT_UTILITY = "Headend Certificate Information Supplied by Utility"
    DTLS_CERT = "DTLS Certificate Information"
    DTLS_BYPASS = "DTLS Bypass Allowed [DTLS_FIELD_TRIAL=False]"
    DCU_CONFIG = "DCU Configuration"

@dataclass
class StatusData:
    Headend_Certificate_Information_Supplied_by_Utility: str = None
    DTLS_Certificate_Information: str = None
    DTLS_Bypass_Allowed: str = None
    DCU_Configuration: str = None
    
    Headend_Certificate_Information_Supplied_by_Utility_STATUS: Status = None
    DTLS_Certificate_Information_STATUS: Status = None
    DTLS_Bypass_Allowed_STATUS: Status = None
    DCU_Configuration_STATUS: Status = None

    def getData(self) -> dict:
        return {
            str(StatusEntryName.HE_CERT_UTILITY.value): self.Headend_Certificate_Information_Supplied_by_Utility,
            str(StatusEntryName.DTLS_CERT.value): self.DTLS_Certificate_Information,
            str(StatusEntryName.DTLS_BYPASS): self.DTLS_Bypass_Allowed,
            str(StatusEntryName.DCU_CONFIG.value): self.DCU_Configuration
        }
    


def getStatusData(USER_ENTRIES: UserEntries, DTLS_DATA: DtlsData, DATA_4: Step4Data) -> StatusData:
        
        STATUS_DATA = StatusData()
        # Row 32
        result = None
        status = None
        
        if USER_ENTRIES.Utility_Head_End_Certificate_Source_r12 == "Manufacturer":
            result = "Trusting Aclara PKI"
            status = Status.PASS
        else:
            result = """Contact Aclara.\n\nManufacturer must provide RootCA support: 
            
            (DER X.509v3 security certificate chain (SHA-256 ECC P-256). 
             Security certificate chain must include a common root certificate authority and can optionally include one 
             subordinate certificate authority. Each certificate must be 450 bytes or less in size)"""
            # Contact Aclara
            status = Status.FAIL

        STATUS_DATA.Headend_Certificate_Information_Supplied_by_Utility = result
        STATUS_DATA.Headend_Certificate_Information_Supplied_by_Utility_STATUS = status
        # Row 33
        result = None
        status = None

        result = DTLS_DATA.status

        if result == "Data Looks Ok":
            status = Status.PASS
        elif result == 'Head End Certificate Error':
            status = Status.FAIL
        elif result == 'Meter Shop Certificate Error':
            status = Status.FAIL
        elif result == 'Text String is too large':
            status = Status.FAIL
        else:
            print("error 559: unexcepcted DTLS response")
            status = Status.FAIL

        STATUS_DATA.DTLS_Certificate_Information = result
        STATUS_DATA.DTLS_Certificate_Information_STATUS = status
        # Row 34
        result = None
        status = None

        if USER_ENTRIES.DTLS_Bypass_Mode_Allowed_r13:
            result = "Firmware Build Switch Allowed"
            status = Status.PASS
        else:
            result = "Firmware Build Switch Not Allowed"
            # Utility Communications will not be protected in field
            status = Status.WARNING

        STATUS_DATA.DTLS_Bypass_Allowed = result
        STATUS_DATA.DTLS_Bypass_Allowed_STATUS = status
        # Row 35
        result = None
        status = None

        if (DATA_4.SRFN_Receiver_Channels_r68 + DATA_4.STAR_Receiver_Channels_Minimum_r67 + DATA_4.DCU_Transmitter_Count_r66) > DATA_4.DCU_Receive_Channels_Available_r65:
            result = "Error: More Radio Assets Needed"
            # show message displaying the numbers
            # "Some field devices will not be able to communicate with any DCUs. More Radio Assets Needed "
            status = Status.FAIL
        else:
            result = toStr(DATA_4.DCU_Configuration_Description_r81)
            status = Status.PASS

        STATUS_DATA.DCU_Configuration = result
        STATUS_DATA.DCU_Configuration_STATUS = status

        return STATUS_DATA


        
