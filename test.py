import os,json

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
config = {'geometry':[],'find_keyword':'','find_upndown':'','case_sensitivity':'','wrap_around':''}

try:
    with open(str(os.path.join(CURRENT_PATH,'test.json')),'r') as r:
        print(r.read())
except FileNotFoundError:
    with open(str(os.path.join(CURRENT_PATH,'test.json')),'w') as w:
        json.dump(config,w,indent=4)
# if not r.read():
#     with open(str(os.path.join(CURRENT_PATH,'t.json')),'w') as w:
#         json.dump(config,w,indent=4)
else:
    config_json = json.load(r)

print(config_json)