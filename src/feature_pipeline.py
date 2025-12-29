from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder, StandardScaler


@dataclass
class FeatureEncoder:
    categorical_cols: List[str]
    numeric_cols: List[str]
    skills_mlb: MultiLabelBinarizer
    desired_mlb: MultiLabelBinarizer
    cat_encoder: OneHotEncoder
    scaler: StandardScaler

    @classmethod
    def create(cls) -> "FeatureEncoder":
        categorical_cols = [
            "education",
            "field_of_study",
            "personality",
            "work_preference",
            "sentiment",
        ]
        numeric_cols = [
            "age",
            "risk_taking",
            "motivation_score",
            "years_experience",
            "interest_data",
            "interest_programming",
            "interest_design",
            "interest_hardware",
            "interest_management",
            "interest_research",
            "interest_teaching",
        ]
        return cls(
            categorical_cols=categorical_cols,
            numeric_cols=numeric_cols,
            skills_mlb=MultiLabelBinarizer(),
            desired_mlb=MultiLabelBinarizer(),
            cat_encoder=OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            scaler=StandardScaler(),
        )

    def fit(self, df: pd.DataFrame) -> None:
        self.skills_mlb.fit(df["skills"])
        self.desired_mlb.fit(df["desired_roles"])
        self.cat_encoder.fit(df[self.categorical_cols])
        self.scaler.fit(df[self.numeric_cols].fillna(0))

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        skills = self.skills_mlb.transform(df["skills"])
        desired = self.desired_mlb.transform(df["desired_roles"])
        cats = self.cat_encoder.transform(df[self.categorical_cols])
        nums = self.scaler.transform(df[self.numeric_cols].fillna(0))
        return np.hstack([skills, desired, cats, nums])

