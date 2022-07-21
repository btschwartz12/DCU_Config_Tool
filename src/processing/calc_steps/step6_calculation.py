# step6_calculation.py
# 6/20/22
# Ben Schwartz
#
# Defines the data structure associated with the calculations for
# this step, does all necessary calculations to initialize an instance
# of the data structure, and returns it for future use

# Corresponding Excel worksheet rows: 105-120

from dataclasses import dataclass, fields


from src.processing.calc_steps.freqs_generator import FrequencyData
from src.processing.calc_steps.step4_calculation import Step4Data
from src.processing.calc_steps.step5_calculation import Step5Data
from src.utils.utils import StepData

@dataclass
class Step6Data(StepData):
    Slot_3_Channel_1_r105: int = None
    Slot_3_Channel_2_r106: int = None
    Slot_3_Channel_3_r107: int = None
    Slot_3_Channel_4_r108: int = None
    Slot_3_Channel_5_r109: int = None
    Slot_3_Channel_6_r110: int = None
    Slot_3_Channel_7_r111: int = None
    Slot_3_Channel_8_r112: int = None
    Slot_2_Channel_1_r113: int = None
    Slot_2_Channel_2_r114: int = None
    Slot_2_Channel_3_r115: int = None
    Slot_2_Channel_4_r116: int = None
    Slot_2_Channel_5_r117: int = None
    Slot_2_Channel_6_r118: int = None
    Slot_2_Channel_7_r119: int = None
    Slot_2_Channel_8_r120: int = None

def func1(bVal: str, cVal, DATA_FREQ: FrequencyData, DATA_4: Step4Data):
    """Used by B105-B120"""
    result = None
    if bVal == "SRFN*":
        result = int(DATA_FREQ.SRFN_Outbound_Downlink_Frequency_r47 * 1000000)
    elif DATA_4.SRFN_Receiver_Channels_r68 > cVal and (bVal == "SRFN" or bVal == "DA"):
        offset_freq_name = DATA_FREQ.getInboundNameByOffset(offset=cVal)
        offset_freq: float = getattr(DATA_FREQ, offset_freq_name)
        result = int(offset_freq * 1000000)
    elif bVal == "STAR 7200*":
        result = int(DATA_FREQ.STAR_F2_Downlink_Frequency_r46 * 1000000)
    elif bVal == "STAR 7200" or bVal == "STAR 2400" or bVal == "STAR 2400 Legacy":
        result = int(DATA_FREQ.STAR_F1_Uplink_Frequency_r48 * 1000000)
    else:
        print("error 882")
    return result

def func2(val, addend=None):
    """Used by C105-C120"""
    result = None
    if val == "SRFN" or val == "DA":
        result = 1
    else:
        result = 0
    if addend is not None:
        result += addend
    return result



def getStep6Data(DATA_FREQ: FrequencyData, DATA_4: Step4Data, DATA_5: Step5Data):
    """This will use the previously calculated Step4Data, Step5Data,
    and existing FrequencyData to generate a Step6Data object.
    """
    
    STEP_6_DATA = Step6Data()

    # Row 105
    result = None

    result = func1(DATA_5.Slot_3_Channel_1_r88, 0, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_3_Channel_1_r105 = result
    # Row 106
    result = None

    val_c105 = func2(DATA_5.Slot_3_Channel_1_r88)
    result = func1(DATA_5.Slot_3_Channel_2_r89, val_c105, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_3_Channel_2_r106 = result
    # Row 107
    result = None

    val_c106 = func2(DATA_5.Slot_3_Channel_2_r89, val_c105)
    result = func1(DATA_5.Slot_3_Channel_3_r90, val_c106, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_3_Channel_3_r107 = result
    # Row 108
    result = None

    val_c107 = func2(DATA_5.Slot_3_Channel_3_r90, val_c106)
    result = func1(DATA_5.Slot_3_Channel_4_r91, val_c107, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_3_Channel_4_r108 = result
    # Row 109
    result = None

    val_c108 = func2(DATA_5.Slot_3_Channel_4_r91, val_c107)
    result = func1(DATA_5.Slot_3_Channel_5_r92, val_c108, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_3_Channel_5_r109 = result
    # Row 110
    result = None

    val_c109 = func2(DATA_5.Slot_3_Channel_5_r92, val_c108)
    result = func1(DATA_5.Slot_3_Channel_6_r93, val_c109, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_3_Channel_6_r110 = result
    # Row 111
    result = None

    val_c110 = func2(DATA_5.Slot_3_Channel_6_r93, val_c109)
    result = func1(DATA_5.Slot_3_Channel_7_r94, val_c110, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_3_Channel_7_r111 = result
    # Row 112
    result = None

    val_c111 = func2(DATA_5.Slot_3_Channel_7_r94, val_c110)
    result = func1(DATA_5.Slot_3_Channel_8_r95, val_c111, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_3_Channel_8_r112 = result
    # Row 113
    result = None

    val_c112 = func2(DATA_5.Slot_3_Channel_8_r95, val_c111)
    result = func1(DATA_5.Slot_2_Channel_1_r96, val_c112, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_2_Channel_1_r113 = result
    # Row 114
    result = None

    val_c113 = func2(DATA_5.Slot_2_Channel_1_r96, val_c112)
    result = func1(DATA_5.Slot_2_Channel_2_r97, val_c113, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_2_Channel_2_r114 = result
    # Row 115
    result = None

    val_c114 = func2(DATA_5.Slot_2_Channel_2_r97, val_c113)
    result = func1(DATA_5.Slot_2_Channel_3_r98, val_c114, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_2_Channel_3_r115 = result
    # Row 116
    result = None

    val_c115 = func2(DATA_5.Slot_2_Channel_3_r98, val_c114)
    result = func1(DATA_5.Slot_2_Channel_4_r99, val_c115, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_2_Channel_4_r116 = result
    # Row 117
    result = None

    val_c116 = func2(DATA_5.Slot_2_Channel_4_r99, val_c115)
    result = func1(DATA_5.Slot_2_Channel_5_r100, val_c116, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_2_Channel_5_r117 = result
    # Row 118
    result = None

    val_c117 = func2(DATA_5.Slot_2_Channel_5_r100, val_c116)
    result = func1(DATA_5.Slot_2_Channel_6_r101, val_c117, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_2_Channel_6_r118 = result
    # Row 119
    result = None

    val_c118 = func2(DATA_5.Slot_2_Channel_6_r101, val_c117)
    result = func1(DATA_5.Slot_2_Channel_7_r102, val_c118, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_2_Channel_7_r119 = result
    # Row 120
    result = None

    val_c119 = func2(DATA_5.Slot_2_Channel_7_r102, val_c118)
    result = func1(DATA_5.Slot_2_Channel_8_r103, val_c119, DATA_FREQ, DATA_4)

    STEP_6_DATA.Slot_2_Channel_8_r120 = result

    STEP_6_DATA.validate()

    return STEP_6_DATA
