# Required libraries
import datetime
import tifffile as tiff
import numpy as np
import glob
import csv


def load_file(fp):
    """Takes a PosixPath object or string filepath
    and returns np array"""
    return tiff.imread(fp.__str__())

# Get a list of dates that an observation from Sentinel-2 is provided for from the currently downloaded imagery
tile_dates = {}
for f in glob.glob('**/*.tif', recursive=True):
    if len(f.split('/')) != 4:
        continue
    tile_id = f.split('/')[1]
    date = datetime.datetime.strptime(f.split('/')[2], '%Y%m%d')
    if tile_dates.get(tile_id, None) is None:
        tile_dates[tile_id] = []
    tile_dates[tile_id].append(date)

for tile_id, dates in tile_dates.items():
    tile_dates[tile_id] = list(set(tile_dates[tile_id]))

selected_tile = list(tile_dates.keys())[0]
dates = sorted(tile_dates[selected_tile])

bands = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B8A', 'B09', 'B11', 'B12', 'CLD']

pixelDataDict = {}
fieldDict = {}
cropDict = {}

for tile in range(4):
    fieldFile = f'data/0{tile}/{tile}_field_id.tif'
    cropFile = f'data/0{tile}/{tile}_label.tif'
    fieldDict[tile] = load_file(fieldFile)
    cropDict[tile] = load_file(cropFile)

for tile in range(4):
    numRows = len(fieldDict[tile])
    numCol = len(fieldDict[tile][0])
    tempMatrix = np.empty((numRows, numCol, len(dates), len(bands)))
    for dateIndex,date in enumerate(dates):
        dateString = ''.join(str(date.date()).split('-'))
        for bandIndex,band in enumerate(bands):
            # load image
            tempBandFile = f'data/0{tile}/{dateString}/{tile}_{band}_{dateString}.tif'
            tempBandImage = load_file(tempBandFile)
            # convulution operation to check for features
            print(tempBandImage)
            for row in range(numRows):
                for col in range(numCol):
                    tempMatrix[row,col,dateIndex,bandIndex] = tempBandImage[row][col]
    pixelDataDict[tile] = tempMatrix


















