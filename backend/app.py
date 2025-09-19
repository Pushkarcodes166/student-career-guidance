from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import pandas as pd
import json
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# --- Database Connection ---
# IMPORTANT: Replace with your MySQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'database': 'career_guidance',
    'user': 'root',
    'password': 'root' # <--- CHANGE THIS
}

def create_db_connection():
    try:
        # FIX: Replaced invalid whitespace with standard spaces throughout the file
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# --- Load ML Model and Career Data ---
try:
    model = joblib.load('models/career_model.joblib')
    model_classes = joblib.load('models/model_classes.joblib')
    with open('science_careers.json', 'r') as f:
        science_careers_data = json.load(f)
except FileNotFoundError as e:
    print(f"FATAL ERROR: Model or data file not found: {e}")
    print("Please run train_model.py first to generate model files.")
    model = None
    
# --- Helper Function for Preprocessing ---
def preprocess_input(data):
    performance_map = {'Poor': 1, 'Average': 2, 'Good': 3, 'Excellent': 4}
    yes_no_map = {'Yes': 1, 'No': 0}
    processed_features = {
        'math_score': performance_map.get(data.get('q4_math_performance'), 2),
        'bio_score': performance_map.get(data.get('q5_bio_performance'), 2),
        'interest_tech': yes_no_map.get(data.get('q6_tech_interest'), 0),
        'interest_medicine': yes_no_map.get(data.get('q7_medicine_interest'), 0),
        'interest_design': yes_no_map.get(data.get('q8_design_interest'), 0),
        'interest_research': yes_no_map.get(data.get('q9_research_interest'), 0),
        'coding_skill': yes_no_map.get(data.get('q14_coding_interest'), 0),
        'creativity_skill': yes_no_map.get(data.get('q15_creative_interest'), 0)
    }
    feature_order = [
        'math_score', 'bio_score', 'interest_tech', 'interest_medicine', 
        'interest_design', 'interest_research', 'coding_skill', 'creativity_skill'
    ]
    return pd.DataFrame([processed_features])[feature_order]

# --- API Endpoints ---
@app.route('/career-path/science', methods=['GET'])
def get_science_careers():
    return jsonify(science_careers_data)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded. Check backend logs."}), 500

    try:
        data = request.json
        processed_data = preprocess_input(data)
        probabilities = model.predict_proba(processed_data)[0]
        
        top_3_indices = probabilities.argsort()[-3:][::-1]
        results = [
            {"career": model_classes[i], "score": round(float(probabilities[i]) * 100, 2)}
            for i in top_3_indices
        ]

        conn = create_db_connection()
        # IMPROVEMENT: Use a try...finally block to ensure the database connection is always closed
        if conn:
            try:
                with conn.cursor() as cursor:
                    query = ("INSERT INTO students (q1_enjoy_subject, q4_math_performance, "
                             "q5_bio_performance, q6_tech_interest, q7_medicine_interest, "
                             "q8_design_interest, q9_research_interest, q14_coding_interest, "
                             "q15_creative_interest, predicted_career_1, score_1, "
                             "predicted_career_2, score_2, predicted_career_3, score_3) "
                             "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                    
                    # FIX: Removed stray characters from the end of lines for valid syntax
                    db_values = (
                        data.get('q1_enjoy_subject'), data.get('q4_math_performance'),
                        data.get('q5_bio_performance'), data.get('q6_tech_interest'),
                        data.get('q7_medicine_interest'), data.get('q8_design_interest'),
                        data.get('q9_research_interest'), data.get('q14_coding_interest'),
                        data.get('q15_creative_interest'), results[0]['career'],
                        results[0]['score'], results[1]['career'], results[1]['score'],
                        results[2]['career'], results[2]['score'])
                    
                    cursor.execute(query, db_values)
                    conn.commit()
                    print("💾 Prediction saved to database.")
            except Error as e:
                print(f"Database error during prediction save: {e}")
            finally:
                conn.close()

        return jsonify(results)

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": "An error occurred during prediction."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)