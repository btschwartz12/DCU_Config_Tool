from dataclasses import dataclass, fields
from src.processing.calc_steps.DTLS_generator import DtlsData
from src.processing.calc_steps.entry_generator import UserEntries
from src.processing.calc_steps.freqs_generator import FrequencyData
from src.processing.calc_steps.step10_calculation import Step10Data

from src.utils.utils import StepData



@dataclass
class Step11Data(StepData):
    phyAvailableFrequencies_r152: list[str] = None
    phyRxFrequencies_r153: int = None
    phyTxFrequencies_r154: list[int] = None
    macChannelSetsSTAR_r155: list[int] = None
    macChannelSets_r156: list[int] = None
    Flash_Security_Enabled_r157: int = None
    debugPortEnabled_r158: int = None
    appSecurityAuthMode_r159: int = None
    dtlsNetworkHESubject_r160: str = None
    dtlsNetworkMSSubject_r161: str = None
    dtlsNetworkRootCA_r162: str = None
    ipHEContext_r163: int = None
    macNetworkId_r164: int = None
    opportunisticThreshold_r165: int = None
    realtimeThreshold_r166: int = None
    realtimeThreshold_DCU_r167: int = None
    shipMode_r168: int = None
    timeAcceptanceDelay_r169: int = None
    dstStartRule_r170: int = None
    dstEndRule_r171: int = None
    timeZoneOffset_r172: int = None
    dstEnabled_r173: int = None
    dstOffset_r174: int = None
    timeZoneDSTHash_r175: int = None
    dailySelfReadTime_r176: int = None
    scheduledDemandResetDay_r177: int = None
    outageDeclarationDelay_r178: int = None
    restorationDeclarationDelay_r179: int = None


def getStep11Data(DTLS_DATA: DtlsData, TIME_ZONE_DATA: dict, USER_ENTRIES: UserEntries, FREQ_DATA: FrequencyData, DATA_10: Step10Data) -> Step11Data:
    """This will look at all previously generated data
    and fill all the fields that will be used for the xml
    
    Data Used: 
    Corresponding excel rows: 
    Step(s) / Block(s): 
    """   

    STEP_11_DATA = Step11Data()  

    # Row 152
    result = []
    # 17 total commas

    result = list(map(str, DATA_10.All_STAR_and_SRFN_Frequencies_r149)) # Convert from list[int] to list[str]

    while len(result) != 18:
        result.append("")
    
    STEP_11_DATA.phyAvailableFrequencies_r152 = result
    # Row 153
    result = None

    if FREQ_DATA.SRFN_Outbound_Downlink_Frequency_r47 is not None:
        result = int(FREQ_DATA.SRFN_Outbound_Downlink_Frequency_r47 * 1000000)
    else:
        result = ""
    
    STEP_11_DATA.phyRxFrequencies_r153 = result
    # Row 154
    result = []

    result = DATA_10.SRFN_Endpoint_Inbound_Transmit_Frequencies_r150
    
    STEP_11_DATA.phyTxFrequencies_r154 = result
    # Row 155
    result = []
    
    if USER_ENTRIES.System_Includes_STAR_7200_devices_r21 is False:
        result = [466600000, 468000000, 456000000, 458000000]
    elif int(FREQ_DATA.STAR_F2_Downlink_Frequency_r46) not in range(450, 470+1) or int(FREQ_DATA.STAR_F1_Uplink_Frequency_r48) not in range(450, 470+1):
        result = ["INVALID FREQUENCY"]
    else:
        result.append(int(FREQ_DATA.STAR_F2_Downlink_Frequency_r46 * 1000000))
        result.append(int(FREQ_DATA.STAR_F2_Downlink_Frequency_r46 * 1000000))
        result.append(int(FREQ_DATA.STAR_F1_Uplink_Frequency_r48 * 1000000))
        result.append(int(FREQ_DATA.STAR_F1_Uplink_Frequency_r48 * 1000000))
        
    STEP_11_DATA.macChannelSetsSTAR_r155 = result
    # Row 156
    result = []
    

    if int(STEP_11_DATA.phyRxFrequencies_r153) > 450000000 or \
            int(STEP_11_DATA.phyRxFrequencies_r153) < 470000000:
        result.append(STEP_11_DATA.phyRxFrequencies_r153)
        result.append(STEP_11_DATA.phyRxFrequencies_r153)
        result.append(456000000)
        result.append(458000000)
    else:
        result.append("INVALID")

    STEP_11_DATA.macChannelSets_r156 = result
    # Row 157
    result = None

    result = 1
    
    STEP_11_DATA.Flash_Security_Enabled_r157 = result
    # Row 158
    result = None

    result = 0
    
    STEP_11_DATA.debugPortEnabled_r158 = result
    # Row 159
    result = None

    result = 2
    
    STEP_11_DATA.appSecurityAuthMode_r159 = result
    # Row 160
    result = None

    result = DTLS_DATA.dtlsNetworkHESubject
    
    STEP_11_DATA.dtlsNetworkHESubject_r160 = result
    # Row 161
    result = None

    result = DTLS_DATA.dtlsNetworkMSSubject
    
    STEP_11_DATA.dtlsNetworkMSSubject_r161 = result
    # Row 162
    result = None

    result = DTLS_DATA.dtlsNetworkRootCA
    
    STEP_11_DATA.dtlsNetworkRootCA_r162 = result
    # Row 163
    result = None

    result = 0
    
    STEP_11_DATA.ipHEContext_r163 = result
    # Row 164
    result = None

    result = 0
    
    STEP_11_DATA.macNetworkId_r164 = result
    # Row 165
    result = None

    result = 85
    
    STEP_11_DATA.opportunisticThreshold_r165 = result
    # Row 166
    result = None

    result = 170
    
    STEP_11_DATA.realtimeThreshold_r166 = result
    # Row 167
    result = None

    result = 85
    
    STEP_11_DATA.realtimeThreshold_DCU_r167 = result
    # Row 168
    result = None

    result = 1
    
    STEP_11_DATA.shipMode_r168 = result
    # Row 169
    result = None

    result = 60
    
    STEP_11_DATA.timeAcceptanceDelay_r169 = result
    # Row 170
    result = None

    result = int(TIME_ZONE_DATA["dstStartRule2"])
    
    STEP_11_DATA.dstStartRule_r170 = result
    # Row 171
    result = None

    result = int(TIME_ZONE_DATA["dstEndRule2"])
    
    STEP_11_DATA.dstEndRule_r171 = result
    # Row 172
    result = None

    result = int(TIME_ZONE_DATA["timeZoneOffset"])
    
    STEP_11_DATA.timeZoneOffset_r172 = result
    # Row 173
    result = None

    result = int(TIME_ZONE_DATA["dstEnabled"])
    
    STEP_11_DATA.dstEnabled_r173 = result
    # Row 174
    result = None

    result = int(TIME_ZONE_DATA["dstOffset"])
    
    STEP_11_DATA.dstOffset_r174 = result
    # Row 175
    result = None

    result = int(TIME_ZONE_DATA["timeZoneDSTHash Decimal"])
    
    STEP_11_DATA.timeZoneDSTHash_r175 = result
    # Row 176
    result = None

    result = (int(USER_ENTRIES.Daily_Shift_Time_r15) % 24)  * 3600
    
    STEP_11_DATA.dailySelfReadTime_r176 = result
    # Row 177
    result = None

    if USER_ENTRIES.Automatic_Demand_Reset_r16 == "Default":
        result = 1
    elif int(USER_ENTRIES.Automatic_Demand_Reset_r16) not in range (1,28+1):
        result == 1
    else:
        result = int(USER_ENTRIES.Automatic_Demand_Reset_r16)
    
    STEP_11_DATA.scheduledDemandResetDay_r177 = result
    # Row 178
    result = None

    if int(USER_ENTRIES.Outage_Last_Gasp_Delay_r17) < 1:
        result = 0
    elif int(USER_ENTRIES.Outage_Last_Gasp_Delay_r17) > 300:
        result = 300
    else:
        result = USER_ENTRIES.Outage_Last_Gasp_Delay_r17  

    STEP_11_DATA.outageDeclarationDelay_r178 = result
    # Row 179
    result = None

    if int(USER_ENTRIES.Restoration_Delay_r18) < 1:
        result = 0
    elif int(USER_ENTRIES.Restoration_Delay_r18) > 300:
        result = 300
    else:
        result = USER_ENTRIES.Restoration_Delay_r18  
    
    STEP_11_DATA.restorationDeclarationDelay_r179 = result

    STEP_11_DATA.validate()

    return STEP_11_DATA