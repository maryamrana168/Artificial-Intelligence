import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder

def preprocess_data(df):
    df = df.ffill().bfill()
    le = LabelEncoder()
    for col in df.select_dtypes(include=['object']).columns:
        if col != 'Loan_ID':
            df[col] = le.fit_transform(df[col].astype(str))
    return df

# Load Data
train = pd.read_csv('train_u6lujuX_CVtuZ9i.csv')
test = pd.read_csv('test_Y3wMUE5_7gLdaTN.csv')
results = pd.read_csv('sample_submission_49d68Cx.csv')

# Preprocess
train = preprocess_data(train)
test = preprocess_data(test)

X_train = train.drop(['Loan_ID', 'Loan_Status'], axis=1)
y_train = train['Loan_Status']
X_test = test.drop(['Loan_ID'], axis=1)
y_test_actual = LabelEncoder().fit_transform(results['Loan_Status'])

# Task: Run with different estimators
print("\n--- TASK 02: RANDOM FOREST ---")
for n in [10, 50, 100]:
    model = RandomForestClassifier(n_estimators=n, random_state=42)
    model.fit(X_train, y_train)
    
    train_acc = accuracy_score(y_train, model.predict(X_train))
    y_pred = model.predict(X_test)
    test_acc = accuracy_score(y_test_actual, y_pred)
    
    print(f"Estimators {n}: Train Acc: {train_acc:.4f}, Test Acc: {test_acc:.4f}")