import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

df = pd.read_csv("data/processed/ml_dataset.csv")
df = df.sort_values("year")

features = ["previous_year_cases", "previous_year_rate", "year"]
target = "total_cases"

train = df[df["year"] <= 2020]
test = df[df["year"] > 2020]

X_train, y_train = train[features], train[target]
X_test, y_test = test[features], test[target]

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=200, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42)
}

results = []

for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    results.append({
        "Model": name,
        "MAE": mean_absolute_error(y_test, predictions),
        "RMSE": np.sqrt(mean_squared_error(y_test, predictions)),
        "R2": r2_score(y_test, predictions)
    })

results_df = pd.DataFrame(results).sort_values("MAE")
print(results_df.to_string(index=False))
results_df.to_csv("data/processed/model_results.csv", index=False)