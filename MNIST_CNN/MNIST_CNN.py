import os
os.environ['KERAS_BACKEND'] = 'theano'
from keras import backend as K
K.set_image_dim_ordering('th')


import keras

import numpy as np
np.random.seed(123)  # for reproducibility

# Import Keras model
from keras.models import Sequential, load_model
# Import Keras core layers
from keras.layers import Dense, Dropout, Activation, Flatten
# Import Keras CNN layers
from keras.layers import Conv2D, MaxPooling2D
# Import Keras utils
from keras.utils import np_utils

#####################################################################

# Import Dataset
from keras.datasets import mnist


class MNIST_CNN:

    def __init__(self):
        # Load Data
        print('Date preprocessing . . .')
        (self.X_train, self.y_train), (self.X_test, self.y_test) = mnist.load_data()

        # Reshape data
        self.X_train = self.X_train.reshape(self.X_train.shape[0], 1, 28, 28)
        self.X_test = self.X_test.reshape(self.X_test.shape[0], 1, 28, 28)

        # Convert data type as float32
        self.X_train = self.X_train.astype('float32')
        self.X_test = self.X_test.astype('float32')

        # Normalization (Data in range [0,1])
        self.X_train /= 255
        self.X_test /= 255

        # Convert data to 10-dimensional matrice
        self.Y_train = np_utils.to_categorical(self.y_train, 10)
        self.Y_test = np_utils.to_categorical(self.y_test, 10)


    def fitModel(self):
        ## Setup the sequential model
        self.model = Sequential()

        # Declare input layer
        self.model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=(1,28,28)))
        self.model.add(Conv2D(64, (3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))
        self.model.add(Flatten())
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(10, activation='softmax'))

        # Compile model
        print("Model compilation . . .")
        self.model.compile(loss=keras.losses.categorical_crossentropy,optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])

        # Fit model
        print('Model fitting . . .')
        self.model.fit(self.X_train, self.Y_train, batch_size=128, epochs=12, verbose=1, validation_data=(self.X_test, self.Y_test))

        # Save fitted model
        self.model.save('MNIST_CNN.h5')

    def loadModel(self, model_file):
        # Load model and weights from file
        print('Load model from file: {}'.format(model_file))
        self.model = load_model(model_file)

    def evaluate(self):
        # Evaluate the model accuracy with a test set
        print('Evaluate test set images')
        score = self.model.evaluate(self.X_test, self.Y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])


# MNIST CNN CLASS TESTS
if __name__ == "__main__":
    print("Test MNIST CNN CLASS")
    cnn = MNIST_CNN()
    cnn.loadModel('MNIST_CNN.h5')
    cnn.evaluate()
