import pandas as pd
import json
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# ----------------------------
# Load dataset
# ----------------------------
df = pd.read_csv("data/livestock_data.csv")

X = df.drop("growth_rate", axis=1)
y = df["growth_rate"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ----------------------------
# Train multiple ML models
# ----------------------------
models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(random_state=42)
}

results = []
best_model = None
best_r2 = -1

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    results.append({
        "Model": name,
        "MAE": round(mae, 3),
        "R2_Score": round(r2, 3)
    })

    if r2 > best_r2:
        best_r2 = r2
        best_model = model
        best_model_name = name

# ----------------------------
# Save best model
# ----------------------------
joblib.dump(best_model, "model/livestock_growth_model.pkl")

# ----------------------------
# Save model comparison
# ----------------------------
results_df = pd.DataFrame(results)
results_df.to_csv("model/model_comparison.csv", index=False)

# ----------------------------
# Save metrics (for UI)
# ----------------------------
metrics = {
    "best_model": best_model_name,
    "r2_score": round(best_r2, 3)
}

with open("model/model_metrics.json", "w") as f:
    json.dump(metrics, f)

print("✅ Training completed successfully")
print("✅ Best model:", best_model_name)
print("✅ Metrics saved")
