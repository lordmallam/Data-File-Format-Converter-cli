import json

 # Json import function
def json_importer(file):
    with open(file, 'r') as f:
        data = json.load(f)
        if not isinstance(data, list):
            raise ValueError('Data is not a collection of rows')
        for row in data:
            yield row