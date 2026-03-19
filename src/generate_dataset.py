import pandas as pd
import numpy as np

np.random.seed(42)

n_samples = 2000

data = {
    "feed_quality": np.random.randint(1, 4, n_samples),
    "health_score": np.random.randint(1, 11, n_samples),
    "temperature": np.random.uniform(20, 40, n_samples),
    "humidity": np.random.uniform(40, 80, n_samples),
}

growth_rate = (
    data["feed_quality"] * 0.7 +
    data["health_score"] * 0.15 -
    abs(data["temperature"] - 28) * 0.05 -
    abs(data["humidity"] - 60) * 0.02 +
    np.random.normal(0, 0.2, n_samples)
)

data["growth_rate"] = growth_rate.round(2)

df = pd.DataFrame(data)
df.to_csv("data/livestock_data.csv", index=False)

print("✅ Dataset generated successfully")
