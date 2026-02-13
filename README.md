# Bitcoin Transaction Fee Predictor

A Flask-based web app that predicts Bitcoin transaction fees using a trained ML model, compares predictions with live network data, and displays results with intuitive color-coded badges.

## 🚀 Features
- Predicts transaction fee (BTC total + USD equivalent)
- Shows predicted fee rate (sat/byte)
- Fetches live BTC price from CoinGecko API
- Fetches network average fee rate from Blockchain.info API
- Compares prediction vs. network fee rate
- Color-coded badges (green/yellow/red) for accuracy
- Confirmation time estimate (Low, Medium, High Priority)

## 🛠 Tech Stack
- **Backend:** Python (Flask, NumPy, joblib, requests)
- **Frontend:** HTML, CSS (Bootstrap-style badges)
- **Data Sources:** CoinGecko API, Blockchain.info API
- **Model:** Trained ML model (`fee_model.pkl`)

## 📂 Project Structure
bitcoin-fee-predictor/ │── app.py                # Main Flask app │── fee_model.pkl         # Trained ML model │── model_training.py     # Script to train model │── generate_synthetic.py # Script to generate synthetic dataset │── synthetic_bitcoin.csv # Dataset │── latest_tx.csv         # Latest transactions dataset │── latest_tx.py          # Script for fetching transactions │── requirements.txt      # Dependencies │── README.md             # Project documentation │── static/ │   └── style.css         # Custom styles │── templates/ │   ├── base.html         # Base layout │   ├── index.html        # Main UI │   └── home.html         # Optional landing page


## ⚙️ Installation & Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/bitcoin-fee-predictor.git
   cd bitcoin-fee-predictor

2. Install dependencies:
pip install -r requirements.txt

3. Run the app:
python app.py

4. Open in browser
http://127.0.0.1:5000/

📜 License
© 2026 Bitcoin Fee Predictor  Tanya



