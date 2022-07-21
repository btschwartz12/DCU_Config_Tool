# step7_calculation.py
# 6/20/22
# Ben Schwartz
#
# Defines the data structure associated with the calculations for
# this step, does all necessary calculations to initialize an instance
# of the data structure, and returns it for future use

# Corresponding Excel worksheet rows: 122-128

from dataclasses import dataclass, fields
from src.processing.calc_steps.freqs_generator import FrequencyData

from src.processing.calc_steps.step5_calculation import Step5Data
from src.processing.calc_steps.step6_calculation import Step6Data
from src.utils.utils import StepData


@dataclass
class Step7Data(StepData): # step 7
    comDeviceGatewayConfig_r122: str = None
    phyRxFrequencies_r123: list[str] = None
    phyTxFrequencies_r124: list[int] = None
    phyRxDetection_r125: list[int] = None
    phyRxFraming_r126: list[int] = None
    phyRxMode_r127: list[int] = None
    phyRxDA_r128: list[int] = None

def getStep7Data(FREQ_DATA: FrequencyData, DATA_5: Step5Data, DATA_6: Step6Data):
    """This will use the previously calculated the slot 3 data,
    using the frequency data, as well as computations from step 5 and 6.
    """   

    STEP_7_DATA = Step7Data()   


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

    # Row 122
    result = None

    if DATA_5.Slot_3_Channel_1_r88 == "SRFN*":
        result = "SRFN"
    elif DATA_5.Slot_3_Channel_1_r88 == "STAR 7200*" and DATA_5.Slot_2_Channel_2_r97 != "STAR 7200*":
        result = "STAR"
    else:
        result = "NONE"

    STEP_7_DATA.comDeviceGatewayConfig_r122 = result
    # Row 123
    result = []

    result.append("")
    for channel, data in SLOT_3_CHANNEL_DATA.items():
        result.append(str(data["freq"]))


    STEP_7_DATA.phyRxFrequencies_r123 = result
    # Row 124
    result = []
    # DO WE WANT AN EMPTY LIST VALUE IF ONE IS BLANK? CAN THIS BE BLANK?

    result.append(int(FREQ_DATA.SRFN_Outbound_Downlink_Frequency_r47 * 1000000))
    result.append(int(FREQ_DATA.STAR_F2_Downlink_Frequency_r46 * 1000000))

    STEP_7_DATA.phyTxFrequencies_r124 = result
    # Row 125
    result = []

    val_map = {
        "STAR 7200": 1,
        "STAR 7200*": 1,
        "STAR 2400": 2,
        "STAR 2400*": 2,
        "STAR 2400 Legacy": 3
    }

    result.append(0)
    for channel, data in SLOT_3_CHANNEL_DATA.items():
        name = data["name"]
        val = val_map.get(name)
        if val is None:
            val = 0
        result.append(int(val))

    STEP_7_DATA.phyRxDetection_r125 = result
    # Row 126
    result = []

    val_map = {
        "STAR 7200": 2,
        "STAR 7200*": 2,
        "STAR 2400": 1,
        "STAR 2400*": 1,
        "STAR 2400 Legacy": 1
    }

    result.append(0)
    for channel, data in SLOT_3_CHANNEL_DATA.items():
        name = data["name"]
        val = val_map.get(name)
        if val is None:
            val = 0
        result.append(int(val))

    STEP_7_DATA.phyRxFraming_r126 = result
    # Row 127
    result = []

    val_map = {
        "STAR 7200": 2,
        "STAR 7200*": 2,
        "STAR 2400": 3,
        "STAR 2400*": 3,
        "STAR 2400 Legacy": 3
    }

    result.append(1)
    for channel, data in SLOT_3_CHANNEL_DATA.items():
        name = data["name"]
        val = val_map.get(name)
        if val is None:
            val = 1
        result.append(int(val))

    STEP_7_DATA.phyRxMode_r127 = result
    # Row 128
    result = []

    result.append(0)
    for channel, data in SLOT_3_CHANNEL_DATA.items():
        name = data["name"]
        if name == "DA":
            result.append(1)
        else:
            result.append(0)

    STEP_7_DATA.phyRxDA_r128 = result


    STEP_7_DATA.validate()

    return STEP_7_DATA
