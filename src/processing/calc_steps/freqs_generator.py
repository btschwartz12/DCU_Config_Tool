from dataclasses import dataclass, fields
import json
from tkinter import messagebox
from openpyxl import load_workbook


from src.utils.utils import StepData


WB_NAME = 'customer_wkst/ExcelTool/exampleWorksheet.xlsx'
SHEET_NAME = "CustomerFreqs"


class UnassignedFrequencyException(Exception):
    def __init__(self, freqs):
        self.freqs = freqs

@dataclass
class FrequencyData(StepData):
    """This contains the frequency values provided by the excel sheet.
    ALl frequencies will be loaded, but there is a possibility that some are
    not included in the export, depending on if the user indicated weather or not the system 
    included STAR/SRFN devices"""
    # Unassign - warn and don't use
    STAR_F2_Downlink_Frequency_r46: float = None
    SRFN_Outbound_Downlink_Frequency_r47: float = None
    STAR_F1_Uplink_Frequency_r48: float = None
    SRFN_Inbound_Uplink_Frequency_0_r49: float = None
    SRFN_Inbound_Uplink_Frequency_1_r50: float = None
    SRFN_Inbound_Uplink_Frequency_2_r51: float = None
    SRFN_Inbound_Uplink_Frequency_3_r52: float = None
    SRFN_Inbound_Uplink_Frequency_4_r53: float = None
    SRFN_Inbound_Uplink_Frequency_5_r54: float = None
    SRFN_Inbound_Uplink_Frequency_6_r55: float = None
    SRFN_Inbound_Uplink_Frequency_7_r56: float = None
    SRFN_Inbound_Uplink_Frequency_8_r57: float = None
    SRFN_Inbound_Uplink_Frequency_9_r58: float = None
    SRFN_Inbound_Uplink_Frequency_10_r59: float = None
    SRFN_Inbound_Uplink_Frequency_11_r60: float = None
    SRFN_Inbound_Uplink_Frequency_12_r61: float = None
    SRFN_Inbound_Uplink_Frequency_13_r62: float = None
    SRFN_Inbound_Uplink_Frequency_14_r63: float = None
    num_inbound_frequencies: int = None

    def getInboundFieldNames(self):
        names = []
        for field_data in fields(self):
            if "SRFN_Inbound_Uplink_Frequency" in field_data.name:
                names.append(field_data.name)
        return names

    def getInboundNameByOffset(self, offset):
        inbound_names = self.getInboundFieldNames()
        val = getattr(self, inbound_names[offset])
        if val is None:
            raise Exception("error 810: "+str(inbound_names[offset])+" value is not initialized")
        else:
            return inbound_names[offset]
        


class _FrequencyGenerator:
    """This will get the customer frequencies from the Excel sheet,
    so that they can be used for DTLS calculations"""
    def __init__(self, wb_name, sheet_name):
        self.wb_name = wb_name
        self.sheet_name = sheet_name
        self.frequency_objs = []

        self.unassigned_freqs = []

        

    def getFrequencyData(self, debug=False) -> FrequencyData:

        if not debug:
            self.__loadFreqs()

        inbound_freqs = []
        unassigned_freqs = []
        has_f1 = False
        has_f2 = False
        has_outbound = False

        frequency_data = FrequencyData()
        
        for frequency_obj in self.frequency_objs:
            use = frequency_obj["Frequency Use"]
            frequency = float(frequency_obj["Frequency"])

            if use == 'F1':
                if frequency_data.STAR_F1_Uplink_Frequency_r48 is not None:
                    raise Exception("error 330: multiple F1 frequencies provided ("+str(frequency_data.STAR_F1_Uplink_Frequency_r48)+", "+str(frequency)+")")
                has_f1 = True
                frequency_data.STAR_F1_Uplink_Frequency_r48 = frequency
            elif use == 'F2':
                if frequency_data.STAR_F2_Downlink_Frequency_r46 is not None:
                    raise Exception("error 331: multiple F2 frequencies provided ("+str(frequency_data.STAR_F2_Downlink_Frequency_r46)+", "+str(frequency)+")")
                has_f2 = True
                frequency_data.STAR_F2_Downlink_Frequency_r46 = frequency
            
            elif use == 'OUTBOUND':
                if frequency_data.SRFN_Outbound_Downlink_Frequency_r47 is not None:
                    raise Exception("error 332: multiple outbound frequencies provided ("+str(frequency_data.SRFN_Outbound_Downlink_Frequency_r47)+", "+str(frequency)+")")
                has_outbound = True
                frequency_data.SRFN_Outbound_Downlink_Frequency_r47 = frequency

            elif use == 'UNASSIGN':
                unassigned_freqs.append(frequency)

            elif use == 'INBOUND':
                inbound_freqs.append(frequency)

        if not has_f1:
            raise Exception("error 340: F1 frequency not provided")
        if not has_f2:
            raise Exception("error 340: F2 frequency not provided")
        if not has_outbound:
            raise Exception("error 340: outbound frequency not provided")

        if unassigned_freqs != []:
            self.unassigned_freqs = unassigned_freqs

        inbound_field_names = frequency_data.getInboundFieldNames()

        inbound_freqs.sort()

        for i, frequency in enumerate(inbound_freqs):
            setattr(frequency_data, inbound_field_names[i], frequency)

        frequency_data.num_inbound_frequencies = len(inbound_freqs)


        return frequency_data
            
    def getFrequency_objs(self):
        return self.frequency_objs

    def __loadFreqs(self):
        """This will use an Excel parser to grab the customer frequencies
        and the data associated with them and return a list containing 
        each frequency data entry"""
        workbook = load_workbook(self.wb_name)
        
        sheet = workbook[self.sheet_name]

        freq_entries = []

        for row in range(2, 18):
            freq_entry = {}

            if sheet['A'+str(row)].value == ' ' or sheet['A'+str(row)].value is None:
                break

            for col in range(0, 12):
                col_letter = chr(col + 65) # converts col number to letter
                key_cell = col_letter+'1'
                key = sheet[key_cell].value

                val_cell = col_letter+str(row)
                val = sheet[val_cell].value

                freq_entry[key] = val
            
            freq_entries.append(freq_entry)

        self.frequency_objs = freq_entries
            

def getFrequencyData(debug=False, freq_fn=None) -> FrequencyData:
        """This will extract relevent data from the frequencies in the excel tool,
        and create a data structure that stores the F1, F2, Outbound, and sorted Inbound 
        frequencies. If there is an unassigned frequency, a message will be shown.
        
        Data Used: Frequency data from Excel page
        Corresponding excel rows: 46-63
        Step(s) / Block(s): 3
        """
        try: # Getting the frequencies from the excel tool and constructing the FrequencyData struct
            frequency_generator = _FrequencyGenerator(WB_NAME, SHEET_NAME)
            
            if debug:
                with open(freq_fn, 'r') as f:
                    data = json.load(f)
                frequency_generator.frequency_objs = data
                frequency_data: FrequencyData = frequency_generator.getFrequencyData(debug=True)
            else:
                frequency_data: FrequencyData = frequency_generator.getFrequencyData()

        except Exception as e:
            raise e

        unassigned_freqs = frequency_generator.unassigned_freqs
        if unassigned_freqs != []:
            # messagebox.showinfo("Unassigned frequencies", "There are "+str(len(unassigned_freqs))+" unassigned frequencies: "+str(unassigned_freqs))
            print("Unassigned frequencies", "There are "+str(len(unassigned_freqs))+" unassigned frequencies: "+str(unassigned_freqs))

        return frequency_data