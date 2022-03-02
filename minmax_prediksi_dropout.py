# -*- coding: utf-8 -*-
"""MinMax_Prediksi_StudentDropout.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EGugY3pgJwNKL5QSHGjuSzTjo--qN_95
"""

import numpy as np # used for handling numbers 
import pandas as pd # used for handling the dataset
from sklearn.impute import SimpleImputer # used for handling missing data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder # used for encoding categorical data
from sklearn.model_selection import train_test_split # used for splitting training and testing data
#from sklearn.preprocessing import StandardScaler # used for feature scaling

"""Load Dataset"""

dataset = pd.read_csv('datamahasiswa_proses_2.csv', delimiter=";") # to import the dataset into a variable

dataset

# Splitting the attributes into independent and dependent attributes
dataset = dataset.to_numpy() # ubah pd.Daraframe menjadi array numpy
X = dataset[:, 0:14] # Which contains the features
y = dataset[:, 14] # Which contains the target variable

"""Missing Value (Mean)"""

# handling the missing data and replace missing values with nan from numpy and replace with mean of all the other values
imputer = SimpleImputer(missing_values=np.nan, strategy='mean') 
imputer = imputer.fit(X[:, 0:])
X[:, 0:] = imputer.transform(X[:, 0:])

X

X = pd.DataFrame(data=X,  columns= ['Alamat','PendidikanIbu','PendidikanBapak','PekerjaanIbu','PekerjaanBapak',
                 'Bekerja','LamaKuliah','SKSSemester','Keuangan','JumlahSKS',
                 'DataAbsen','NilaiTesMasuk','NilaiIPS','NilaiIPK'])

X

"""Min-Max Normalization"""

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X = scaler.fit_transform(X)
print(X)

X = pd.DataFrame(data=X, columns= ['Alamat','PendidikanIbu','PendidikanBapak','PekerjaanIbu','PekerjaanBapak',
                 'Bekerja','LamaKuliah','SKSSemester','Keuangan','JumlahSKS',
                 'DataAbsen','NilaiTesMasuk','NilaiIPS','NilaiIPK'])

X

"""Information Gain"""

from sklearn.feature_selection import mutual_info_classif
threshold = 8  # the number of most relevant features #Revisi : (menggunakan rangking nilai information gain )
high_score_features = []
feature_scores = mutual_info_classif(X, y, random_state=0)
for score, f_name in sorted(zip(feature_scores, X.columns), reverse=True)[:threshold]:
        print(f_name, score)
        high_score_features.append(f_name)
X = X[high_score_features]
print(X)

X=np.array(X)
X

y = y.reshape(-1, 1)

from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder()
y = ohe.fit_transform(y).toarray()

#y = pd.DataFrame.from_records(y)

y

"""Split Data Training 80%"""

from sklearn.model_selection import train_test_split
# train_ratio = 0.70
# validation_ratio = 0.10
# test_ratio = 0.20
train_ratio = 0.70
validation_ratio = 0.20
test_ratio = 0.10

# train is now 70% of the entire data set
# the _junk suffix means that we drop that variable completely
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 - train_ratio)

# test is now 10% of the initial data set
# validation is now 20% of the initial data set
X_val, X_train, y_val, y_train = train_test_split(X_train, y_train, test_size=test_ratio/(test_ratio + validation_ratio)) 

print(X_train, X_val, X_test)

X_test.shape

"""**Neural Network**

**ALTERNATIF** **SEMENTARA**
"""

from tensorflow import keras
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import Sequential
import tensorflow as tf

nn = Sequential()
nn.add(Dense(50, input_dim=8, activation='sigmoid'))
nn.add(Dense(70, activation='sigmoid'))
nn.add(Dense(3, activation='softmax'))
nn.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#nn.compile(loss=tf.nn.nce_loss, optimizer='adam', metrics=['accuracy'])

print(nn.summary())

history = nn.fit(X_train, y_train, epochs=300, batch_size=20, validation_data=(X_val, y_val))

import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

plt.plot(history.history['loss']) 
plt.plot(history.history['val_loss']) 
plt.title('Model loss') 
plt.ylabel('Loss') 
plt.xlabel('Epoch') 
plt.legend(['Train', 'Test'], loc='upper left') 
plt.show()

"""**Evaluate**"""

# evaluate the model
# scores = nn.evaluate(X, y, verbose=0)
# print("%s: %.2f%%" % (nn.metrics_names[1], scores[1]*100))

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

"""**F1-Score**"""

# predict probabilities for test set
#y_pred = nn.predict(X_val)
y_test_arg=np.argmax(y_test,axis=1)
Y_pred = np.argmax(nn.predict(X_test),axis=1)

print("F1-Score : %.2f" % f1_score(y_test_arg, Y_pred, average="micro"))
print("Precision : %.2f" % precision_score(y_test_arg, Y_pred, average="micro"))

print('Confusion Matrix')
print(confusion_matrix(y_test_arg, Y_pred))
print(classification_report(y_test_arg, Y_pred))

#ditambah F-Score

"""**SIMPAN MODEL**"""

!pip install tensorflowjs

import tensorflowjs as tfjs

tfjs.converters.save_keras_model(nn, 'models')

# y_pred = nn.predict(X_test) #sklearn.metric f-one score / confusion  matrix 
# #w = nn.evaluate(X_test, y_test,verbose=1)
# y_pred = pd.DataFrame.from_records(y_pred)
# y_pred

#data_test = pd.read_csv('datamahasiswa_campur2-angka-test2.csv', delimiter=";") # to import the dataset into a variable

#data_test

# data_test = data_test.to_numpy()
# X_input = data_test[:, 0:8] # Which contains the features
#y_pred = dataset[:, 8] # Which contains the target variable

#X_input

# X_input = pd.DataFrame(data=X_input,  columns= ['NilaiIPK','NilaiIPS','JumlahSK','Keuangan',
#                                                 'NilaiTesMasuk','SemesterBerjalan','Bekerja','DataAbsen'])

# X_input

# X_input = z_score(X_input)

# X_input

#data_test=np.array(data_test, dtype=np.float)
# y_predt = nn.predict(np.array(X_input))
# y_predt = pd.DataFrame.from_records(y_predt)

# y_predt