import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("data/processed/model_results.csv")
os.makedirs("figures", exist_ok=True)

print(df.sort_values("MAE").to_string(index=False))

df.plot(x="Model", y=["MAE", "RMSE"], kind="bar", figsize=(9, 5))
plt.title("Model Performance Comparison")
plt.ylabel("Error")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("figures/model_comparison.png", dpi=300)
plt.show()

best = df.loc[df["MAE"].idxmin()]
print("\nBest model by MAE:", best["Model"])
print("MAE:", round(best["MAE"], 2))
print("RMSE:", round(best["RMSE"], 2))
print("R²:", round(best["R2"], 3))