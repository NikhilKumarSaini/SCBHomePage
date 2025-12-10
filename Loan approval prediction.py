# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import warnings
warnings.filterwarnings("ignore")

# Load dataset
df = pd.read_csv("Loan dataset_classification.csv")

# Drop Loan_ID column
df.drop("Loan_ID", axis=1, inplace=True)

# Handle missing values (Categorical)
cat_cols = ["Gender","Married","Dependents","Education","Self_Employed","Property_Area"]
for col in cat_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

# Handle missing values (Numerical)
num_cols = ["LoanAmount","Loan_Amount_Term","Credit_History","CoapplicantIncome"]
for col in num_cols:
    df[col].fillna(df[col].median(), inplace=True)

# Convert Dependents
df["Dependents"] = df["Dependents"].replace("3+", 3).astype(int)

# Encode categorical columns
df["Gender"] = df["Gender"].map({"Male":1 , "Female":0})
df["Married"] = df["Married"].map({"Yes":1 , "No":0})
df["Education"] = df["Education"].map({"Graduate":1 , "Not Graduate":0})
df["Self_Employed"] = df["Self_Employed"].map({"Yes":1 , "No":0})
df["Loan_Status"] = df["Loan_Status"].map({"Y":1 , "N":0})

# One-hot encoding for Property_Area
df = pd.get_dummies(df, columns=["Property_Area"], drop_first=True)

# Feature & Target split
X = df.drop("Loan_Status", axis=1)
y = df["Loan_Status"]

# Train-Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Logistic Regression Model
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)

# Predictions
y_pred_lr = lr.predict(X_test)

# Evaluation for Logistic Regression
print("LOGISTIC REGRESSION RESULTS")
print("===========================")
print("Accuracy:", accuracy_score(y_test, y_pred_lr))
print(confusion_matrix(y_test, y_pred_lr))
print(classification_report(y_test, y_pred_lr))

# Random Forest Model
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train, y_train)

# Predictions
y_pred_rf = rf.predict(X_test)

# Evaluation for Random Forest
print("\nRANDOM FOREST RESULTS")
print("=====================")
print("Accuracy:", accuracy_score(y_test, y_pred_rf))
print(confusion_matrix(y_test, y_pred_rf))
print(classification_report(y_test, y_pred_rf))

# Confusion Matrix Plot (Logistic Regression)
sns.heatmap(confusion_matrix(y_test, y_pred_lr), annot=True)
plt.title("Confusion Matrix - Logistic Regression")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()