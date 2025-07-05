# 📊 Market Data Stream Analyzer

A lightweight, modular Python CLI tool to analyze stock market data from JSON files.  
Built with `argparse`, clean code practices, and extensibility in mind.

---

## 🚀 Features

- 📁 Filter stock data by symbol (e.g., `AAPL`)
- 🕒 Group entries into configurable time windows (`--window`)
- 📈 Compute **Moving Average** over a sliding window
- 💰 Calculate **VWAP** (Volume Weighted Average Price) per time bucket
- 🪙 Find **Min** and **Max** prices per time bucket
- 📊 Calculate statistical metrics:
  - `--stats median,std,change`
- 🖼️ Generate price plots with:
  - Average bucket price
  - Moving average overlay (`--plot`)
- 🎨 Color-coded CLI output with `colorama`
- 🛠️ Built using `argparse` and clean modular structure

---

## 🧪 Example Usage

```bash
python -m src.main \
  --file data/sample_data.json \
  --symbol AAPL \
  --window 3 \
  --vwap \
  --min \
  --max \
  --stats median,std,change \
  --plot

```

### 📤 Sample Output

```
File: data/sample_data.json
Symbol: AAPL
Window: 3

AAPL Moving averages (window = 3):
2023-10-01T09:32:40 101.17
...

Time Window: 2023-10-01 09:30:00
  VWAP for AAPL: 101.20
  Minimum price for AAPL: 100.5
  Maximum price for AAPL: 102.2
  Median: 101.00
  Standard deviation: 0.84
  Percentage change: +1.02%

```
## A combined plot is saved to:
output/plots/AAPL_combined_plot.png
---

## 📁 Project Structure

```
market-data-stream-analyzer/
├── data/                 # Raw or sample JSON input files
├── output/               # Auto-generated results (ignored in Git)
│   └── plots/            # Plots created via --plot
├── src/                  # Main source code
│   ├── main.py           # CLI entry point
│   ├── plotting.py       # Matplotlib-based plot generator
│   ├── indicators/       # VWAP, Moving Average, Min/Max, Stats
│   └── ...
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── .gitignore            # Excludes output, __pycache__, etc.

```

---

## 🔮 Coming Soon

- 📉 Export analysis results to CSV/Excel (`--export`)
- 📊 Volume & price plotting per symbol
- 🧮 Strategy backtesting modules (e.g. SMA crossover)
- 🌐 Live stream support (WebSocket or REST polling)
- 📦 `pip install -e .` support for CLI install

---

## 💡 Motivation

This project is part of a larger learning path toward HFT and quantitative finance tooling — documenting a journey from foundational CLI skills to real-world market data pipelines.

---

## ✅ Requirements

- Python 3.8+
- JSON data in the expected schema format  
  *(see `sample_data.json` in the `data/` folder)*

---

## 👨‍💻 Author

**Harshit Singh**  
GitHub: [@Haxedblack](https://github.com/Haxedblack)

---

## 🧠 License

MIT License — feel free to use, fork, or build upon it.
