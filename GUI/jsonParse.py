import json

with open('data.json') as file:
	data = json.load( file )

print data[ "voltage" ]
print data[ "direction" ]
