import matplotlib.pyplot as plt
from sklearn.metrics import plot_precision_recall_curve, plot_roc_curve, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV, train_test_split

# Assuming your data is already loaded and preprocessed into X_train, X_test, y_train, y_test

# Example models initialized
log_reg = LogisticRegression(max_iter=10000)
svm = SVC(probability=True)
dt = DecisionTreeClassifier()
knn = KNeighborsClassifier()

# Example GridSearchCV for hyperparameter tuning
param_grid_lr = {'C': [0.01, 0.1, 1], 'penalty': ['l2']}
param_grid_svm = {'C': [0.01, 0.1, 1], 'gamma': [0.001, 0.01], 'kernel': ['linear']}
param_grid_dt = {'criterion': ['gini', 'entropy'], 'max_depth': [10, 20, 30], 'min_samples_split': [2, 5], 'min_samples_leaf': [1, 4]}
param_grid_knn = {'n_neighbors': [5, 7, 9], 'weights': ['uniform', 'distance'], 'metric': ['euclidean', 'manhattan']}

grid_search_lr = GridSearchCV(log_reg, param_grid_lr, cv=5)
grid_search_svm = GridSearchCV(svm, param_grid_svm, cv=5)
grid_search_dt = GridSearchCV(dt, param_grid_dt, cv=5)
grid_search_knn = GridSearchCV(knn, param_grid_knn, cv=5)

# Fit models
grid_search_lr.fit(X_train, y_train)
grid_search_svm.fit(X_train, y_train)
grid_search_dt.fit(X_train, y_train)
grid_search_knn.fit(X_train, y_train)

# Get best models
log_reg_best = grid_search_lr.best_estimator_
svm_best = grid_search_svm.best_estimator_
dt_best = grid_search_dt.best_estimator_
knn_best = grid_search_knn.best_estimator_

# Predictions and Classification Reports
print("Classification Report for Logistic Regression:")
print(classification_report(y_test, log_reg_best.predict(X_test)))

print("Classification Report for SVM:")
print(classification_report(y_test, svm_best.predict(X_test)))

print("Classification Report for Decision Tree:")
print(classification_report(y_test, dt_best.predict(X_test)))

print("Classification Report for KNN:")
print(classification_report(y_test, knn_best.predict(X_test)))

# Precision-Recall Curves
plt.figure(figsize=(12, 6))
ax = plt.gca()
plot_precision_recall_curve(log_reg_best, X_test, y_test, ax=ax, name='Logistic Regression')
plot_precision_recall_curve(svm_best, X_test, y_test, ax=ax, name='SVM')
plot_precision_recall_curve(dt_best, X_test, y_test, ax=ax, name='Decision Tree')
plot_precision_recall_curve(knn_best, X_test, y_test, ax=ax, name='KNN')
plt.title('Precision-Recall Curves')
plt.show()

# ROC Curves
plt.figure(figsize=(12, 6))
ax = plt.gca()
plot_roc_curve(log_reg_best, X_test, y_test, ax=ax, name='Logistic Regression')
plot_roc_curve(svm_best, X_test, y_test, ax=ax, name='SVM')
plot_roc_curve(dt_best, X_test, y_test, ax=ax, name='Decision Tree')
plot_roc_curve(knn_best, X_test, y_test, ax=ax, name='KNN')
plt.title('ROC Curves')
plt.show()

# Calculate and print the accuracy of each model
print(f"Accuracy on test data for Logistic Regression: {log_reg_best.score(X_test, y_test):.4f}")
print(f"Accuracy on test data for SVM: {svm_best.score(X_test, y_test):.4f}")
print(f"Accuracy on test data for Decision Tree: {dt_best.score(X_test, y_test):.4f}")
print(f"Accuracy on test data for KNN: {knn_best.score(X_test, y_test):.4f}")
