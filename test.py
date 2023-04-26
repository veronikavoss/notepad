import os,json

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

config = {'geometry':[],'find_keyword':'안녕 '}
config['geometry'] = 0,1,2,3

with open(str(os.path.join(CURRENT_PATH,'test.json')),'w') as w:
    json.dump(config,w,indent=4)

with open(str(os.path.join(CURRENT_PATH,'test.json')),'r') as r:
    keyword = json.load(r)['find_keyword']

print(keyword)