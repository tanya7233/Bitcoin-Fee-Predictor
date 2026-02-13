import pandas as pd
import numpy as np

def generate_synthetic_data(n=10000, filename="synthetic_bitcoin.csv"):
    data = {
        "txid": [f"tx_{i}" for i in range(n)],
        "time": pd.date_range("2025-01-01", periods=n, freq="min"),
        "size": np.random.randint(150, 2000, n),
        "fee": np.random.randint(50, 2000, n),
        "inputs": np.random.randint(1, 5, n),
        "outputs": np.random.randint(1, 4, n),
        "value_btc": np.random.uniform(0.0001, 5, n)
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Synthetic dataset saved to {filename} with {len(df)} rows.")

if __name__ == "__main__":
    generate_synthetic_data()