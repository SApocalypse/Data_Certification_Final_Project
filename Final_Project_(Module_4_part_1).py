import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report
import io
import requests
import numpy as np

# URLs for datasets
URL1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
URL2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv'

# Load data from URLs
def load_data(url):
    response = requests.get(url)
    data = pd.read_csv(io.BytesIO(response.content))
    return data

# Load dataset_part_2.csv into 'data'
data = load_data(URL1)

# Load dataset_part_3.csv into 'X'
X = load_data(URL2)

# Standardize the data in X
scaler = StandardScaler()
X_standardized = scaler.fit_transform(X)
X = pd.DataFrame(X_standardized, columns=X.columns)

# Create Y as a Pandas Series from 'Class' column in 'data'
Y = data['Class'].to_numpy()

# Split data into training and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

# Print descriptive statistics for training dataset
print("Descriptive statistics for training dataset:")
print(X_train.describe())

# Print descriptive statistics for testing dataset
print("\nDescriptive statistics for testing dataset:")
print(X_test.describe())

# Define the Logistic Regression model with appropriate parameters
logreg = LogisticRegression(max_iter=10000)

# Define the SVM model with appropriate parameters
svm = SVC()

# Define the Decision Tree Classifier model with appropriate parameters
tree = DecisionTreeClassifier()

# Define the K Nearest Neighbors (KNN) model with appropriate parameters
knn = KNeighborsClassifier()

# Define the parameter grids for GridSearchCV
parameters_logreg = {
    'C': np.logspace(-3, 3, 7),
    'penalty': ['l1', 'l2']
}

parameters_svm = {
    'kernel': ['linear', 'rbf', 'poly', 'sigmoid'],
    'C': np.logspace(-3, 3, 7),
    'gamma': np.logspace(-3, 3, 7)
}

parameters_tree = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [None, 10, 20, 30, 40, 50],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

parameters_knn = {
    'n_neighbors': [3, 5, 7, 9],
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan']
}

# Create GridSearchCV objects with 10-fold cross-validation
logreg_cv = GridSearchCV(logreg, parameters_logreg, cv=10)
svm_cv = GridSearchCV(svm, parameters_svm, cv=10)
tree_cv = GridSearchCV(tree, parameters_tree, cv=10)
knn_cv = GridSearchCV(knn, parameters_knn, cv=10)

# Fit the GridSearchCV objects to find the best parameters
logreg_cv.fit(X_train, Y_train)
svm_cv.fit(X_train, Y_train)
tree_cv.fit(X_train, Y_train)
knn_cv.fit(X_train, Y_train)

# Print the best parameters found by GridSearchCV for each model
print("\nBest parameters found by GridSearchCV for Logistic Regression:")
print(logreg_cv.best_params_)
print("\nBest parameters found by GridSearchCV for SVM:")
print(svm_cv.best_params_)
print("\nBest parameters found by GridSearchCV for Decision Tree:")
print(tree_cv.best_params_)
print("\nBest parameters found by GridSearchCV for KNN:")
print(knn_cv.best_params_)

# Get the best estimators
best_logreg = logreg_cv.best_estimator_
best_svm = svm_cv.best_estimator_
best_tree = tree_cv.best_estimator_
best_knn = knn_cv.best_estimator_

# Predict on the test set for each model
Y_pred_logreg = best_logreg.predict(X_test)
Y_pred_svm = best_svm.predict(X_test)
Y_pred_tree = best_tree.predict(X_test)
Y_pred_knn = best_knn.predict(X_test)

# Print classification report and confusion matrix for each model
print("\nClassification Report for Logistic Regression:")
print(classification_report(Y_test, Y_pred_logreg))
print("\nClassification Report for SVM:")
print(classification_report(Y_test, Y_pred_svm))
print("\nClassification Report for Decision Tree:")
print(classification_report(Y_test, Y_pred_tree))
print("\nClassification Report for KNN:")
print(classification_report(Y_test, Y_pred_knn))

# Calculate accuracy on the test data for each model
accuracy_logreg = best_logreg.score(X_test, Y_test)
accuracy_svm = best_svm.score(X_test, Y_test)
accuracy_tree = best_tree.score(X_test, Y_test)
accuracy_knn = best_knn.score(X_test, Y_test)

print(f"\nAccuracy on test data for Logistic Regression: {accuracy_logreg:.4f}")
print(f"Accuracy on test data for SVM: {accuracy_svm:.4f}")
print(f"Accuracy on test data for Decision Tree: {accuracy_tree:.4f}")
print(f"Accuracy on test data for KNN: {accuracy_knn:.4f}")

# Plot confusion matrices for each model
def plot_confusion_matrix(y_true, y_pred, title):
    cm = confusion_matrix(y_true, y_pred)
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, ax=ax, fmt='d', cmap='Blues')
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title(title)
    ax.xaxis.set_ticklabels(['did not land', 'land'])
    ax.yaxis.set_ticklabels(['did not land', 'land'])
    plt.show()

# Plot confusion matrices for each model
plot_confusion_matrix(Y_test, Y_pred_logreg, "Confusion Matrix for Logistic Regression")
plot_confusion_matrix(Y_test, Y_pred_svm, "Confusion Matrix for SVM")
plot_confusion_matrix(Y_test, Y_pred_tree, "Confusion Matrix for Decision Tree")
plot_confusion_matrix(Y_test, Y_pred_knn, "Confusion Matrix for KNN")

