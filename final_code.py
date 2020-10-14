# -*- coding: utf-8 -*-
"""final code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1E8hgR2Tg1K0neLmDKKmkZBLP7ORijgS_
"""

Link to download the dataset - https://datahack.analyticsvidhya.com/contest/practice-problem-loan-prediction-iii/#ProblemStatement

"""# **Importing the libraries**"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""# **Importing the dataset**"""

dataset_train = pd.read_csv('./drive/My Drive/Analytics Vidhya Challenges/Loan Prediction/train.csv')
dataset_test = pd.read_csv('./drive/My Drive/Analytics Vidhya Challenges/Loan Prediction/test.csv')

"""Study the datasets"""

dataset_train.info()

dataset_test.info()

dataset_train.dtypes

dataset_test.dtypes

"""# **Data Preprocessing - 1**

Taking care of duplicate values
"""

dataset_train.duplicated().sum()

dataset_test.duplicated().sum()

"""Taking care of null/missing values"""

dataset_train.isnull().sum()

dataset_train['Gender'] = dataset_train['Gender'].fillna(dataset_train['Gender'].mode()[0])

dataset_train['Married'] = dataset_train['Married'].fillna(dataset_train['Married'].mode()[0])

dataset_train['Dependents'] = dataset_train['Dependents'].fillna(dataset_train['Dependents'].mode()[0])

dataset_train['LoanAmount'] = dataset_train['LoanAmount'].fillna(dataset_train['LoanAmount'].median())
dataset_train['Loan_Amount_Term'] = dataset_train['Loan_Amount_Term'].fillna(dataset_train['Loan_Amount_Term'].mode()[0])

dataset_train['Self_Employed'] = dataset_train['Self_Employed'].fillna(dataset_train['Self_Employed'].mode()[0])
dataset_train['Credit_History'] = dataset_train['Credit_History'].fillna(dataset_train['Credit_History'].mode()[0])

dataset_test.isnull().sum()

dataset_test['Gender'] = dataset_test['Gender'].fillna(dataset_test['Gender'].mode()[0])
dataset_test['Dependents'] = dataset_test['Dependents'].fillna(dataset_test['Dependents'].mode()[0])
dataset_test['Self_Employed'] = dataset_test['Self_Employed'].fillna(dataset_test['Self_Employed'].mode()[0])
dataset_test['LoanAmount'] = dataset_test['LoanAmount'].fillna(dataset_test['LoanAmount'].median())
dataset_test['Loan_Amount_Term'] = dataset_test['Loan_Amount_Term'].fillna(dataset_test['Loan_Amount_Term'].mode()[0])
dataset_test['Credit_History'] = dataset_test['Credit_History'].fillna(dataset_test['Credit_History'].mode()[0])

dataset_train['TotalIncome'] = dataset_train['ApplicantIncome'] + dataset_train['CoapplicantIncome']

"""# **Exploratory Data Analysis**"""

import seaborn as sns

sns.distplot(dataset_train['TotalIncome'])

dataset_train['TotalIncome_log'] = np.log(dataset_train['TotalIncome'])

sns.distplot(dataset_train['TotalIncome_log'])

sns.distplot(dataset_train['LoanAmount'])

dataset_train['LoanAmount_log'] = np.log(dataset_train['LoanAmount'])

sns.distplot(dataset_train['LoanAmount_log'])

sns.displot(dataset_train['Loan_Amount_Term'])

dataset_train.drop(['ApplicantIncome', 'CoapplicantIncome','TotalIncome', 'LoanAmount'], axis=1, inplace=True)

dataset_test['TotalIncome'] = dataset_test['ApplicantIncome'] + dataset_test['CoapplicantIncome']
dataset_test['TotalIncome_log'] = np.log(dataset_test['TotalIncome'])
dataset_test['LoanAmount_log'] = np.log(dataset_test['LoanAmount'])
dataset_test.drop(['ApplicantIncome', 'CoapplicantIncome','TotalIncome', 'LoanAmount'], axis=1, inplace=True)

"""# **Data Preprocessing - 2**"""

dataset_train.head(5)

"""Encoding the Categorical Data"""

x = dataset_train.iloc[:, [1,2,3,4,5,6,7,8,10,11]].values
y = dataset_train.iloc[:, 9].values

print(x[0])

"""1. OneHotEncoder"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers = [('encoder', OneHotEncoder(), [2, 7])], remainder='passthrough')
x = np.array(ct.fit_transform(x))

print(x[0])

"""2. LabelEncoder"""

from sklearn.preprocessing import LabelEncoder
le_gender, le_married, le_education, le_self_employed, le_y = LabelEncoder(), LabelEncoder(), LabelEncoder(), LabelEncoder(), LabelEncoder()
x[:, 7] = le_gender.fit_transform(x[:, 7])
x[:, 8] = le_married.fit_transform(x[:, 8])
x[:, 9] = le_education.fit_transform(x[:, 9])
x[:, 10] = le_self_employed.fit_transform(x[:, 10])

y = le_y.fit_transform(y)

print(x[0])

x = np.asarray(x).astype(np.float32)

"""Splitting the dataset into Training set and Test set"""

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

"""Feature Scaling"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train[:, [11,13,14]] = sc.fit_transform(x_train[:, [11,13,14]])
x_test[:, [11,13,14]] = sc.transform(x_test[:, [11,13,14]])

print(x_train[0])

print(y_train)

"""# **Model Training**"""

from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
def print_score(y_test, y_pred):
  print('Accuracy Score : '+str(round(accuracy_score(y_test, y_pred)*100,2))+' %')
  print('F1 Score : '+str(round(f1_score(y_test, y_pred)*100,2))+' %')
  print('Confusion Matrix : ',confusion_matrix(y_test,y_pred))

from sklearn.linear_model import LogisticRegression
lr_classifier = LogisticRegression()
lr_classifier.fit(x_train, y_train)

y_pred_lr = lr_classifier.predict(x_test)
y_proba_lr = lr_classifier.predict_proba(x_test)
print_score(y_test, y_pred_lr)
print(y_proba_lr)

"""# **Predicting the Test Set**

Training using Logistic Regression on whole dataset
"""

x_whole = x
y_whole = y

from sklearn.preprocessing import StandardScaler
sc_whole = StandardScaler()
x_whole[:, [11,13,14]] = sc_whole.fit_transform(x_whole[:, [11,13,14]])

final_model = LogisticRegression()
final_model.fit(x_whole, y_whole)

"""Processing the Test data for predictions"""

dataset_test.head(5)

test_data = dataset_test.iloc[:, 1:].values

print(test_data)

test_data = np.array(ct.transform(test_data))

test_data[:, 7] = le_gender.fit_transform(test_data[:, 7])
test_data[:, 8] = le_married.fit_transform(test_data[:, 8])
test_data[:, 9] = le_education.fit_transform(test_data[:, 9])
test_data[:, 10] = le_self_employed.fit_transform(test_data[:, 10])

print(test_data[0])

print(x_whole[0])

test_data[:, [11,13,14]] = sc_whole.transform(test_data[:, [11,13,14]])

test_data = np.asarray(test_data).astype(np.float32)

"""Predicting the results of Test.csv"""

pred_data = final_model.predict(test_data)

pred_data = le_y.inverse_transform(pred_data)

"""Exporting the .csv file"""

data = {"Loan_ID":dataset_test.iloc[:, 0].values, "Loan_Status":pred_data}
pd.DataFrame(data).to_csv('./drive/My Drive/Analytics Vidhya Challenges/Loan Prediction/predictions.csv', index=False)