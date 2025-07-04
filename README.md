# 📊 Market Data Stream Analyzer

A lightweight, modular Python CLI tool to analyze stock market data from JSON files.  
Built with `argparse`, clean code practices, and extensibility in mind.

---

## 🚀 Features

- 📁 Filter stock data by symbol (e.g., `AAPL`)
- 📈 Compute **Moving Average** over a configurable window
- 💰 Calculate **VWAP** (Volume Weighted Average Price)
- 🪙 Find **Min** and **Max** prices
- 🛠️ Built using `argparse` and clean modular structure

---

## 🧪 Example Usage

```bash
python src/main.py --file data/sample_data.json --symbol AAPL --window 5 --vwap --min --max
```

### 📤 Output:

```
File: data/sample_data.json
Symbol: AAPL
Window: 5

 AAPL Moving averages (window = 5):
2023-10-01T09:34:00 172.76
VWAP for AAPL: 172.79
Minimum price for AAPL: 170.5
Maximum price for AAPL: 175.3
```

---

## 📁 Project Structure

```plaintext
market-data-stream-analyzer/
├── data/                 # Raw or sample JSON input files
├── output/               # (Optional) Result logs or summaries
├── src/                  # Main source code
│   ├── main.py           # CLI entry point
│   ├── indicators/       # VWAP, Moving Average, Min/Max logic
│   ├── parser.py         # (Coming soon) Centralized CLI argument logic
│   ├── analyzer.py       # (Coming soon) Modular analytics toolkit
├── requirements.txt      # Python dependencies (if any)
├── README.md             # This file
```

---

## 🔮 Coming Soon

- [ ] 🧪 Volatility & standard deviation metrics
- [ ] 📉 Real-time stream support (via WebSocket)
- [ ] 🧮 Strategy testing modules (e.g., SMA crossover)
- [ ] 📤 CSV/Excel export of results
- [ ] 📦 Packaged CLI tool (`pip install -e .` support)

---

## 💡 Motivation

This project is part of a larger learning path toward HFT and quantitative finance tooling — documenting a journey from foundational CLI skills to real-world market data pipelines.

---

## ✅ Requirements

- Python 3.8+
- JSON data in the expected schema format  
(*see `sample_data.json` in `data/` folder*)

---

## 👨‍💻 Author

**Harshit Singh**  
GitHub: [@Haxedblack](https://github.com/Haxedblack)

---

## 🧠 License

MIT License — feel free to use, fork, or build upon it.