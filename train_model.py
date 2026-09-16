import joblib

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


# -----------------------------
# Training Data
# -----------------------------

X = [
    [20, 80, 20],
    [25, 90, 22],
    [30, 100, 25],
    [35, 120, 27],
    [40, 150, 30],
    [45, 180, 32],
    [50, 200, 35],
    [55, 220, 38]
]


# 0 = Low Risk
# 1 = High Risk

y = [
    0,
    0,
    0,
    0,
    1,
    1,
    1,
    1
]


# -----------------------------
# Create ML Pipeline
# -----------------------------

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression())
])


# -----------------------------
# Train Model
# -----------------------------

pipeline.fit(X, y)


# -----------------------------
# Save Pipeline
# -----------------------------

joblib.dump(
    pipeline,
    "D:/M.Tech/AI_ENGINEER/model_pipeline.pkl"
)


print("Model trained successfully.")
print("Model saved inside AI_ENGINEER/model_pipeline.pkl")