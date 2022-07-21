# DTLS_generator.py
# 6/20/22
# Ben Schwartz & Mark Dubuque
#
# Takes user-entered data and generates DTLS info

from dataclasses import dataclass
from src.processing.calc_steps.entry_generator import UserEntries

@dataclass
class DtlsData:
    status: str
    dtlsNetworkHESubject: str
    dtlsNetworkMSSubject: str
    dtlsNetworkRootCA: str


def getDtlsData(USER_ENTRIES: UserEntries, LOCATION_DATA: dict) -> DtlsData: 
    """This will extract relevent data from self.entry_data
    and feed it to networkMaterialDTLS.py, where the DTLS data will
    be calculated and returned.
    
    Data Used: Country, State, and City entered
    Corresponding excel rows: 37-39 and 41-44
    Step(s) / Block(s): 1, 2
    """
    # Getting entry data
    selected_country = USER_ENTRIES.Country_r4
    selected_state = USER_ENTRIES.State_r5
    selected_city = USER_ENTRIES.City_r6
    # Using stored location data
    iso_code = LOCATION_DATA[selected_country]["ISO_CODE"]
    selected_state_abbreviation = LOCATION_DATA[selected_country]["states"][selected_state]["code"]
    # Formatting data so it can be used by networkMaterialDTLS.py
    organization = selected_city + ", City of ("+selected_state_abbreviation+")"
    certificate_country = iso_code
    certificate_state = selected_state
    locality_name = selected_city
    # Now fetching DTLS info
    dtls_data_dict = getNetworkPublicKeyInformation(organization, certificate_country, certificate_state, locality_name)
    DTLS_DATA = DtlsData(**dtls_data_dict)
    # Store as dataclass then return
    return DTLS_DATA

#Name: networkMaterialDTLS.py
#Purpose: Calculates dtlsNetworkHESubject, dtlsNetworkMSSubject, dtlsNetworkRootCA parameters
def getNetworkPublicKeyInformation(Organization,CountryIsoCode,State,Locality) -> dict:

    org = __getFirstNCharacters(Organization,20)
    iso = __getFirstNCharacters(CountryIsoCode,2)
    sta = __getFirstNCharacters(State,14)
    loc = __getFirstNCharacters(Locality,14)
    HeadEnd = "HE"
    Metershop = "MS"
    
    orgID="060355040A"
    orgFormat="UTF-8"
    isoID="0603550406"
    isoFormat="Printable String"
    staID="0603550408"
    staFormat="UTF-8"
    locID="0603550407"
    locFormat="UTF-8"
    HeadEndID="0603550403"
    HeadEndFormat="UTF-8"
    MetershopID="0603550403"
    MetershopFormat="UTF-8"
    Params = list()
    Params.append([org,__getNetworkObjectParam(org,orgID,orgFormat)])
    Params.append([iso,__getNetworkObjectParam(iso,isoID,isoFormat)])
    Params.append([sta,__getNetworkObjectParam(sta,staID,staFormat)])
    Params.append([loc,__getNetworkObjectParam(loc,locID,locFormat)])
    Params.append([HeadEnd,__getNetworkObjectParam(HeadEnd,HeadEndID,HeadEndFormat)])
    Params.append([Metershop,__getNetworkObjectParam(Metershop,MetershopID,MetershopFormat)])
    HESequence = 2 + len(org)+(len(orgID)-1)+2 + len(iso)+(len(isoID)-1)+2 + len(sta)+(len(staID)-1)+2 + len(loc)+(len(locID)-1)+2 + len(HeadEnd)+(len(HeadEndID)-1)+2   
    MSSequence = 2 + len(org)+(len(orgID)-1)+2 + len(iso)+(len(isoID)-1)+2 + len(sta)+(len(staID)-1)+2 + len(loc)+(len(locID)-1)+2 + len(Metershop)+(len(MetershopID)-1)+2
    dtlsNetworkHESubject = "30" + __DEC2HEX(HESequence,2) + "30"+ __DEC2HEX(HESequence-2,2) + __getNetworkDescriptionParam(Params,iso) + __getNetworkDescriptionParam(Params,sta) + __getNetworkDescriptionParam(Params,loc) + __getNetworkDescriptionParam(Params,org) + __getNetworkDescriptionParam(Params,HeadEnd)
    dtlsNetworkMSSubject = "30" + __DEC2HEX(MSSequence,2) + "30"+ __DEC2HEX(MSSequence-2,2) + __getNetworkDescriptionParam(Params,iso) + __getNetworkDescriptionParam(Params,sta) + __getNetworkDescriptionParam(Params,loc) + __getNetworkDescriptionParam(Params,org) + __getNetworkDescriptionParam(Params,Metershop)
    dtlsNetworkRootCA = "308201A43082014AA003020102020100300A06082A8648CE3D040302302B310F300D060355040A0C0641636C6172613118301606035504030C0F5574696C69747920526F6F742043413020170D3135303631303134303030305A180F39393939313233313233353935395A302B310F300D060355040A0C0641636C6172613118301606035504030C0F5574696C69747920526F6F742043413059301306072A8648CE3D020106082A8648CE3D030107034200046D6AB634B5E43A877DAFD4A366A39D0649C2E12343C78AF3E9B8E709D8D964F90FA95DC67041DBF1CC76D4E33A18C2978DEEAD8ACF65A331F3FADD3D4A86F555A353D05B300C0603551D13040530030101FF300B0603551D0F040403020106301D0603551D0E041604141BC0464EFCFBE686CF552DBF57C874D22AB71CE9301F0603551D230418301680141BC0464EFCFBE686CF552DBF57C874D22AB71CE9300A06082A8648CE3D040302034800304502204DA370417281033DB1139AAF2D7859F9B291E4DE2C2D8F7D955DC7B41EA88980022100D8C622BD34548441D4CC9472226B2CC541C3A46D4EB6A5035DFA4E9A6529FD8C"
    
    Status = "Data Looks Ok"
    if min(len(org),len(iso),len(sta),len(loc),len(HeadEnd),len(Metershop))<1:
        Status = "Please fill in all cells"
    if not len(dtlsNetworkHESubject)== (HESequence+2)*2:
        Status = "Head End Certificate Error"
    if not len(dtlsNetworkMSSubject)== (MSSequence+2)*2:
        Status = "Meter Shop Certificate Error"    
    if (max(int(HESequence),int(HESequence))>111 or max(len(org),len(iso),len(sta),len(loc),len(HeadEnd),len(Metershop)))<1:
        Status = "Text String is to large"

    results = {
        "status": Status,
        "dtlsNetworkHESubject": dtlsNetworkHESubject,
        "dtlsNetworkMSSubject": dtlsNetworkMSSubject,
        "dtlsNetworkRootCA": dtlsNetworkRootCA
    }
    
    return results

def __getNetworkDescriptionParam(thisList,thisString):
    response = ""
    for thispair in thisList:
        if thispair[0] ==  thisString:
            response = thispair[1]
    return response        

def __getNetworkObjectParam(myName,myObject,myFormat):
    baselength = len(myName)
    setlength = baselength+(len(myObject)-1)
    asciitext = __getAsciiValue(myName,True)
    if myFormat in ['utf-8', 'UTF-8']:
        formatValue="0C"
    if myFormat in ['printable string', 'Printable String']:
        formatValue="13"
    networkObjectParam = "31" + __DEC2HEX(setlength,2) + "30" + __DEC2HEX(setlength-2,2) + myObject + formatValue + __DEC2HEX(baselength,2,False) + asciitext
    networkObjectParam = __convertAsciiCase(networkObjectParam,True)
    return networkObjectParam

def __convertAsciiCase(thisString,Upper=True):
    if Upper:
        newString = thisString.upper()
    else:
        newString = thisString.lower()
    return newString

def __getAsciiValue(thisString,hexformat=True):
    ascii_equivalent = ""
    for character in thisString:
        ascii_equivalent = ascii_equivalent + str((ord(character)))   
    if hexformat:
        ascii_equivalent = __convertASCII2HexString(thisString)    
    return ascii_equivalent

def __DEC2HEX(decimalvalue,padlength=0,add0x=False):
    h = hex(int(decimalvalue))[2:]  # [2:] removes 0x
    if not padlength == 0:
        h=h.zfill(int(padlength))
    if add0x:
        h = "0x" + h
    return h

# def HEX2DEC(hexvalue):
#     return int(hexvalue, 16)
    
def __getFirstNCharacters(thisString,number):
    return thisString[ 0 : number ]

def __convertASCII2HexString(thisString):
    s=thisString.encode()
    s=s.hex()
    return s
