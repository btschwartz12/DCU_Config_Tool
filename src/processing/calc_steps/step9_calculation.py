# step9_calculation.py
# 6/20/22
# Ben Schwartz
#
# Defines the data structure associated with the calculations for
# this step, does all necessary calculations to initialize an instance
# of the data structure, and returns it for future use

# Corresponding Excel worksheet rows: 138-147

from dataclasses import dataclass, fields
from src.processing.calc_steps.freqs_generator import FrequencyData

from src.processing.calc_steps.step5_calculation import Step5Data
from src.processing.calc_steps.step6_calculation import Step6Data
from src.utils.utils import StepData


@dataclass
class Step9Data(StepData):
    EP_Tx_SRFN_Except_DA_r138: list[int] = None
    EP_Tx_SRFN_DA_Except_DA_r139: list[int] = None
    EP_Tx_STAR7200_r140: list[int] = None
    EP_Tx_STAR2400_r141: list[int] = None
    EP_Tx_STAR2400Legacy_r142: list[int] = None
    EP_Rx_SRFN_Except_DA_r143: int = None
    EP_Rx_SRFN_DA_Except_DA_r144: int = None
    EP_Rx_STAR7200_r145: int = None
    EP_Rx_STAR2400_r146: int = None
    EP_Rx_STAR2400Legacy_r147: int = None

def getStep9Data(FREQ_DATA: FrequencyData, DATA_5: Step5Data, DATA_6: Step6Data) -> Step9Data:
    """This will use look at the frequencies and types for each 
    channel of each slot, and record a list of frequencies for each type.
    """   

    STEP_9_DATA = Step9Data()  


    SLOT_2_CHANNEL_DATA = {
        1: {
            "name": DATA_5.Slot_2_Channel_1_r96,
            "freq": DATA_6.Slot_2_Channel_1_r113
        },
        2: {
            "name": DATA_5.Slot_2_Channel_2_r97,
            "freq": DATA_6.Slot_2_Channel_2_r114
        },
        3: {
            "name": DATA_5.Slot_2_Channel_3_r98,
            "freq": DATA_6.Slot_2_Channel_3_r115
        },
        4: {
            "name": DATA_5.Slot_2_Channel_4_r99,
            "freq": DATA_6.Slot_2_Channel_4_r116
        },
        5: {
            "name": DATA_5.Slot_2_Channel_5_r100,
            "freq": DATA_6.Slot_2_Channel_5_r117
        },
        6: {
            "name": DATA_5.Slot_2_Channel_6_r101,
            "freq": DATA_6.Slot_2_Channel_6_r118
        },
        7: {
            "name": DATA_5.Slot_2_Channel_7_r102,
            "freq": DATA_6.Slot_2_Channel_7_r119
        },
        8: {
            "name": DATA_5.Slot_2_Channel_8_r103,
            "freq": DATA_6.Slot_2_Channel_8_r120
        }
    }

    SLOT_3_CHANNEL_DATA = {
        1: {
            "name": DATA_5.Slot_3_Channel_1_r88,
            "freq": DATA_6.Slot_3_Channel_1_r105
        },
        2: {
            "name": DATA_5.Slot_3_Channel_2_r89,
            "freq": DATA_6.Slot_3_Channel_2_r106
        },
        3: {
            "name": DATA_5.Slot_3_Channel_3_r90,
            "freq": DATA_6.Slot_3_Channel_3_r107
        },
        4: {
            "name": DATA_5.Slot_3_Channel_4_r91,
            "freq": DATA_6.Slot_3_Channel_4_r108
        },
        5: {
            "name": DATA_5.Slot_3_Channel_5_r92,
            "freq": DATA_6.Slot_3_Channel_5_r109
        },
        6: {
            "name": DATA_5.Slot_3_Channel_6_r93,
            "freq": DATA_6.Slot_3_Channel_6_r110
        },
        7: {
            "name": DATA_5.Slot_3_Channel_7_r94,
            "freq": DATA_6.Slot_3_Channel_7_r111
        },
        8: {
            "name": DATA_5.Slot_3_Channel_8_r95,
            "freq": DATA_6.Slot_3_Channel_8_r112
        }
    }

    # Row 138
    result = []

    for channel_idx, channel in SLOT_2_CHANNEL_DATA.items():
        if channel["name"] == "SRFN" or channel["name"] == "SRFN*":
            result.append(channel["freq"])
    for channel_idx, channel in SLOT_3_CHANNEL_DATA.items():
        if channel["name"] == "SRFN" or channel["name"] == "SRFN*":
            result.append(channel["freq"])

    STEP_9_DATA.EP_Tx_SRFN_Except_DA_r138 = result
    # Row 139
    result = []

    for channel_idx, channel in SLOT_2_CHANNEL_DATA.items():
        if channel["name"] == "DA":
            result.append(channel["freq"])
    for channel_idx, channel in SLOT_3_CHANNEL_DATA.items():
        if channel["name"] == "DA":
            result.append(channel["freq"])

    STEP_9_DATA.EP_Tx_SRFN_DA_Except_DA_r139 = result
    # Row 140
    result = []

    for channel_idx, channel in SLOT_2_CHANNEL_DATA.items():
        if channel["name"] == "STAR 7200" or channel["name"] == "STAR 7200*":
            result.append(channel["freq"])
    for channel_idx, channel in SLOT_3_CHANNEL_DATA.items():
        if channel["name"] == "STAR 7200" or channel["name"] == "STAR 7200*":
            result.append(channel["freq"])

    STEP_9_DATA.EP_Tx_STAR7200_r140 = result
    # Row 141
    result = []

    for channel_idx, channel in SLOT_2_CHANNEL_DATA.items():
        if channel["name"] == "STAR 2400": # or channel["name"] == "STAR 2400*":
            result.append(channel["freq"])
    for channel_idx, channel in SLOT_3_CHANNEL_DATA.items():
        if channel["name"] == "STAR 2400": # or channel["name"] == "STAR 2400*":
            result.append(channel["freq"])

    STEP_9_DATA.EP_Tx_STAR2400_r141 = result
    # Row 142
    result = []

    for channel_idx, channel in SLOT_2_CHANNEL_DATA.items():
        if channel["name"] == "STAR 2400 Legacy": 
            result.append(channel["freq"])
    for channel_idx, channel in SLOT_3_CHANNEL_DATA.items():
        if channel["name"] == "STAR 2400 Legacy":
            result.append(channel["freq"])

    STEP_9_DATA.EP_Tx_STAR2400Legacy_r142 = result
    # Row 143
    result = None

    if len(STEP_9_DATA.EP_Tx_SRFN_Except_DA_r138) > 0:
        result = int(FREQ_DATA.STAR_F1_Uplink_Frequency_r48 * 1000000)
    else:
        result = None

    STEP_9_DATA.EP_Rx_SRFN_Except_DA_r143 = result
    # Row 144
    result = None

    if len(STEP_9_DATA.EP_Tx_SRFN_DA_Except_DA_r139) > 0:
        result = int(FREQ_DATA.STAR_F1_Uplink_Frequency_r48 * 1000000)
    else:
        result = None

    STEP_9_DATA.EP_Rx_SRFN_DA_Except_DA_r144 = result
    # Row 145
    result = None

    if len(STEP_9_DATA.EP_Tx_STAR7200_r140) > 0:
        result = int(FREQ_DATA.STAR_F2_Downlink_Frequency_r46 * 1000000)
    else:
        result = None

    STEP_9_DATA.EP_Rx_STAR7200_r145 = result
    # Row 146
    result = None

    if len(STEP_9_DATA.EP_Tx_STAR2400_r141) > 0:
        result = int(FREQ_DATA.STAR_F2_Downlink_Frequency_r46 * 1000000)
    else:
        result = None

    STEP_9_DATA.EP_Rx_STAR2400_r146 = result
    # Row 138
    result = None

    if len(STEP_9_DATA.EP_Tx_STAR2400Legacy_r142) > 0:
        result = int(FREQ_DATA.STAR_F2_Downlink_Frequency_r46 * 1000000)
    else:
        result = None

    STEP_9_DATA.EP_Rx_STAR2400Legacy_r147 = result
    

    # STEP_9_DATA.validate()

    return STEP_9_DATA