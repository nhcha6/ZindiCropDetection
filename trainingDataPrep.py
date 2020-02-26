import numpy as np
from scipy.stats import skew

# function to convert fieldDictTrain to group all data from different pixels together under each date.
def groupPixelsByDate(fieldDictOld, trainFlag):
    fieldDictNew = {}
    cropData = {}
    for fieldNo, fieldData in fieldDictOld.items():
        if trainFlag:
            cropData[fieldNo] = fieldData[0]
            fieldPixels = fieldData[1:]
        else:
            fieldPixels = fieldData
        newFieldData = []
        for i in range(len(fieldPixels[0])):
            newDateData = []
            for pixel in fieldPixels:
                newDateData.extend(pixel[i])
            newFieldData.append(newDateData)
        fieldDictNew[fieldNo] = newFieldData
    return fieldDictNew, cropData

# get data from each tile
for tile in range(2,3):
    fieldArray = np.load(f'data/fieldArray{tile}.npy', allow_pickle=True)
    cropArray = np.load(f'data/cropArray{tile}.npy', allow_pickle=True)
    pixelDataArray = np.load(f'data/pixelDataArray{tile}.npy', allow_pickle=True)

    '''create array of pixel data for training/testing, which is a list of pixel data points: ie. a list of corresponding to
    each date, containing a list of values for each band'''
    trainPixelData = []
    testPixelData = []

    '''create array of crop data, which is a list where each element is a list representing the probability of a pixel being
    each of the crop types. In training we know the crop type, so for each pixel this is a list of 0s and 1 at the index of
    the actual crop type of that pixel'''
    trainCropData = []
    noCropTypes=7
    noBands = 13

    '''also hold field data for future model, which is just the field number for each pixel'''
    trainFieldData = []
    testFieldData = []

    """alternative test data combines field data and takes descriptive statistics for given data/band.
    currently produces test and train dictionaries with keys as field types and a list of pixel data (dates and bands)
    as values. The first element of the train value is the crop type in matrix probability form."""
    fieldDictTrain = {}
    fieldDictTest = {}
    nrows, ncols = np.shape(cropArray)
    for row in range(nrows):
        print(row)
        for col in range(ncols):
            if cropArray[row, col] != 0:
                if fieldArray[row, col] not in fieldDictTrain.keys():
                    cropProb = [0] * noCropTypes
                    # set 1 at index corresponding to that crop type
                    cropProb[cropArray[row, col] - 1] = 1
                    fieldDictTrain[fieldArray[row, col]] = [cropProb]
                fieldDictTrain[fieldArray[row, col]].append(pixelDataArray[row, col])
            elif fieldArray[row, col] != 0:
                if fieldArray[row, col] not in fieldDictTest.items():
                    fieldDictTest[fieldArray[row, col]] = [pixelDataArray[row, col]]
                else:
                    fieldDictTest[fieldArray[row, col]].add(pixelDataArray[row, col])
    print(fieldDictTrain)
    print(fieldDictTest)

    # call function to convert fieldDictTrain to group all data from different pixels together under each date in a
    # concatenated list
    fieldDictTrain, cropDataDict = groupPixelsByDate(fieldDictTrain, True)
    fieldDictTest, cropTestDummy = groupPixelsByDate(fieldDictTest, False)

    # convert to training/testing lists
    np.save(f'data/trainCropData{tile}.npy', np.asarray(trainCropData))
    np.save(f'data/trainFieldData{tile}.npy', np.asarray(trainFieldData))
    np.save(f'data/trainPixelData{tile}.npy', np.asarray(trainPixelData))
    np.save(f'data/testFieldData{tile}.npy', np.asarray(testFieldData))
    np.save(f'data/testPixelData{tile}.npy', np.asarray(testPixelData))

