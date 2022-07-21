# step10_calculation.py
# 6/20/22
# Ben Schwartz
#
# Defines the data structure associated with the calculations for
# this step, does all necessary calculations to initialize an instance
# of the data structure, and returns it for future use

# Corresponding Excel worksheet rows: 149-150

from dataclasses import dataclass, fields
from src.processing.calc_steps.freqs_generator import FrequencyData

from src.processing.calc_steps.step5_calculation import Step5Data
from src.processing.calc_steps.step6_calculation import Step6Data
from src.utils.utils import StepData


@dataclass
class Step10Data(StepData):
    All_STAR_and_SRFN_Frequencies_r149: list[int] = None
    SRFN_Endpoint_Inbound_Transmit_Frequencies_r150: list[int] = None


def getStep10Data(FREQ_DATA: FrequencyData) -> Step10Data:
    """This will look at all frequencies, and generate lists of 
    frequencies.
    """   

    STEP_10_DATA = Step10Data()  

    # Row 149
    result = []

    inbound_names = FREQ_DATA.getInboundFieldNames()

    for inbound_varname in inbound_names:
        freq = getattr(FREQ_DATA, inbound_varname)
        if freq is not None:
            result.append(int(freq * 1000000))

    if FREQ_DATA.STAR_F1_Uplink_Frequency_r48 is not None:
        result.append(int(FREQ_DATA.STAR_F1_Uplink_Frequency_r48 * 1000000))
    if FREQ_DATA.SRFN_Outbound_Downlink_Frequency_r47 is not None:
        result.append(int(FREQ_DATA.SRFN_Outbound_Downlink_Frequency_r47 * 1000000))
    if FREQ_DATA.STAR_F2_Downlink_Frequency_r46 is not None:
        result.append(int(FREQ_DATA.STAR_F2_Downlink_Frequency_r46 * 1000000))
    
    STEP_10_DATA.All_STAR_and_SRFN_Frequencies_r149 = result
    # Row 150
    result = []

    if FREQ_DATA.SRFN_Outbound_Downlink_Frequency_r47 is not None:
        result.append(int(FREQ_DATA.SRFN_Outbound_Downlink_Frequency_r47 * 1000000))
    
    for inbound_varname in inbound_names:
        freq = getattr(FREQ_DATA, inbound_varname)
        if freq is not None:
            result.append(int(freq * 1000000))

    STEP_10_DATA.SRFN_Endpoint_Inbound_Transmit_Frequencies_r150 = result
   
    STEP_10_DATA.validate()

    return STEP_10_DATA