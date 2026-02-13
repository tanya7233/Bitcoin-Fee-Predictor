import requests
import pandas as pd

BASE_URL = "https://blockchain.info/unconfirmed-transactions?format=json"

def get_latest_transactions(limit=50):
    """Fetch latest unconfirmed Bitcoin transactions"""
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        data = response.json()
        txs = data.get("txs", [])
        rows = []
        for tx in txs[:limit]:
            rows.append({
                "txid": tx["hash"],
                "time": tx["time"],
                "size": tx.get("size", 0),
                "fee": tx.get("fee", 0),
                "inputs": len(tx.get("inputs", [])),
                "outputs": len(tx.get("out", [])),
                "value_btc": sum(o["value"] for o in tx["out"]) / 1e8
            })
        return pd.DataFrame(rows)
    else:
        print("Error fetching transactions")
        return pd.DataFrame()

if __name__ == "__main__":
    limit = int(input("Enter number of latest transactions to fetch (default 50): ") or 50)
    filename = input("Enter output CSV filename (default: latest_tx.csv): ") or "latest_tx.csv"
    
    df = get_latest_transactions(limit)
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} transactions to {filename}")
    print(df.head(10))  # preview first 10 rows