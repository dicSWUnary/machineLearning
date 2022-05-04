# -*- coding: utf-8 -*-
"""dicSWUnary_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13C9jvLl-QWPXngf2jrskzNYARu0jWuVI
"""

ls

from google.colab import drive
drive.mount('/content/gdrive')

import os, re, glob
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from PIL import Image


groups_folder_path = "/content/gdrive/MyDrive/image set"
categories = ["front_logo", "gs25", "gusia", "insa_kiosk", "job", "lib_kiosk", "lib_science", "post_office"]
nb_classes = len(categories)

image_w = 64
image_h = 64

pixels = image_h * image_w * 3



X = []
y = []

for idx, category in enumerate(categories):
    
    #one-hot 돌리기.
    label = [0 for i in range(nb_classes)]
    label[idx] = 1

    image_dir = groups_folder_path + "/" + category
    files = glob.glob(image_dir+"/*.jpeg")
    print(category, " 파일 길이 : ", len(files))
    for i, f in enumerate(files):
        img = Image.open(f)
        img = img.convert("RGB")
        img = img.resize((image_w, image_h))
        data = np.asarray(img)

        X.append(data)
        y.append(label)

        if i % 27 == 0:
            print(category, " : ", f)



import numpy as np
X = np.array(X)
print("x done")
y = np.array(y)
#1 0 0 0 이면 airplanes
#0 1 0 0 이면 buddha 이런식

X_train, X_test, y_train, y_test = train_test_split(X, y)
xy = (X_train, X_test, y_train, y_test)
np.save("./img_data.npy", xy)

print("ok", len(y))

import os, glob, numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
#import keras.backend.tensorflow_backend as K

import tensorflow as tf
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
#session = tf.Session(config=config)

X_train, X_test, y_train, y_test = np.load('./img_data.npy',allow_pickle=True)
print(X_train.shape)
print(X_train.shape[0])

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dropout, Activation, Dense
from keras.layers import Flatten, Convolution2D, MaxPooling2D
from keras.models import load_model
import cv2
from tensorflow.keras.optimizers import Adam
#from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator

X_train, X_test, y_train, y_test = np.load('./img_data.npy',allow_pickle=True)

model = Sequential()
model.add(Conv2D(32, (3,3), padding="same", input_shape=X_train.shape[1:], activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3,3), padding="same", activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(8, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model_dir = './model'

if not os.path.exists(model_dir):
    os.mkdir(model_dir)

model_path = model_dir + '/multi_img_classification.model'
checkpoint = ModelCheckpoint(filepath=model_path , monitor='val_loss', verbose=1, save_best_only=True)
early_stopping = EarlyStopping(monitor='val_loss', patience=6)

model.summary()

history = model.fit(X_train, y_train, batch_size=32, epochs=30, validation_data=(X_test, y_test), callbacks=[checkpoint, early_stopping])

model.save('dicswunary.h5')

print("정확도 : %.4f" % (model.evaluate(X_test, y_test)[1]))

from PIL import Image
import os, glob, numpy as np
from keras.models import load_model

caltech_dir = "./guide/"
image_w = 64
image_h = 64

pixels = image_h * image_w * 3

X = []
filenames = []
files = glob.glob(caltech_dir+"/*.*")
for i, f in enumerate(files):
    img = Image.open(f)
    img = img.convert("RGB")
    img = img.resize((image_w, image_h))
    data = np.asarray(img)
    filenames.append(f)
    X.append(data)

X = np.array(X)
model = load_model('./model/multi_img_classification.model')

prediction = model.predict(X)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
cnt = 0

#이 비교는 그냥 파일들이 있으면 해당 파일과 비교. 카테고리와 함께 비교해서 진행하는 것은 _4 파일.
for i in prediction:
    pre_ans = i.argmax()  # 예측 레이블
    print(i)
    # print(pre_ans)
    pre_ans_str = ''
    category = ["front_logo", "gs25", "gusia", "insa_kiosk", "job", "lib_kiosk", "lib_science", "post_office"]
    if pre_ans == 0: pre_ans_str = category[0]
    elif pre_ans == 1: pre_ans_str = category[1]
    elif pre_ans == 2: pre_ans_str = category[2]
    elif pre_ans == 3: pre_ans_str = category[3]
    elif pre_ans == 4: pre_ans_str = category[4]
    elif pre_ans == 5: pre_ans_str = category[5]
    elif pre_ans == 6: pre_ans_str = category[6]
    else : pre_ans_str = category[7]

    
    if i[0] >= 0.8: print("해당 "+filenames[cnt]+"이미지는 "+pre_ans_str+"로 추정됩니다.")
    if i[1] >= 0.8: print("해당 "+filenames[cnt]+"이미지는 "+pre_ans_str+"으로 추정됩니다.")
    if i[2] >= 0.8: print("해당 "+filenames[cnt]+"이미지는 "+pre_ans_str+"로 추정됩니다.")
    if i[3] >= 0.8: print("해당 "+filenames[cnt]+"이미지는 "+pre_ans_str+"로 추정됩니다.")
    if i[4] >= 0.8: print("해당 "+filenames[cnt]+"이미지는 "+pre_ans_str+"로 추정됩니다.")
    if i[5] >= 0.7: print("해당 "+filenames[cnt]+"이미지는 "+pre_ans_str+"로 추정됩니다.")
    if i[6] >= 0.8: print("해당 "+filenames[cnt]+"이미지는 "+pre_ans_str+"로 추정됩니다.")
    if i[7] >= 0.7: print("해당 "+filenames[cnt]+"이미지는 "+pre_ans_str+"로 추정됩니다.")
    
    cnt += 1

i

prediction



pip install coremltools

import coremltools
coreml_model = coremltools.converters.convert('./dicswunary.h5')
coreml_model.save('./dicswunary.mlmodel')