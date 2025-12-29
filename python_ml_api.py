"""
Flask ML API scaffold for Career Compass
- Exposes /predict that accepts JSON {skills, education, experience}
- Tries to load 'ml_model.xgb' with xgboost if available; otherwise returns heuristic recommendations

Run: python python_ml_api.py
"""
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Try to import xgboost if available
MODEL_PATH = 'ml_model.xgb'
model = None
try:
    import xgboost as xgb
    if os.path.exists(MODEL_PATH):
        model = xgb.Booster()
        model.load_model(MODEL_PATH)
        print('Loaded XGBoost model from', MODEL_PATH)
    else:
        print('No XGBoost model found at', MODEL_PATH)
except Exception as e:
    print('xgboost not available or failed to load model:', e)

# Simple heuristic mapping as fallback
skill_role_map = {
    'python': ['Data Scientist', 'Machine Learning Engineer', 'Software Developer'],
    'java': ['Software Developer', 'Backend Developer'],
    'javascript': ['Frontend Developer', 'Full Stack Developer'],
    'sql': ['Data Analyst', 'Database Administrator'],
    'aws': ['Cloud Engineer', 'DevOps Engineer'],
}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    skills = data.get('skills', '')
    education = data.get('education', '')
    experience = data.get('experience', 0)

    skill_list = [s.strip().lower() for s in skills.split(',') if s.strip()]

    if model is not None:
        # Placeholder: in a real model, convert inputs to feature vector
        # Here we return a dummy response indicating model used
        return jsonify({'source': 'xgboost', 'message': 'Model prediction placeholder - implement feature vector processing.'})

    # Fallback heuristic
    matches = set()
    for s in skill_list:
        if s in skill_role_map:
            matches.update(skill_role_map[s])

    if not matches:
        recs = ['Data Scientist', 'Software Developer', 'Product Manager']
    else:
        recs = list(matches)[:5]

    return jsonify({'source': 'heuristic', 'recommendations': recs, 'education': education, 'experience': experience})

if __name__ == '__main__':
    app.run(port=5001, debug=True)

import pandas as pd
from pathlib import Path

DATA_PATH = Path('data/synthetic_career_data.csv')
dataset = None
if DATA_PATH.exists():
    dataset = pd.read_csv(DATA_PATH)
    print('Loaded synthetic dataset from', DATA_PATH)
else:
    # try absolute workspace path
    alt = Path(r'P:\Desktop\PROJEcTS\CAREER\data\synthetic_career_data.csv')
    if alt.exists():
        dataset = pd.read_csv(alt)
        print('Loaded synthetic dataset from', alt)
