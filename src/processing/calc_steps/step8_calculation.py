# step8_calculation.py
# 6/20/22
# Ben Schwartz
#
# Defines the data structure associated with the calculations for
# this step, does all necessary calculations to initialize an instance
# of the data structure, and returns it for future use

# Corresponding Excel worksheet rows: 130-136

from dataclasses import dataclass, fields
from src.processing.calc_steps.freqs_generator import FrequencyData
from src.processing.calc_steps.step4_calculation import Step4Data

from src.processing.calc_steps.step5_calculation import Step5Data
from src.processing.calc_steps.step6_calculation import Step6Data
from src.processing.calc_steps.step7_calculation import Step7Data
from src.utils.utils import StepData


@dataclass
class Step8Data(StepData): # step 8
    comDeviceGatewayConfig_r130: str = None
    phyRxFrequencies_r131: list[str] = None
    phyTxFrequencies_r132: list[int] = None
    phyRxDetection_r133: list[int] = None
    phyRxFraming_r134: list[int] = None
    phyRxMode_r135: list[int] = None
    phyRxDA_r136: list[int] = None

def getStep8Data(FREQ_DATA: FrequencyData, DATA_4: Step4Data, DATA_5: Step5Data, DATA_6: Step6Data, DATA_7: Step7Data) -> Step8Data:
    """This will use the previously calculated the slot 2 data,
    using the frequency data, as well as computations from step 5 and 6.
    """   

    STEP_8_DATA = Step8Data()  


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

    # Row 130
    result = None

    if DATA_5.Slot_2_Channel_1_r96 == "SRFN*":
        result = "NONE" if DATA_7.comDeviceGatewayConfig_r122 == "SRFN" else "SRFN"
    elif DATA_5.Slot_2_Channel_1_r96 == "STAR 7200*" or (DATA_4.STAR_Receiver_Channels_Minimum_r67 > 0 
            and DATA_7.comDeviceGatewayConfig_r122 != "STAR 7200*"):
        result = "STAR"
    else:
        result = "NONE"

    STEP_8_DATA.comDeviceGatewayConfig_r130 = result
    # Row 131
    result = []

    result.append("")
    for channel, data in SLOT_2_CHANNEL_DATA.items():
        if data["freq"] is None:
            result.append("")
        else:
            result.append(str(data["freq"]))


    STEP_8_DATA.phyRxFrequencies_r131 = result
    # Row 132
    result = []
    # DO WE WANT AN EMPTY LIST VALUE IF ONE IS BLANK? CAN THIS BE BLANK?

    result.append(int(FREQ_DATA.SRFN_Outbound_Downlink_Frequency_r47 * 1000000))
    result.append(int(FREQ_DATA.STAR_F2_Downlink_Frequency_r46 * 1000000))

    STEP_8_DATA.phyTxFrequencies_r132 = result
    # Row 133
    result = []

    val_map = {
        "STAR 7200": 1,
        "STAR 7200*": 1,
        "STAR 2400": 2,
        "STAR 2400*": 2,
        "STAR 2400 Legacy": 4
    }

    result.append(0)
    for channel, data in SLOT_2_CHANNEL_DATA.items():
        name = data["name"]
        val = val_map.get(name)
        if val is None:
            val = 0
        result.append(int(val))

    STEP_8_DATA.phyRxDetection_r133 = result
    # Row 134
    result = []

    val_map = {
        "STAR 7200": 2,
        "STAR 7200*": 2,
        "STAR 2400": 1,
        "STAR 2400*": 1,
        "STAR 2400 Legacy": 1
    }

    result.append(0)
    for channel, data in SLOT_2_CHANNEL_DATA.items():
        name = data["name"]
        val = val_map.get(name)
        if val is None:
            val = 0
        result.append(int(val))

    STEP_8_DATA.phyRxFraming_r134 = result
    # Row 135
    result = []

    val_map = {
        "STAR 7200": 2,
        "STAR 7200*": 2,
        "STAR 2400": 3,
        "STAR 2400*": 3,
        "STAR 2400 Legacy": 3
    }

    result.append(1)
    for channel, data in SLOT_2_CHANNEL_DATA.items():
        name = data["name"]
        val = val_map.get(name)
        if val is None:
            val = 1
        result.append(int(val))

    STEP_8_DATA.phyRxMode_r135 = result
    # Row 136
    result = []

    result.append(0)
    for channel, data in SLOT_2_CHANNEL_DATA.items():
        name = data["name"]
        if name == "DA":
            result.append(1)
        else:
            result.append(0)

    STEP_8_DATA.phyRxDA_r136 = result

    STEP_8_DATA.validate()

    return STEP_8_DATA