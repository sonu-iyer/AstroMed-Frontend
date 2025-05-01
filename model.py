import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load your enhanced dataset
df = pd.read_csv("astrology_doctor_prediction_dataset_advanced_v2.csv")

# Label encode categorical columns
from sklearn.preprocessing import LabelEncoder

# Dictionary to store encoders
label_encoders = {}

# Encode all categorical features
for col in ['sun_sign', 'moon_sign', 'ascendant', 'mars_house', 'mercury_house',
            'jupiter_house', 'saturn_house', 'rahu_house', 'ketu_house', 'moon_phase']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le


# Split into features and target
X = df.drop("is_doctor", axis=1)
y = df["is_doctor"]

# Apply SMOTE to balance the dataset
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Split data into train/test
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Define parameter grid for fine-tuning
param_grid = {
    'learning_rate': [0.05, 0.1, 0.2],
    'max_depth': [5, 7, 9],
    'n_estimators': [100, 200],
    'subsample': [0.7, 0.8, 1.0],
    'scale_pos_weight': [1.2, 1.5, 1.8]
}

# Initialize the model
#xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
# Initialize the model without 'use_label_encoder'
xgb_model = XGBClassifier(eval_metric='logloss')


# Set up GridSearchCV
grid_search = GridSearchCV(
    estimator=xgb_model,
    param_grid=param_grid,
    cv=3,
    scoring='accuracy',
    verbose=1,
    n_jobs=-1
)

# Fit the model
grid_search.fit(X_train, y_train)

# Get best model and evaluate
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

# Print results
# Predict using the best model
import pickle

# Save model
with open("xgb_doctor_model.pkl", "wb") as f:
    pickle.dump(best_model, f)
best_model.save_model('new_model.model')

# Save label encoders
with open("label_encoders.pkl", "wb") as f:
    pickle.dump(label_encoders, f)

model = xgb.Booster() 
model.load_model('new_model.model')
