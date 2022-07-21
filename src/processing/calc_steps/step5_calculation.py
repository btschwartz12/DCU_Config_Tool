# step5_calculation.py
# 6/20/22
# Ben Schwartz
#
# Defines the data structure associated with the calculations for
# this step, does all necessary calculations to initialize an instance
# of the data structure, and returns it for future use

# Corresponding Excel worksheet rows: 88-103

from dataclasses import dataclass, fields
from math import floor, log10

from src.processing.calc_steps.step4_calculation import Step4Data
from src.utils.utils import StepData



@dataclass
class Step5Data(StepData):
    Slot_3_Channel_1_r88: str = None
    Slot_3_Channel_2_r89: str = None
    Slot_3_Channel_3_r90: str = None
    Slot_3_Channel_4_r91: str = None
    Slot_3_Channel_5_r92: str = None
    Slot_3_Channel_6_r93: str = None
    Slot_3_Channel_7_r94: str = None
    Slot_3_Channel_8_r95: str = None
    Slot_2_Channel_1_r96: str = None
    Slot_2_Channel_2_r97: str = None
    Slot_2_Channel_3_r98: str = None
    Slot_2_Channel_4_r99: str = None
    Slot_2_Channel_5_r100: str = None
    Slot_2_Channel_6_r101: str = None
    Slot_2_Channel_7_r102: str = None
    Slot_2_Channel_8_r103: str = None

def func1(val: int, powers: tuple):
    """Used in C88-C89"""
    result = None
    if floor(val / 2**powers[0]) > 0:
        result = val - floor(val / 2**powers[0]) * 2**powers[0]
    elif floor(val / 2**powers[1]) > 0:
        result = val - floor(val / 2**powers[1]) * 2**powers[1]
    elif floor(val / 2**powers[2]) > 0:
        result = val - floor(val / 2**powers[2]) * 2**powers[2]
    else:
        result = 0
    return result

def func2(val: int):
    """Used in C90-C95"""  
    result = None
    if val > 0:
        result = val - 2**(floor(log10(val / log10(2))))
    else:
        result = 0
    return result

def func3(val1:int, min:int, val2:int):
    """Used in C97-C103"""
    result = None
    if val1 > min:
        result = val2
    elif val2 > 0:
        result = val2 - 1
    else:
        result = 0
    return result


def getStep5Data(DATA_4: Step4Data) -> Step5Data:
    """This will use the previously calculated Step4Data to 
    generate the Step4Data for step5.
    """
    STEP_5_DATA = Step5Data()

    # Row 88
    result = None
    s3_count_b84 = DATA_4.Slot3Count_r84

    if floor(s3_count_b84 / 2**9) > 0:
        result = "SRFN*"
    elif floor(s3_count_b84 / 2**8) > 0:
        result = "DA"
    elif floor(s3_count_b84 / 2**7) > 0:
        result = "SRFN"
    else:
        result = ""

    STEP_5_DATA.Slot_3_Channel_1_r88 = result
    # Row 89
    result = None

    func1_val_c88 = func1(s3_count_b84, (9, 8, 7))

    if floor(func1_val_c88 / 2**8) > 0:
        result = "DA"
    elif floor(func1_val_c88 / 2**7) > 0:
        result = "SRFN"
    elif floor(func1_val_c88 / 2**6) > 0:
        result = "SRFN"
    else:
        result = ""

    STEP_5_DATA.Slot_3_Channel_2_r89 = result
    #Row 90
    result = None

    func1_val_c89 = func1(func1_val_c88, (8, 7, 6))
    result = "SRFN" if func1_val_c89 > 0 else ""

    STEP_5_DATA.Slot_3_Channel_3_r90 = result
    #Row 91
    result = None

    func2_val_c90 = func2(func1_val_c89)
    result = "SRFN" if func2_val_c90 > 0 else ""

    STEP_5_DATA.Slot_3_Channel_4_r91 = result
    #Row 92
    result = None

    func2_val_c91 = func2(func2_val_c90)
    result = "SRFN" if func2_val_c91 > 0 else ""

    STEP_5_DATA.Slot_3_Channel_5_r92 = result
    #Row 93
    result = None

    func2_val_c92 = func2(func2_val_c91)
    result = "SRFN" if func2_val_c92 > 0 else ""

    STEP_5_DATA.Slot_3_Channel_6_r93 = result
    #Row 94
    result = None

    func2_val_c93 = func2(func2_val_c92)
    result = "SRFN" if func2_val_c93 > 0 else ""

    STEP_5_DATA.Slot_3_Channel_7_r94 = result
    #Row 95
    result = None

    func2_val_c94 = func2(func2_val_c93)
    result = "SRFN" if func2_val_c94 > 0 else ""

    STEP_5_DATA.Slot_3_Channel_8_r95 = result
    #Row 96
    result = None

    if DATA_4.SRFN_Transmit_Frequency_Reserved_Receiver_r74 == 2:
        result = "SRFN*"
    elif DATA_4.STAR_7200_Channels_r77 > 0:
        result = "STAR 7200*"
    elif DATA_4.SRFN_Non_DA_Receivers_on_Slot2_r83 > 0:
        result = "SRFN"
    else:
        result = ""

    STEP_5_DATA.Slot_2_Channel_1_r96 = result
    #Row 97
    result = None
    
    val_c96 = None
    if DATA_4.SRFN_Transmit_Frequency_Reserved_Receiver_r74 == 2 or DATA_4.STAR_7200_Channels_r77 > 0:
        val_c96 = DATA_4.SRFN_Non_DA_Receivers_on_Slot2_r83
    elif DATA_4.SRFN_Non_DA_Receivers_on_Slot2_r83 > 0:
        val_c96 = DATA_4.SRFN_Non_DA_Receivers_on_Slot2_r83 - 1
    else:
        val_c96 = 0

    if DATA_4.STAR_7200_Channels_r77 > 1:
        result = "STAR 7200"
    elif val_c96 > 0:
        result = "SRFN"
    else:
        result = ""

    STEP_5_DATA.Slot_2_Channel_2_r97 = result
    #Row 98
    result = None

    val_c97 = func3(DATA_4.STAR_7200_Channels_r77, 1, val_c96)

    if DATA_4.STAR_2400_Channels_Non_Legacy_r76 > 0:
        result = "STAR 2400"
    elif val_c97 > 0:
        result = "SRFN"
    else:
        result = ""

    STEP_5_DATA.Slot_2_Channel_3_r98 = result
    #Row 99
    result = None

    val_c98 = func3(DATA_4.STAR_2400_Channels_Non_Legacy_r76, 0, val_c97)

    if DATA_4.STAR_2400_Legacy_Channels_r75 > 0:
        result = "STAR 2400 Legacy"
    elif val_c98 > 0:
        result = "SRFN"
    else:
        result = ""

    STEP_5_DATA.Slot_2_Channel_4_r99 = result
    #Row 100
    result = None

    val_c99 = func3(DATA_4.STAR_2400_Legacy_Channels_r75, 0, val_c98)

    if DATA_4.STAR_7200_Channels_r77 > 2:
        result = "STAR 7200*"
    elif val_c99 > 0:
        result = "SRFN"
    else:
        result = ""
    
    STEP_5_DATA.Slot_2_Channel_5_r100 = result
    #Row 101
    result = None

    val_c100 = func3(DATA_4.STAR_7200_Channels_r77, 2, val_c99)

    if DATA_4.STAR_7200_Channels_r77 > 3:
        result = "STAR 7200"
    elif val_c100 > 0:
        result = "SRFN"
    else:
        result = ""

    STEP_5_DATA.Slot_2_Channel_6_r101 = result
    #Row 102
    result = None

    val_c101 = func3(DATA_4.STAR_7200_Channels_r77, 3, val_c100)

    if DATA_4.STAR_2400_Channels_Non_Legacy_r76 > 1:
        result = "STAR 2400"
    elif val_c101 > 0:
        result = "SRFN"
    else:
        result = ""

    STEP_5_DATA.Slot_2_Channel_7_r102 = result
    #Row 103
    result = None

    val_c102 = func3(DATA_4.STAR_2400_Channels_Non_Legacy_r76, 1, val_c101)

    if DATA_4.STAR_2400_Legacy_Channels_r75 > 0:
        result = "STAR 2400 Legacy"
    elif val_c102 > 0:
        result = "SRFN"
    else:
        result = ""

    STEP_5_DATA.Slot_2_Channel_8_r103 = result

    STEP_5_DATA.validate()

    return STEP_5_DATA
