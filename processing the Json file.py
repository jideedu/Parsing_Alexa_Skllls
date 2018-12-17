import json
from pprint import pprint

############load the file
    
print('NOW WE LOAD AND PRINT THE FILE')
alll = []
with open('file.json', "r") as f:    
    for line in f:
        jsonobj = json.loads(line)
        print(jsonobj['name'])

        #loading all the file into an array
        alll.append(jsonobj)

#printing the file from an array
for i,json in enumerate(alll):
    print('{} object is: {}'.format(i,alll[i]['name']))
