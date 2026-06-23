import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder

def preprocess_data(df):
    # Separate numeric and categorical columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    # Fill numeric missing values with Mean
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].mean())
        
    # Fill categorical missing values with Mode
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])
    
    # Encode categorical data to numbers
    le = LabelEncoder()
    for col in categorical_cols:
        if col != 'Loan_ID':
            df[col] = le.fit_transform(df[col].astype(str))
    return df

# Load datasets
train_df = pd.read_csv('train_u6lujuX_CVtuZ9i.csv')
test_df = pd.read_csv('test_Y3wMUE5_7gLdaTN.csv')
result_df = pd.read_csv('sample_submission_49d68Cx.csv')

# Preprocess
train_df = preprocess_data(train_df)
test_df = preprocess_data(test_df)

X_train = train_df.drop(['Loan_ID', 'Loan_Status'], axis=1)
y_train = train_df['Loan_Status']
X_test = test_df.drop(['Loan_ID'], axis=1)
# Encode the results file for comparison
le_res = LabelEncoder()
y_test_actual = le_res.fit_transform(result_df['Loan_Status'])

# Run Task 01
print("--- TASK 01: DECISION TREE ---")
for depth in [2, 5, None]:
    dt = DecisionTreeClassifier(max_depth=depth, random_state=42)
    dt.fit(X_train, y_train)
    
    train_acc = accuracy_score(y_train, dt.predict(X_train))
    y_pred = dt.predict(X_test)
    test_acc = accuracy_score(y_test_actual, y_pred)
    
    print(f"Depth {depth}: Train Acc: {train_acc:.4f}, Test Acc: {test_acc:.4f}")