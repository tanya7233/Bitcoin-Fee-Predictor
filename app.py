from flask import Flask, render_template, request
import joblib
import numpy as np
import requests

app = Flask(__name__)

# Load trained model
model = joblib.load("fee_model.pkl")

# Function to fetch live BTC price (USD)
def get_btc_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return data["bitcoin"]["usd"]
    except:
        return None

# Function to fetch network average fee (satoshis per byte)
def get_network_fee_rate():
    try:
        url = "https://api.blockchain.info/mempool/fees"
        response = requests.get(url)
        data = response.json()
        return data.get("regular")  # satoshis per byte
    except:
        return None

# Function to estimate confirmation time priority
def get_priority(fee_btc):
    if fee_btc < 0.000002:  # adjust thresholds to BTC scale
        return "Low Priority: May take hours to confirm."
    elif fee_btc < 0.000006:
        return "Medium Priority: Likely in next few blocks."
    else:
        return "High Priority: Fast confirmation expected."

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    fee_usd = None
    btc_price = get_btc_price()
    priority = None
    tx_size = None
    network_fee_rate = get_network_fee_rate()  # sat/byte
    network_fee_btc = None
    network_fee_usd = None
    comparison = None
    prediction_sats_per_byte = None
    badge_class = None

    if request.method == "POST":
        try:
            size = float(request.form["size"])
            inputs = int(request.form["inputs"])
            outputs = int(request.form["outputs"])
            value_btc = float(request.form["value_btc"])

            # Prepare features
            features = np.array([[size, inputs, outputs, value_btc]])
            prediction = model.predict(features)[0]  # predicted fee in BTC (total)

            # Convert fee to USD if price available
            if btc_price:
                fee_usd = prediction * btc_price

            # Get confirmation priority
            priority = get_priority(prediction)
            tx_size = size

            if network_fee_rate:
                # Convert network fee rate (sat/byte) to total BTC fee
                network_fee_btc = (network_fee_rate * size) / 100000000
                if btc_price:
                    network_fee_usd = network_fee_btc * btc_price

                # Convert prediction (BTC total) into sat/byte
                prediction_sats_per_byte = (prediction * 100000000) / size
                prediction_sats_per_byte = prediction_sats_per_byte / 1000000  # scaling hack

                # Compare sat/byte vs sat/byte
                if network_fee_rate > 0:
                    comparison = ((prediction_sats_per_byte - network_fee_rate) / network_fee_rate) * 100

                    # Badge logic
                    if abs(comparison) <= 20:
                        badge_class = "badge badge-success"   # green
                    elif abs(comparison) <= 100:
                        badge_class = "badge badge-warning"   # yellow
                    else:
                        badge_class = "badge badge-danger"    # red

        except Exception as e:
            prediction = f"Error: {e}"

    return render_template(
        "index.html",
        prediction=prediction,
        fee_usd=fee_usd,
        btc_price=btc_price,
        priority=priority,
        tx_size=tx_size,
        network_fee=network_fee_btc,
        network_fee_usd=network_fee_usd,
        comparison=comparison,
        prediction_sats_per_byte=prediction_sats_per_byte,
        network_fee_rate=network_fee_rate,
        badge_class=badge_class
    )

if __name__ == "__main__":
    app.run(debug=True)