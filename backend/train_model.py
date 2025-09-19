# FIX: Corrected indentation by replacing non-standard whitespace with regular spaces.
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib
import os, json

# Define features that will come from the questionnaire
features = [
    'math_score', 'bio_score', 'interest_tech', 'interest_medicine', 
    'interest_design', 'interest_research', 'coding_skill', 'creativity_skill'
]

# Load career titles dynamically from the JSON file
try:
    with open('science_careers.json', 'r') as f:
        careers_data = json.load(f)
    target_careers = [career['title'] for career in careers_data['Science']['careers']]
except (FileNotFoundError, KeyError) as e:
    print(f"Error reading careers from JSON file: {e}. Using a default list.")
    # Fallback list in case the JSON is missing or malformed
    target_careers = [
        'Computer Science & IT', 'Medical (MBBS/BDS/AYUSH)', 'Architecture',
        'Pure Sciences (Physics / Chemistry / Mathematics / Biology)', 'Pharmacy',
        'Agricultural Sciences & Horticulture', 'Nursing & Allied Health Sciences',
        'Veterinary Science', 'Data Science, AI & Analytics', 'Engineering (General)'
    ]

# Generate synthetic data based on logical rules
def generate_data(n_samples=2500):
    data = []
    for _ in range(n_samples):
        career_choice = np.random.choice(target_careers)
        row = {
            'math_score': np.random.randint(1, 5), # Scale: 1(Poor) to 4(Excellent)
            'bio_score': np.random.randint(1, 5),
            'interest_tech': np.random.choice([0, 1]), # 0(No), 1(Yes)
            'interest_medicine': np.random.choice([0, 1]),
            'interest_design': np.random.choice([0, 1]),
            'interest_research': np.random.choice([0, 1]),
            'coding_skill': np.random.choice([0, 1]),
            'creativity_skill': np.random.choice([0, 1])
        }
        
        # Apply rules to make data logical
        if career_choice in ['Computer Science & IT', 'Data Science, AI & Analytics', 'Engineering (General)']:
            row['math_score'] = np.random.randint(3, 5)
            row['interest_tech'] = 1
            if career_choice != 'Engineering (General)': row['coding_skill'] = 1
        elif career_choice in ['Medical (MBBS/BDS/AYUSH)', 'Veterinary Science', 'Nursing & Allied Health Sciences', 'Pharmacy']:
            row['bio_score'] = np.random.randint(3, 5)
            row['interest_medicine'] = 1
        elif career_choice == 'Architecture':
            row['math_score'] = np.random.randint(2, 5)
            row['creativity_skill'] = 1
            row['interest_design'] = 1
        elif career_choice == 'Pure Sciences (Physics / Chemistry / Mathematics / Biology)':
            row['interest_research'] = 1
            if np.random.rand() > 0.5: row['math_score'] = np.random.randint(3, 5)
            else: row['bio_score'] = np.random.randint(3, 5)
        
        row['career'] = career_choice
        data.append(row)
        
    return pd.DataFrame(data)

# --- Main Training Process ---
print("Generating synthetic data...")
df = generate_data(3000)
X = df[features]
y = df['career']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Training Logistic Regression model...")
model = LogisticRegression(max_iter=1500, class_weight='balanced')
model.fit(X_train, y_train)

print(f"Model Accuracy: {model.score(X_test, y_test):.2f}")

if not os.path.exists('models'):
    os.makedirs('models')

joblib.dump(model, 'models/career_model.joblib')
joblib.dump(model.classes_, 'models/model_classes.joblib')

print("✅ Model trained and saved successfully in the 'models' directory!")