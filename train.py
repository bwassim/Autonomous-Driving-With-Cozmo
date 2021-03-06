import os

os.environ['KERAS_BACKEND'] = 'theano'
os.environ['THEANO_FLAGS']='mode=FAST_RUN,device=cuda0,floatX=float32,optimizer=None'

import keras.models as models
from keras.models import Sequential, Model
from keras.optimizers import SGD, Adam, RMSprop
from keras.callbacks import ModelCheckpoint

import autodrive_constants
import numpy as np
import glob

import matplotlib.pyplot as plt

imgSize = autodrive_constants.IMG_SIZE
imgs = np.zeros((0, imgSize[0], imgSize[1], imgSize[2]), dtype=np.float16)
targets = np.zeros(0, dtype=np.float32)
imgs_val = np.zeros((0, imgSize[0], imgSize[1], imgSize[2]), dtype=np.float16)
targets_val = np.zeros(0, dtype=np.float32)

# Load training data
imgfiles = sorted(glob.glob('data_train_01/*-images.npz'))
steerfiles = sorted(glob.glob('data_train_01/*-steer.npz'))
for imgfile, steerfile in zip(imgfiles, steerfiles):
    imgs = np.append(imgs, np.load(imgfile)['img_arr'], axis=0)
    targets = np.append(targets, np.load(steerfile)['steer_arr'], axis=0)

# Augment the training data by flipping each image left to right
# and reversing the steering inputs
imgs_aug = np.zeros(imgs.shape, dtype=np.float16)
targets_aug = np.zeros(targets.shape, dtype=np.float32)
for i in range(0, imgs.shape[0]):
    imgs_aug[i,:] = np.fliplr(imgs[i,:])
    targets_aug[i] = -targets[i]

imgs = np.append(imgs, imgs_aug, axis=0)
targets = np.append(targets, targets_aug, axis=0)

imgs_aug = None
target_aug = None

print(f'Have {imgs.shape[0]} training images')

# Load validation data
imgfiles = sorted(glob.glob('data_val_01/*-images.npz'))
steerfiles = sorted(glob.glob('data_val_01/*-steer.npz'))
for imgfile, steerfile in zip(imgfiles, steerfiles):
    imgs_val = np.append(imgs_val, np.load(imgfile)['img_arr'], axis=0)
    targets_val = np.append(targets_val, np.load(steerfile)['steer_arr'], axis=0)

print(f'Have {imgs_val.shape[0]} validation images')

#idx = 2000
#imgplot = plt.imshow(imgs[idx,:].astype(np.float32))
#print(f'steer: {targets[idx]}')
#plt.show()

# Shuffle images and steering targets
idx = np.arange(0,imgs.shape[0])
idx = np.random.permutation(idx)
imgs = imgs[idx,:,:,:]
targets = targets[idx]

# load the model:
model = Sequential()
with open('autopilot_basic_model.json') as model_file:
    model = models.model_from_json(model_file.read())

adam = Adam(lr=0.0001)
model.compile(loss='mse',
              optimizer=adam,
              metrics=['mse'])

epochs = 25
batch_size = 64

model.fit(imgs, targets, 
	batch_size=batch_size, epochs=epochs, verbose=1,
	validation_data=(imgs_val, targets_val), shuffle=True)

model.save_weights('weights/model_basic_weight.hdf5')

