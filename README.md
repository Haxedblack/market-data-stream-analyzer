# 📊 Market Data Stream Analyzer

A lightweight Python CLI tool to analyze stock market data from JSON files.

---

## 🚀 Features

- Filter stock data by symbol (e.g., `AAPL`)
- Calculate moving average over a configurable window
- Command-line interface using `argparse`
- Easily extendable for more analytics (volatility, volume, etc.)

---

## 📁 Project Structure

<pre>
market-data-stream-analyzer/
├── data/                 # Raw or sample JSON input files
├── output/               # Analysis results (optional)
├── src/                  # Main source code
│   ├── main.py           # CLI entry point
│   ├── parser.py         # (Coming soon) CLI parsing logic
│   ├── analyzer.py       # (Coming soon) Analysis utilities
├── requirements.txt
├── README.md
</pre>

---

## 🧪 Usage

```bash
python src/main.py --file data/sample_data.json --symbol AAPL --window 5
