# ===========================
# IMPORT LIBRARIES
# ===========================
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

# ===========================
# LOAD DATA
# ===========================
df = pd.read_csv("Loan dataset_classification.csv")

# ===========================
# DROP USELESS COLUMN
# ===========================
df.drop("Loan_ID", axis=1, inplace=True)

# ===========================
# HANDLE MISSING VALUES
# ===========================
cat_cols = ["Gender","Married","Dependents","Education","Self_Employed","Property_Area","Loan_Status"]
num_cols = ["ApplicantIncome","CoapplicantIncome","LoanAmount","Loan_Amount_Term","Credit_History"]

for col in cat_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

for col in num_cols:
    df[col].fillna(df[col].median(), inplace=True)

# ===========================
# CLEAN TARGET COLUMN
# ===========================
df["Loan_Status"] = df["Loan_Status"].str.strip()
df["Loan_Status"] = df["Loan_Status"].map({"Y":1, "N":0})
df.dropna(subset=["Loan_Status"], inplace=True)
df.reset_index(drop=True, inplace=True)

# ===========================
# DATA TYPE FIX
# ===========================
df["Dependents"] = df["Dependents"].replace("3+", 3).astype(int)

# ===========================
# ENCODING
# ===========================
df["Gender"] = df["Gender"].map({"Male":1, "Female":0})
df["Married"] = df["Married"].map({"Yes":1, "No":0})
df["Education"] = df["Education"].map({"Graduate":1, "Not Graduate":0})
df["Self_Employed"] = df["Self_Employed"].map({"Yes":1, "No":0})

df = pd.get_dummies(df, columns=["Property_Area"], drop_first=True)

# ===========================
# FINAL CHECK
# ===========================
print("NULL VALUES CHECK:\n", df.isnull().sum())

# ===========================
# FEATURE & TARGET
# ===========================
X = df.drop("Loan_Status", axis=1)
y = df["Loan_Status"]

# ===========================
# TRAIN TEST SPLIT
# ===========================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# ===========================
# LOGISTIC REGRESSION MODEL
# ===========================
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)

y_pred_lr = lr.predict(X_test)

# ===========================
# RANDOM FOREST MODEL
# ===========================
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train, y_train)

y_pred_rf = rf.predict(X_test)

# ===========================
# RESULTS
# ===========================
print("\nLOGISTIC REGRESSION")
print("Accuracy:", accuracy_score(y_test, y_pred_lr))
print(confusion_matrix(y_test, y_pred_lr))
print(classification_report(y_test, y_pred_lr))

print("\nRANDOM FOREST")
print("Accuracy:", accuracy_score(y_test, y_pred_rf))
print(confusion_matrix(y_test, y_pred_rf))
print(classification_report(y_test, y_pred_rf))

# ===========================
# CONFUSION MATRIX PLOT
# ===========================
sns.heatmap(confusion_matrix(y_test, y_pred_lr), annot=True)
plt.title("Confusion Matrix - Logistic Regression")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()