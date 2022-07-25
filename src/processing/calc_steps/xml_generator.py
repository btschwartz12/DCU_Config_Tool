# xml_generator.py
# 6/20/22
# Ben Schwartz
#
# Takes export data generated from the calculator and 
# converts it to an XML string, according to the schema
# and template xml

from dataclasses import dataclass
import json

import xmlschema
from config.config import Config
from src.processing.wkst_calculator import ExportData
from src.utils.utils import toStr


def getXMLstr(data: ExportData, config: Config) -> str:
    """This will take the data generated from all of the calculations, and create 
    an XML for export. It will first take an example output to get the correct keys, 
    populate with correct values, and convert back into XML using the xmlschema module."""
    XML_DICT = {}

    with open(config.EXPORT_TEMPLATE_JSON_RPATH, 'r') as f:
        XML_DICT.update(json.load(f))

    XML_DICT["metadata"]["CustomerID"] = toStr(data.USER_ENTRIES.Aclara_Customer_ID_r28)
    XML_DICT["metadata"]["CustomerName"] = toStr(data.USER_ENTRIES.Customer_Name_r2)
    XML_DICT["metadata"]["Drawing"] = toStr(data.USER_ENTRIES.DCU_Drawing_Number_r26)
    XML_DICT["metadata"]["Product"] = toStr(data.USER_ENTRIES.DCU_Product_Number_r27)

    XML_DICT["common"]["appSecurityAuthMode"] = toStr(data.DATA_11.appSecurityAuthMode_r159)
    XML_DICT["common"]["dtlsNetworkHESubject"] = toStr(data.DATA_11.dtlsNetworkHESubject_r160)
    XML_DICT["common"]["dtlsNetworkMSSubject"] = toStr(data.DATA_11.dtlsNetworkMSSubject_r161)
    XML_DICT["common"]["dtlsNetworkRootCA"] = toStr(data.DATA_11.dtlsNetworkRootCA_r162)
    XML_DICT["common"]["flashSecurityEnabled"] = toStr(data.DATA_11.Flash_Security_Enabled_r157)
    XML_DICT["common"]["ipHEContext"] = toStr(data.DATA_11.ipHEContext_r163)
    XML_DICT["common"]["macChannelSets"] = toStr(data.DATA_11.macChannelSets_r156) 
    XML_DICT["common"]["macChannelSetsSTAR"] = toStr(data.DATA_11.macChannelSetsSTAR_r155)
    XML_DICT["common"]["macNetworkId"] = toStr(data.DATA_11.macNetworkId_r164)
    XML_DICT["common"]["phyAvailableFrequencies"] = toStr(data.DATA_11.phyAvailableFrequencies_r152)
    XML_DICT["common"]["realtimeThreshold"] = toStr(data.DATA_11.realtimeThreshold_r166)
    XML_DICT["common"]["shipMode"] = toStr(data.DATA_11.shipMode_r168)

    SLOT_2_DICT = {
        "@slot": "2",
        "comDeviceGatewayConfig": toStr(data.DATA_8.comDeviceGatewayConfig_r130),
        "phyRxFrequencies": toStr(data.DATA_8.phyRxFrequencies_r131), 
        "phyTxFrequencies": toStr(data.DATA_8.phyTxFrequencies_r132),
        "phyRxDetection": toStr(data.DATA_8.phyRxDetection_r133),
        "phyRxFraming": toStr(data.DATA_8.phyRxFraming_r134),
        "phyRxMode": toStr(data.DATA_8.phyRxMode_r135)
    }

    SLOT_3_DICT = {
        "@slot": "3",
        "comDeviceGatewayConfig": toStr(data.DATA_7.comDeviceGatewayConfig_r122),
        "phyRxFrequencies": toStr(data.DATA_7.phyRxFrequencies_r123),
        "phyTxFrequencies": toStr(data.DATA_7.phyTxFrequencies_r124),
        "phyRxDetection": toStr(data.DATA_7.phyRxDetection_r125),
        "phyRxFraming": toStr(data.DATA_7.phyRxFraming_r126),
        "phyRxMode": toStr(data.DATA_7.phyRxMode_r127)
    }

    XML_DICT["SRFNI-XCVR"] = [SLOT_2_DICT, SLOT_3_DICT]

    XML_DICT["EXPORT-FORMAT"] = toStr(data.USER_ENTRIES.Tool_Version_r29)

    XML_DICT["SRFNI-METER"]["comDeviceGatewayConfig"] = toStr("EP")
    XML_DICT["SRFNI-METER"]["EPRxFrequencies"] = toStr(data.DATA_9.EP_Rx_SRFN_Except_DA_r143)
    XML_DICT["SRFNI-METER"]["EPTxFrequencies"] = toStr(data.DATA_9.EP_Tx_SRFN_Except_DA_r138)

    XML_DICT["SRFNI-DA"]["comDeviceGatewayConfig"] = toStr("EP")
    XML_DICT["SRFNI-DA"]["EPRxFrequencies"] = toStr(data.DATA_9.EP_Rx_SRFN_DA_Except_DA_r144)
    XML_DICT["SRFNI-DA"]["EPTxFrequencies"] = toStr(data.DATA_9.EP_Tx_SRFN_DA_Except_DA_r139)

    XML_DICT["STARI-METER"]["comDeviceGatewayConfig"] = toStr("EP")
    XML_DICT["STARI-METER"]["EPRxFrequenciesSTAR7200"] = toStr(data.DATA_9.EP_Rx_STAR7200_r145)
    XML_DICT["STARI-METER"]["EPTxFrequenciesSTAR7200"] = toStr(data.DATA_9.EP_Tx_STAR7200_r140)
    XML_DICT["STARI-METER"]["EPRxFrequenciesSTAR2400"] = toStr(data.DATA_9.EP_Rx_STAR2400_r146)
    XML_DICT["STARI-METER"]["EPTxFrequenciesSTAR2400"] = toStr(data.DATA_9.EP_Tx_STAR2400_r141)
    XML_DICT["STARI-METER"]["EPRxFrequenciesSTAR2400Legacy"] = toStr(data.DATA_9.EP_Rx_STAR2400Legacy_r147)
    XML_DICT["STARI-METER"]["EPTxFrequenciesSTAR2400Legacy"] = toStr(data.DATA_9.EP_Tx_STAR2400Legacy_r142)

    schema = xmlschema.XMLSchema(config.EXPORT_SCHEMA_RPATH)
    xml_str = xmlschema.etree_tostring(schema.to_etree(XML_DICT))
    return xml_str
    

    