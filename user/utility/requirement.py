import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from hmmlearn import hmm
from sklearn.metrics import accuracy_score, classification_report

def main():


    # Load dataset
    df = pd.read_csv(r"C:\Users\harsh\OneDrive\Documents\OneDrive\Desktop\79CAD~1.HYB\HYBRID~1\CODE\HEART_~1\media\heart-disease-dataset.csv")

    # Handle missing values
    df.dropna(inplace=True)

    # Encode categorical variables if any
    le = LabelEncoder()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = le.fit_transform(df[col])

    # Define features and target
    X = df.drop(columns=['target'])  # Assuming 'target' is the label column
    y = df['target']

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Feature Scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Support Vector Machine (SVM)
    svm_model = SVC(kernel='linear')
    svm_model.fit(X_train, y_train)
    svm_pred = svm_model.predict(X_test)
    svm_acc = accuracy_score(y_test, svm_pred)
    print("SVM Accuracy:", accuracy_score(y_test, svm_pred))
    print(classification_report(y_test, svm_pred))

    # Decision Tree J48 (C4.5)
    dt_model = DecisionTreeClassifier(criterion='entropy')
    dt_model.fit(X_train, y_train)
    dt_pred = dt_model.predict(X_test)
    dt_acc = accuracy_score(y_test, dt_pred)
    print("J48 Decision Tree Accuracy:", accuracy_score(y_test, dt_pred))
    print(classification_report(y_test, dt_pred))

    # Artificial Neural Network (ANN)
    ann_model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, activation='relu', solver='adam')
    ann_model.fit(X_train, y_train)
    ann_pred = ann_model.predict(X_test)
    ann_acc = accuracy_score(y_test, ann_pred)
    print("ANN Accuracy:", accuracy_score(y_test, ann_pred))
    print(classification_report(y_test, ann_pred))

    # Hidden Markov Model (HMM) - Multi-class approach
    unique_classes = np.unique(y)
    hmm_models = {}
    for cls in unique_classes:
        cls_indices = np.where(y_train == cls)
        X_cls = X_train[cls_indices]
        hmm_model = hmm.GaussianHMM(n_components=3, covariance_type="diag", n_iter=1000)
        hmm_model.fit(X_cls)
        hmm_models[cls] = hmm_model

    # Predicting using HMM
    hmm_predictions = []
    for sample in X_test:
        log_likelihoods = {cls: model.score(sample.reshape(1, -1)) for cls, model in hmm_models.items()}
        hmm_predictions.append(max(log_likelihoods, key=log_likelihoods.get))

    hmm_acc = accuracy_score(y_test, hmm_predictions)
    print("HMM Accuracy:", accuracy_score(y_test, hmm_predictions))
    print(classification_report(y_test, hmm_predictions))

    # Selecting the best model
    best_model = None
    best_model_name = ""
    best_accuracy = max(svm_acc, dt_acc, ann_acc, hmm_acc)

    if best_accuracy == svm_acc:
        best_model = svm_model
        best_model_name = "SVM"
    elif best_accuracy == dt_acc:
        best_model = dt_model
        best_model_name = "Decision Tree"
    elif best_accuracy == ann_acc:
        best_model = ann_model
        best_model_name = "ANN"
    elif best_accuracy == hmm_acc:
        best_model = hmm_models
        best_model_name = "HMM"

    # Save the best model
    joblib.dump(best_model, 'best_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')

    print(f"Best Model: {best_model_name} with Accuracy: {best_accuracy}")

    # Return all algorithm accuracies
    return svm_acc, dt_acc, ann_acc,hmm_acc,best_model_name
    

# Call the function and print accuracies

