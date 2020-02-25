import numpy as np

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

    '''also hold field data for future model, which is just the field number for each pixel'''
    trainFieldData = []
    testFieldData = []


    # crops with value != 0 are for training, otherwise they are for testing
    nrows,ncols = np.shape(cropArray)
    for row in range(nrows):
        print(row)
        for col in range(ncols):
            if cropArray[row,col]!=0:
                trainPixelData.append(pixelDataArray[row,col])
                cropProb=[0]*noCropTypes
                # set 1 at index corresponding to that crop type
                cropProb[cropArray[row,col]-1]=1
                trainCropData.append(cropProb)
                trainFieldData.append(fieldArray[row,col])
            elif fieldArray[row,col]!=0:
                testPixelData.append(pixelDataArray[row,col])
                testFieldData.append(fieldArray[row,col])
    print(testPixelData[0])

    np.save(f'data/trainCropData{tile}.npy', np.asarray(trainCropData))
    np.save(f'data/trainFieldData{tile}.npy', np.asarray(trainFieldData))
    np.save(f'data/trainPixelData{tile}.npy', np.asarray(trainPixelData))
    np.save(f'data/testFieldData{tile}.npy', np.asarray(testFieldData))
    np.save(f'data/testPixelData{tile}.npy', np.asarray(testPixelData))

