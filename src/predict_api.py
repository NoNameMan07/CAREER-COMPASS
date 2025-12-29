"""
Flask prediction service for the Sensei Phase 1 engine.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

try:
    from src import feature_pipeline  # noqa: F401
except Exception:
    try:
        import feature_pipeline  # noqa: F401
    except Exception:
        feature_pipeline = None

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DEFAULT_SENTIMENT_MAP = {
    "happy": {"neg": 0.05, "neu": 0.2, "pos": 0.75},
    "neutral": {"neg": 0.2, "neu": 0.6, "pos": 0.2},
    "stressed": {"neg": 0.6, "neu": 0.3, "pos": 0.1},
}

MARKET_TREND_MAP = {
    "Data Scientist": "rising",
    "Machine Learning Engineer": "rising",
    "Data Analyst": "stable",
    "Software Developer": "stable",
    "Full Stack Developer": "stable",
    "DevOps Engineer": "rising",
    "Cloud Engineer": "rising",
    "Cybersecurity Analyst": "rising",
    "Embedded Systems Engineer": "stable",
    "VLSI Engineer": "stable",
    "Mechanical Design Engineer": "stable",
    "Civil Engineer": "stable",
    "Project Manager": "stable",
    "Product Manager": "stable",
    "Business Analyst": "stable",
    "Research Scientist": "stable",
    "Bioinformatics Scientist": "rising",
    "Robotics Engineer": "rising",
    "Blockchain Developer": "falling",
    "UX/UI Designer": "stable",
}


class SenseiPredictor:
    def __init__(self, artifacts_dir: Path, configs_dir: Path):
        self.model = joblib.load(artifacts_dir / "xgb_onevsrest.joblib")
        self.encoder = joblib.load(artifacts_dir / "feature_encoder.joblib")
        self.label_binarizer = joblib.load(artifacts_dir / "label_binarizer.joblib")
        self.roles = self.label_binarizer.classes_.tolist()
        self.thresholds = self._load_thresholds(artifacts_dir)
        self.role_required = json.loads((configs_dir / "role_required_skills.json").read_text())
        self.skill_courses = json.loads((configs_dir / "skill_to_course.json").read_text())

    def _load_thresholds(self, artifacts_dir: Path) -> np.ndarray:
        path = artifacts_dir / "thresholds.npy"
        if path.exists():
            arr = np.load(path)
            if arr.shape[0] != len(self.roles):
                return np.full(len(self.roles), 0.5)
            return arr
        return np.full(len(self.roles), 0.5)

    def _sanitize(self, payload: Dict) -> Dict:
        defaults = {
            "age": 25,
            "education": "UG",
            "field_of_study": "CS",
            "skills": [],
            "personality": "ambivert",
            "risk_taking": 3,
            "work_preference": "team",
            "motivation_score": 70,
            "sentiment": "neutral",
            "years_experience": 2,
            "desired_roles": [],
            "interest_data": 3,
            "interest_programming": 3,
            "interest_design": 3,
            "interest_hardware": 3,
            "interest_management": 3,
            "interest_research": 3,
            "interest_teaching": 3,
        }
        clean = {**defaults, **payload}
        for key in ["skills", "desired_roles"]:
            clean[key] = clean.get(key) or []
        return clean

    def _to_dataframe(self, payload: Dict) -> pd.DataFrame:
        clean = self._sanitize(payload)
        return pd.DataFrame([clean])

    def predict(self, payload: Dict) -> Dict:
        df = self._to_dataframe(payload)
        features = self.encoder.transform(df)
        proba = self.model.predict_proba(features)[0]

        # Rule features
        user_skills = set(df.iloc[0]["skills"]) if isinstance(df.iloc[0]["skills"], list) else set()
        exp_years = float(df.iloc[0]["years_experience"]) if pd.notna(df.iloc[0]["years_experience"]) else 0.0
        exp_norm = min(exp_years / 5.0, 1.0)
        sent = DEFAULT_SENTIMENT_MAP.get(df.iloc[0]["sentiment"], DEFAULT_SENTIMENT_MAP["neutral"]) 
        sent_pos = float(sent.get("pos", 0.33))

        # Interest fit (limited mapping based on available sliders)
        interest_data = float(df.iloc[0].get("interest_data", 3))
        interest_prog = float(df.iloc[0].get("interest_programming", 3))
        interest_design = float(df.iloc[0].get("interest_design", 3))
        interest_mgmt = float(df.iloc[0].get("interest_management", 3))

        role_interest = {
            "Data Scientist": (interest_data, interest_prog),
            "Data Analyst": (interest_data, interest_prog),
            "Machine Learning Engineer": (interest_data, interest_prog),
            "Software Developer": (interest_prog, interest_data),
            "Full Stack Developer": (interest_prog, interest_design),
            "Frontend Developer": (interest_design, interest_prog),
            "Backend Developer": (interest_prog, interest_data),
            "Product Manager": (interest_mgmt, interest_design),
            "Business Analyst": (interest_mgmt, interest_data),
            "Blockchain Developer": (interest_prog, interest_data),
        }

        # Compute blended score per role
        blended = []
        for i, role in enumerate(self.roles):
            ml = float(proba[i])
            required = self.role_required.get(role, [])
            if required:
                overlap = len(set(required) & user_skills)
                skill_fit = overlap / max(len(required), 1)
            else:
                skill_fit = 0.0

            a, b = role_interest.get(role, (3.0, 3.0))
            interest_fit = (a + b) / 10.0  # normalize to ~[0,1]

            raw = 0.6 * ml + 0.25 * skill_fit + 0.1 * interest_fit + 0.05 * (0.5 * exp_norm + 0.5 * sent_pos)
            blended.append(raw)

        # Temperature-scaled softmax to produce sharp percentages
        temperature = 0.7
        logits = np.array(blended) / max(temperature, 1e-6)
        exps = np.exp(logits - logits.max())
        scores = exps / exps.sum()

        ranked = np.argsort(scores)[::-1]
        top_indices = ranked[:5]

        recommendations = [
            {"role": self.roles[idx], "score": float(scores[idx])} for idx in top_indices
        ]

        binary_preds = (proba >= self.thresholds).astype(int)
        activated_roles = [self.roles[i] for i, flag in enumerate(binary_preds) if flag]
        if not activated_roles:
            activated_roles = [self.roles[top_indices[0]]]

        top_role = recommendations[0]["role"]
        skill_gap = self._build_skill_gap(top_role, df.iloc[0]["skills"])
        try:
            learning_plan = self._build_learning_plan(skill_gap["missing"])
        except Exception:
            learning_plan = []

        emotion = {
            "motivation_score": int(df.iloc[0]["motivation_score"]),
            "sentiment": DEFAULT_SENTIMENT_MAP.get(
                df.iloc[0]["sentiment"], DEFAULT_SENTIMENT_MAP["neutral"]
            ),
        }

        market_trend = {role: MARKET_TREND_MAP.get(role, "stable") for role in activated_roles}

        return {
            "top_recommendations": recommendations,
            "skill_gaps": {"required": skill_gap["required"], "have": skill_gap["have"], "missing": skill_gap["missing"]},
            "learning_plan": learning_plan,
            "emotion": emotion,
            "market_trend": market_trend,
        }

    def _build_skill_gap(self, role: str, user_skills: List[str]) -> Dict[str, List[str]]:
        required = self.role_required.get(role, [])
        have = list(set(user_skills))
        missing = [skill for skill in required if skill not in have]
        return {"required": required, "have": have, "missing": missing}

    def _build_learning_plan(self, missing_skills: List[str]) -> List[Dict]:
        plan = []
        for skill in missing_skills:
            course = self.skill_courses.get(skill)
            if course:
                if isinstance(course, dict):
                    entry = {"skill": skill, **course}
                else:
                    entry = {"skill": skill, "course": str(course), "source": "online", "weeks": 2}
            else:
                entry = {"skill": skill, "course": f"Deep dive into {skill}", "source": "TBD", "weeks": 2}
            plan.append(entry)
        return plan


def create_app(predictor: SenseiPredictor, template_dir: Path | None = None) -> Flask:
    template_dir = (template_dir or Path(__file__).resolve().parents[1] / "templates").resolve()
    app = Flask(__name__, template_folder=str(template_dir))
    
    # Enable CORS for all routes - allow requests from localhost:3000
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })

    @app.route("/", methods=["GET"])
    def index():
        logger.info("GET / - Health check")
        return jsonify({"status": "predictor_ok"}), 200

    @app.route("/predict", methods=["POST", "OPTIONS"])
    def predict_route():
        if request.method == "OPTIONS":
            return "", 200
        
        try:
            logger.info(f"POST /predict - Content-Type: {request.content_type}")
            payload = request.get_json(force=True)
            logger.info(f"Prediction request received with payload: {payload}")
            
            result = predictor.predict(payload)
            logger.info(f"Prediction successful: {result['top_recommendations']}")
            
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}", exc_info=True)
            return jsonify({
                "error": str(e),
                "message": "Failed to generate predictions"
            }), 400

    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Flask API for Sensei predictions.")
    parser.add_argument("--artifacts_dir", type=Path, default=Path("artifacts"))
    parser.add_argument("--configs_dir", type=Path, default=Path("configs"))
    parser.add_argument("--template_dir", type=Path, default=Path("templates"))
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    logger.info(f"Starting Sensei Prediction API")
    logger.info(f"  Artifacts: {args.artifacts_dir}")
    logger.info(f"  Configs: {args.configs_dir}")
    logger.info(f"  Listening on {args.host}:{args.port}")

    predictor = SenseiPredictor(args.artifacts_dir, args.configs_dir)
    app = create_app(predictor, args.template_dir)
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()

