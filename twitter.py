# -*- coding: utf-8 -*-
"""Twitter.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bULs3A_7z4eQppnPk-bED-lgL6CMi2qo
"""

! pip install kaggle

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d kazanova/sentiment140

from zipfile import ZipFile
dataset = '/content/sentiment140.zip'

with ZipFile(dataset,'r') as zip:
  zip.extractall()
  print('Dataset is extracted')

import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import nltk
nltk.download ('stopwords')

print(stopwords.words('english'))

twitter_data = pd.read_csv('/content/training.1600000.processed.noemoticon.csv',encoding='ISO-8859-1')

twitter_data.shape

twitter_data.head(5)

column_names = ['target','ids','date','flag','user','text']
twitter_data = pd.read_csv('/content/training.1600000.processed.noemoticon.csv',encoding='ISO-8859-1',names=column_names)

twitter_data.shape

twitter_data.isnull().sum()

twitter_data['target'].value_counts()

twitter_data.replace({'target':{4:1}},inplace=True)

port_stem = PorterStemmer()
stopword =set(stopwords.words('english'))

def stemming(content):
  stemmed_content = re.sub('[^a-zA-Z]',' ',content)
  stemmed_content = stemmed_content.lower()
  stemmed_content = stemmed_content.split()
  stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopword]
  stemmed_content = ' '.join(stemmed_content)
  return stemmed_content

twitter_data['stemmed_text'] = twitter_data['text'].apply(stemming)

twitter_data.head(5)

X = twitter_data['stemmed_text'].values
Y = twitter_data['target'].values

print(X)

print(Y)

X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=2)

print(X.shape,X_train.shape,X_test.shape)

vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

print(X_train)

print(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train,Y_train)

X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(Y_train,X_train_prediction)

print("Training Accuracy= ",training_data_accuracy)

X_test_prediction = model.predict(X_test)
testing_data_accuracy = accuracy_score(Y_test,X_test_prediction)

print("Testing Accuracy= ",testing_data_accuracy)

import pickle

filename = 'trained_model.sav'
pickle.dump(model,open(filename,'wb'))

loaded_model = pickle.load(open('/content/trained_model.sav','rb'))

X_new = X_test[220]

print(Y_test[220])
prediction = loaded_model.predict(X_new)
print(prediction)

if(prediction[0]==0):
  print("Negative")
else:
  print("Positive")

X_new = stemming("i am very sad with this")
arr=[]
arr.append(X_new)
X_new = vectorizer.transform(arr)
prediction = loaded_model.predict(X_new)
print(prediction)

if(prediction[0]==0):
  print("Negative")
else:
  print("Positive")