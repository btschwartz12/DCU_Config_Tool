import xmlschema

schema_fn = 'data/export_data/DCU+2XLS.xsd'
template_fn = 'data/export_data/DCU2+XLS_TEMPLATE.xml'


schema = xmlschema.XMLSchema(schema_fn)
data = schema.to_dict(template_fn)


data["test"] = "dog"
data["metadata"]["CustomerID"] = "Evan"

def iterdict(d):
  for k,v in d.items():        
     if isinstance(v, dict):
         iterdict(v)
    
     else:      
        if isinstance(v, list):
            for l in v:
                iterdict(l)      
        if v == None:
            d[k] = ""
        
iterdict(data)


with open('my.xml', 'w+') as f:
    xml_str = xmlschema.etree_tostring(schema.to_etree(data))
    f.write(xml_str)