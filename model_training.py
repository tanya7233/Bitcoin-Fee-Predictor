import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

def train_model(datafile="synthetic_bitcoin.csv", modelfile="fee_model.pkl"):
    # Load dataset
    df = pd.read_csv(datafile)

    # Features and target
    X = df[["size", "inputs", "outputs", "value_btc"]]
    y = df["fee"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluation
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Model trained successfully!")
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"R² Score: {r2:.2f}")

    # Save model
    joblib.dump(model, modelfile)
    print(f"Model saved to {modelfile}")

if __name__ == "__main__":
    train_model()