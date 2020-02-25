import numpy
from keras.models import Sequential
from keras.layers import LSTM, TimeDistributed, Dense, Bidirectional, Masking

# import the test and train numpy arrays

# calculate number of pixels in train and test datasets
noTrainPixels = 10
noTestPixels = 2
noDates = 13
noBands = 13

# define the model
model = Sequential()

# Add masking layer if timesteps are to have varying length. Not needed atm.
# model.add(Masking(mask_value=0., input_shape=(noDates, noBands)))

# add an initial hidden LSTM layer which has 20 memory units, and takes an input with each
# date as a time step and each timestep storing a data point for each band.
# The memory units parameter is the dimensional size of the output per time step. It has very
# similar effects to the number of neurons in a feed-forward layer and has to be tuned to
# avoid overfitting while still ensuring enough information is stored to learn effectively.
# keep return_sequence set to the default of false as are only concerned about the
# output of the final sequence.
model.add(LSTM(20, input_shape=(noDates, noBands)))

# Output layer is a fully connected dense layer that outputs seven outputs batch (one
# probability per crop type).
# It uses the sigmoid activation function.
# The TimeDistributes wrapper is not required as we do not need the model to be applied
# to every timestep, only the final result.
model.add(Dense(7, activation = 'sigmoid'))

# compile the model with binary crossentropy cost function (because the output is either
# 1 or 0) the standard keras optimiser (backprop algorithm) of adam and return accuracy
# after each epoch.
model.compile(optimizer='adam', loss='binary_crossentropy', metrics = ['acc'])

# Train over 20 epochs with a mini-batch size of 50: an epoch consists of randomly taking
# 50 of the train inputs and runs each through backprop algorithm.
# verbose param sets how information regarding epoch progression is presented in
# the console.
model.fit(X,y, epochs=20, batch_size=50, verbose=2)