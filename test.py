import json
import xmlschema

schema = xmlschema.XMLSchema('data/export_data/DCU+2XLS.xsd')



with open('new.json', 'r') as f:
    data = json.load(f)


with open("new.xml", "w+") as f:
    f.write(xmlschema.etree_tostring(schema.to_etree(data)))
