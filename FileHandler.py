import numpy as np
import pandas as pd

class FileHandler: 
    # Read file and return only the data contained in the "RSSI" column
    def _readFile (filename: str, maxLines: int):
        data = pd.read_csv(filename, usecols=['rssi'], nrows=maxLines)
        if data.empty:
            raise FileNotFoundError('File not found or empty')
        return data
    
    def _parseData (data):
        parsedData = [float(value) for value in data['rssi']]
        adjustedData = np.array(parsedData).reshape(-1,1) - 95 # Adjusting the RSSI values to convert them from percentage to dBm
        return adjustedData

    def readAndParseFile (filename, maxLines): 
        data = FileHandler._readFile(filename, maxLines)
        return FileHandler._parseData(data)