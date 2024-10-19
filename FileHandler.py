import numpy as np
import pandas as pd

class FileHandler:
    # Read file and return only the data contained in the "RSSI" column
    def _readFile (filename: str, maxLines):
        data = pd.read_csv(filename, usecols=['rssi', 'max_magnitude'], nrows=maxLines)
        if data.empty:
            raise FileNotFoundError('File not found or empty')
        return data

    def _parseData (data):
        parsedData = np.array (data[['rssi', 'max_magnitude']])
        parsedData[:, 0] = parsedData[:, 0] - 95
        return parsedData

    def readAndParseFile (filename, maxLines):
        data = FileHandler._readFile(filename, maxLines)
        return FileHandler._parseData(data)