import json
import re

def extractFlight(rawData):
    # rawData = "\"\"" + rawData + "\"\""
    rawData = re.sub("'", "\"", rawData)
    data = json.loads(rawData)
    return(data)

def extractTrain(rawData):
    rawData = rawData[1:-1]
    
