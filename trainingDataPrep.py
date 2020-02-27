import numpy as np

'''concatonates data of individual pixels from all tiles into training and testing data'''


'''create array of pixel data for training/testing, which is a list of pixel data points: ie. a list of corresponding to
each date, containing a list of values for each band'''
trainPixelData = []
testPixelData = []

'''create array of crop data, which is a list where each element is a list representing the probability of a pixel being
each of the crop types. In training we know the crop type, so for each pixel this is a list of 0s and 1 at the index of
the actual crop type of that pixel'''
trainCropData = []
noCropTypes = 7

'''also hold field data for future model, which is just the field number for each pixel'''
trainFieldData = []
testFieldData = []

# get data from each tile
for tile in range(0,4):
    fieldArray = np.load(f'data/fieldArray{tile}.npy', allow_pickle=True)
    cropArray = np.load(f'data/cropArray{tile}.npy', allow_pickle=True)
    pixelDataArray = np.load(f'data/pixelDataArray{tile}.npy', allow_pickle=True)


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


np.save(f'data/master/trainCropData.npy', np.asarray(trainCropData))
np.save(f'data/master/trainFieldData.npy', np.asarray(trainFieldData))
np.save(f'data/master/trainPixelData.npy', np.asarray(trainPixelData))
np.save(f'data/master/testFieldData.npy', np.asarray(testFieldData))
np.save(f'data/master/testPixelData.npy', np.asarray(testPixelData))

