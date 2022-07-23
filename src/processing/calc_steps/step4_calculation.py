# step4_calculation.py
# 6/20/22
# Ben Schwartz
#
# Defines the data structure associated with the calculations for
# this step, does all necessary calculations to initialize an instance
# of the data structure, and returns it for future use

# Corresponding Excel worksheet rows: 65-86

from dataclasses import dataclass, fields
from src.processing.calc_steps.entry_generator import UserEntries
from src.processing.calc_steps.freqs_generator import FrequencyData
from src.utils.utils import StepData

@dataclass
class Step4Data(StepData):
    DCU_Receive_Channels_Available_r65: int = None
    DCU_Transmitter_Count_r66: int = None
    STAR_Receiver_Channels_Minimum_r67: int = None
    SRFN_Receiver_Channels_r68: int = None
    Channels_Available_for_Diversity_r69: int = None
    STAR_2400_Diverity_Channels_r70: int = None
    STAR_2400_Legacy_Diverity_Channels_r71: int = None
    STAR_7200_Diverity_Channels_r72: int = None
    STAR_Transmit_Frequency_Reserved_Receiver_r73: int = None
    SRFN_Transmit_Frequency_Reserved_Receiver_r74: int = None
    STAR_2400_Legacy_Channels_r75: int = None
    STAR_2400_Channels_Non_Legacy_r76: int = None
    STAR_7200_Channels_r77: int = None
    STAR_Receiver_Channels_r78: int = None
    SRFN_Non_DA_Receive_Channels_r79: int = None
    SRFN_DA_Receive_Channels_r80: int = None
    DCU_Configuration_Description_r81: list[str] = None
    SRFN_Non_DA_Receivers_on_Slot3_r82: int = None
    SRFN_Non_DA_Receivers_on_Slot2_r83: int = None
    Slot3Count_r84: int = None
    Slot2Count_r85: int = None
    DCU_Configuration_r86: str = None


def getStep4Data(USER_ENTRIES: UserEntries, FREQUENCY_DATA: FrequencyData) -> Step4Data:
        """This will use the generated FrequencyData as well as the user 
        entries to populate the required data. See Step4Data for a description
        of fields calculated in this step.
        """
        
        STEP_4_DATA = Step4Data() # Create the data object

        # Row 65
        STEP_4_DATA.DCU_Receive_Channels_Available_r65 = int(USER_ENTRIES.DCU_T_Boards_r24) * 8 #
        # Row 66
        result = None
        if USER_ENTRIES.DCU_Single_Transmit_T_Board_Firmware_r25:
            result = 1
        elif USER_ENTRIES.DCU_T_Boards_r24 == 1: 
            result = 1
        elif (USER_ENTRIES.System_Includes_SRFN_Devices_r22 and 
                    FREQUENCY_DATA.num_inbound_frequencies > 7):
            result = 2
        elif (USER_ENTRIES.System_Includes_STAR_2400_Legacy_devices_r19 or
                USER_ENTRIES.System_Includes_STAR_2400_devices_r20 or
                USER_ENTRIES.System_Includes_STAR_7200_devices_r21) \
                and USER_ENTRIES.System_Includes_SRFN_Devices_r22:
            result = 2 
        else:
            result = 1
        STEP_4_DATA.DCU_Transmitter_Count_r66 = result #
        # Row 67
        addend_1 = (1 if USER_ENTRIES.System_Includes_STAR_2400_Legacy_devices_r19 else 0)
        addend_2 = (1 if USER_ENTRIES.System_Includes_STAR_2400_devices_r20 else 0)
        addend_3 = (1 if USER_ENTRIES.System_Includes_STAR_7200_devices_r21 else 0)
        STEP_4_DATA.STAR_Receiver_Channels_Minimum_r67 = addend_1 + addend_2 + addend_3 #
        # Row 68
        result = None
        if USER_ENTRIES.System_Includes_SRFN_Devices_r22 is False:
            result = 0
        else:
            result = FREQUENCY_DATA.num_inbound_frequencies
        STEP_4_DATA.SRFN_Receiver_Channels_r68 = result
        # Row 69
        result = None
        result = STEP_4_DATA.DCU_Receive_Channels_Available_r65 - STEP_4_DATA.STAR_Receiver_Channels_Minimum_r67 - STEP_4_DATA.SRFN_Receiver_Channels_r68 - STEP_4_DATA.DCU_Transmitter_Count_r66
        if result < 0: result = 0
        STEP_4_DATA.Channels_Available_for_Diversity_r69 = result #
        # Row 70
        result = None
        if USER_ENTRIES.System_Includes_STAR_2400_devices_r20:
            result = STEP_4_DATA.Channels_Available_for_Diversity_r69
            if result > 1: result = 1
        else:
            result = 0
        STEP_4_DATA.STAR_2400_Diverity_Channels_r70 = result
        # Row 71
        result = None
        if USER_ENTRIES.System_Includes_STAR_2400_Legacy_devices_r19:
            result = STEP_4_DATA.Channels_Available_for_Diversity_r69 - STEP_4_DATA.STAR_2400_Diverity_Channels_r70
            if result > 1: result = 1
            elif result < 0: result = 0
        else:
            result = 0
        STEP_4_DATA.STAR_2400_Legacy_Diverity_Channels_r71 = result #
        # Row 72
        result = None
        if USER_ENTRIES.System_Includes_STAR_7200_devices_r21:
            result = STEP_4_DATA.Channels_Available_for_Diversity_r69 - STEP_4_DATA.STAR_2400_Diverity_Channels_r70 - STEP_4_DATA.STAR_2400_Legacy_Diverity_Channels_r71
            if result > 2: result = 2
            elif result < 0: result = 0
        else:
            result = 0
        STEP_4_DATA.STAR_7200_Diverity_Channels_r72 = result
        # Row 73
        result = None
        if (USER_ENTRIES.System_Includes_STAR_7200_devices_r21 or \
            USER_ENTRIES.System_Includes_STAR_2400_devices_r20 or \
            USER_ENTRIES.System_Includes_STAR_2400_Legacy_devices_r19):
           result = 1
        else:
            result = 0
        STEP_4_DATA.STAR_Transmit_Frequency_Reserved_Receiver_r73 = result
        # Row 74
        result = None
        result = STEP_4_DATA.DCU_Transmitter_Count_r66 - STEP_4_DATA.STAR_Transmit_Frequency_Reserved_Receiver_r73
        STEP_4_DATA.SRFN_Transmit_Frequency_Reserved_Receiver_r74 = result
        # Row 75
        result = None
        if USER_ENTRIES.System_Includes_STAR_2400_Legacy_devices_r19:
            result = 1 + STEP_4_DATA.STAR_2400_Legacy_Diverity_Channels_r71
        else:
            result = 0
        STEP_4_DATA.STAR_2400_Legacy_Channels_r75 = result
        # Row 76
        result = None
        if USER_ENTRIES.System_Includes_STAR_2400_devices_r20:
            result = 1 + STEP_4_DATA.STAR_2400_Diverity_Channels_r70
        else:
            result = 0
        STEP_4_DATA.STAR_2400_Channels_Non_Legacy_r76 = result
        # Row 77
        result = None
        if USER_ENTRIES.System_Includes_STAR_7200_devices_r21:
            result = 2 + STEP_4_DATA.STAR_7200_Diverity_Channels_r72
        else:
            result = 0
        STEP_4_DATA.STAR_7200_Channels_r77 = result
        # Row 78
        result = None
        addend_1 = STEP_4_DATA.STAR_7200_Channels_r77 - 1
        addend_2 = STEP_4_DATA.STAR_2400_Channels_Non_Legacy_r76
        addend_3 = STEP_4_DATA.STAR_2400_Legacy_Channels_r75
        addend_4 = STEP_4_DATA.STAR_Transmit_Frequency_Reserved_Receiver_r73
        result = addend_1 + addend_2 + addend_3 + addend_4
        STEP_4_DATA.STAR_Receiver_Channels_r78 = result
        # Row 79
        result = None
        if USER_ENTRIES.System_Includes_SRFN_Devices_r22:
            result = STEP_4_DATA.SRFN_Receiver_Channels_r68 - (1 if USER_ENTRIES.System_Includes_SRFN_Dedicated_DA_Recv_Channel_r23 else 0)
        else:
            result = 0
        result += STEP_4_DATA.SRFN_Transmit_Frequency_Reserved_Receiver_r74
        STEP_4_DATA.SRFN_Non_DA_Receive_Channels_r79 = result
        # Row 80
        result = None
        if USER_ENTRIES.System_Includes_SRFN_Devices_r22:
            result = 1 if USER_ENTRIES.System_Includes_SRFN_Dedicated_DA_Recv_Channel_r23 else 0
        else:
            result = 0
        STEP_4_DATA.SRFN_DA_Receive_Channels_r80 = result
        # Row 81
        result = []
        if USER_ENTRIES.System_Includes_STAR_2400_Legacy_devices_r19:
            result.append('STAR 2400 Legacy')
        if USER_ENTRIES.System_Includes_STAR_2400_devices_r20:
            result.append('STAR 2400')
        if USER_ENTRIES.System_Includes_STAR_7200_devices_r21:
            result.append('STAR 7200')
        if STEP_4_DATA.SRFN_Non_DA_Receive_Channels_r79 > 0:
            result.append('SRFN')
        if STEP_4_DATA.SRFN_DA_Receive_Channels_r80 > 0:
            result.append('DA')
        STEP_4_DATA.DCU_Configuration_Description_r81 = result
        # Row 82
        result = None
        if USER_ENTRIES.System_Includes_SRFN_Devices_r22:
            arg1 = 8 - STEP_4_DATA.SRFN_Transmit_Frequency_Reserved_Receiver_r74 - STEP_4_DATA.SRFN_DA_Receive_Channels_r80
            arg2 = STEP_4_DATA.SRFN_Non_DA_Receive_Channels_r79
            result = min(arg1, arg2)
        else:
            result = 0
        STEP_4_DATA.SRFN_Non_DA_Receivers_on_Slot3_r82 = result
        # Row 83
        result = None
        result = STEP_4_DATA.SRFN_Non_DA_Receive_Channels_r79 \
                - STEP_4_DATA.SRFN_Non_DA_Receivers_on_Slot3_r82 \
                - STEP_4_DATA.SRFN_Transmit_Frequency_Reserved_Receiver_r74
        if result < 0: result = 0
        STEP_4_DATA.SRFN_Non_DA_Receivers_on_Slot2_r83 = result
        # Row 84
        result = None
        arg_1 = STEP_4_DATA.SRFN_Transmit_Frequency_Reserved_Receiver_r74 * (2**9)
        arg_2 = STEP_4_DATA.SRFN_DA_Receive_Channels_r80 * (2**8)
        arg_3 = (2**(7+1)-1)
        
        arg_4_1 = STEP_4_DATA.SRFN_Transmit_Frequency_Reserved_Receiver_r74 if USER_ENTRIES.System_Includes_SRFN_Devices_r22 else 0
        arg_4_2 = STEP_4_DATA.SRFN_DA_Receive_Channels_r80
        arg_4_3 = STEP_4_DATA.SRFN_Non_DA_Receivers_on_Slot3_r82
        arg_4 = 2**(7 - arg_4_1 - arg_4_2 - arg_4_3 + 1) - 1

        result = arg_1 + arg_2 + arg_3 - arg_4
        STEP_4_DATA.Slot3Count_r84 = result
        # Row 85
        result = None
        
        arg_1 = None
        if STEP_4_DATA.SRFN_Transmit_Frequency_Reserved_Receiver_r74 > 1:
            arg_1 = 16384
        else:
            arg_1 = (2**13 + 2**12) if STEP_4_DATA.STAR_7200_Channels_r77 > 0 else 0

        arg_2 = 2**11 if STEP_4_DATA.SRFN_Non_DA_Receivers_on_Slot2_r83 > 0 else 0
        arg_3 = 2**10 if STEP_4_DATA.SRFN_Non_DA_Receivers_on_Slot3_r82 > 1 else 0
        arg_4 = 2**9 if STEP_4_DATA.STAR_2400_Legacy_Channels_r75 > 0 else 0
        arg_5 = 2**8 if STEP_4_DATA.SRFN_Transmit_Frequency_Reserved_Receiver_r74 > 0 else 0
        arg_6 = 2**4 * (2**(max(2 - STEP_4_DATA.SRFN_Non_DA_Receivers_on_Slot3_r82, 0)) - 1)
        arg_7 = 8+4 if STEP_4_DATA.STAR_7200_Diverity_Channels_r72 == 2 else 0
        arg_8 = 8+4 if STEP_4_DATA.STAR_2400_Diverity_Channels_r70 == 1 else 0
        arg_9 = 8+4 if STEP_4_DATA.STAR_2400_Legacy_Diverity_Channels_r71 == 1 else 0

        result = arg_1 + arg_2 + arg_3 + arg_4 + arg_5 + arg_6 + arg_7 + arg_8 + arg_9
        
        STEP_4_DATA.Slot2Count_r85 = result
        # Row 86
        result = ""
        if STEP_4_DATA.Slot3Count_r84 > 63:
            result = "Full Complement"
        elif STEP_4_DATA.Slot3Count_r84 > 31:
                result = "High Density"
        elif STEP_4_DATA.Slot3Count_r84 > 15:
            result = "Low Density"
        else:
            result = "STAR ONLY"
        STEP_4_DATA.DCU_Configuration_r86 = result

        STEP_4_DATA.validate()
        return STEP_4_DATA
                