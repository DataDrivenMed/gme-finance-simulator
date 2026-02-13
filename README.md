# GME Finance Scenario Simulator

A slider-based decision tool that models the financial and operational implications of Graduate Medical Education trainee movements, payment rate changes, and affiliation scenarios.

## Live Demo

[View the live simulator →](https://gme-finance-simulator.streamlit.app)

## What It Does

This tool answers the question every DIO and CFO asks: **"What happens to our GME finances if...?"**

| Scenario Lever | What You Can Model |
|---|---|
| **Trainee Volume** | Add or reduce residents and fellows across the enterprise |
| **Site Distribution** | Shift trainees between primary and affiliated hospitals |
| **Payment Rates** | Model IME, DME, and Medicaid rate changes (including cuts) |
| **Operational Parameters** | Adjust case volume, salary increases, site count |

The simulator instantly recalculates revenue, cost, net position, and generates a waterfall chart showing exactly which factors drive the change.

## Key Features

- **Real-time financial modeling** with 8 adjustable parameters
- **Waterfall chart** decomposing baseline-to-scenario changes
- **IME sensitivity analysis** showing break-even thresholds
- **Dynamic narrative** that explains what the numbers mean
- **Full comparison table** for board-ready export

## Design Philosophy

- Board-packet quality: stands alone as a PDF screenshot
- Decision-oriented: every visual answers "so what?"
- No jargon: accessible to clinical and financial leadership
- Slider-driven: explore scenarios without touching data

## Data

All parameters are **synthetic** but modeled on realistic mid-size academic medical center GME financials. The model includes Medicare IME/DME, state Medicaid GME, clinical revenue, and full cost allocation.

## Local Development

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Author

**Per Nilsson**  
Director, Accreditation & Strategic Planning  
[LinkedIn](https://linkedin.com/in/pernilsson) · [GitHub](https://github.com/pernilsson)

---

*Built as part of a decision-architecture portfolio demonstrating enterprise analytics for academic medicine leadership.*
