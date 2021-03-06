import MNIST.DataClean as dc
import numpy as np
import keras.layers.core as core
import keras.layers.convolutional as conv
import keras.models as models
import keras.utils.np_utils as kutils

batch_size = 128 # 128
nb_epoch = 100 # 12
img_rows, img_cols = 28, 28

nb_filters_1 = 128
nb_filters_2 = 256
nb_conv = 5

trainData = dc.convertPandasDataFrameToNumpyArray(dc.loadTrainData(describe=False))
trainX = trainData[:, 1:].reshape(trainData.shape[0], 1, img_rows, img_cols)
trainX = trainX.astype(float)
trainX /= 255.0

trainY = kutils.to_categorical(trainData[:, 0])
nb_classes = trainY.shape[1]

cnn = models.Sequential()

cnn.add(conv.Convolution2D(nb_filters_1, nb_conv, nb_conv, input_shape=(1, 28, 28), activation="relu"))
cnn.add(conv.Convolution2D(nb_filters_1, nb_conv, nb_conv, activation="relu"))
cnn.add(conv.MaxPooling2D())
cnn.add(core.Dropout(0.25))

cnn.add(conv.Convolution2D(nb_filters_2, nb_conv, nb_conv, border_mode="valid", activation="relu"))
cnn.add(conv.Convolution2D(nb_filters_2, nb_conv, nb_conv, activation="relu"))
cnn.add(conv.MaxPooling2D())
cnn.add(core.Dropout(0.25))

cnn.add(core.Flatten())
cnn.add(core.Dense(1024, activation="relu"))
cnn.add(core.Dropout(0.25))
cnn.add(core.Dense(nb_classes, activation="softmax"))

cnn.summary()
cnn.compile(loss="categorical_crossentropy", optimizer="adadelta", )

cnn.fit(trainX, trainY, batch_size=batch_size, nb_epoch=nb_epoch, show_accuracy=True, verbose=1, )

testData = dc.convertPandasDataFrameToNumpyArray(dc.loadTestData())
testX = testData.reshape(testData.shape[0], 1, 28, 28)
testX = testX.astype(float)
testX /= 255.0

yPred = cnn.predict_classes(testX)

np.savetxt('mnist-large-cnn-2.csv', np.c_[range(1,len(yPred)+1),yPred], delimiter=',', header = 'ImageId,Label', comments = '', fmt='%d')
print("Save predictions to file complete")