# Adverse Drug Reaction (ADR) — FAERS Pharmacovigilance + Risk Prediction (Doxorubicin)

Hybrid pharmacovigilance workflow using the FDA **FAERS** spontaneous reporting system (via the **openFDA** API) to:

- Collect adverse event reports for **DOXORUBICIN** (3,000 records)
- Perform exploratory analysis (EDA)
- Run basic signal detection using **PRR** (Proportional Reporting Ratio)
- Train a simple ML model to predict an **ADR risk label** and deploy it with **Streamlit**

> Important: FAERS is a *spontaneous reporting* database. Analyses here describe reporting patterns and **do not establish causality**.

---

## What’s in this repo

### Data

- Raw API output: `data/raw/faers/doxorubicin_3000_raw.json`
- Processed dataset: `data/processed/doxorubicin_3000_faers.csv`

The processed CSV contains these fields (extracted in the collection notebook):

- `Drug` (constant: `DOXORUBICIN`)
- `Reaction` (MedDRA PT from `reactionmeddrapt` when available)
- `Serious`
- `Age`
- `Sex` (as coded in FAERS: commonly `1`, `2`, `0`)
- `Report_Date` (received date, e.g. `20140312`)

### Notebooks (recommended order)

1. `notebooks/01_Data_Collection.ipynb`
	- Pulls FAERS reports using openFDA: `https://api.fda.gov/drug/event.json`
	- Uses pagination (`limit=100`, `skip=0..`) to fetch 3,000 rows
	- Saves both raw JSON and processed CSV
2. `notebooks/02_EDA.ipynb`
	- Professional EDA on the processed CSV (missingness, distributions, plots)
	- Includes a pharmacovigilance caution about under-reporting/confounding
3. `notebooks/03_Signal_Detection_PRR.ipynb`
	- Computes PRR + chi-square per reaction
	- Note: this notebook uses placeholder values for non-doxorubicin counts (`C` and `D`), so treat PRR here as **illustrative** unless you replace those with a real comparator dataset
4. `notebooks/04_Model_Building.ipynb`
	- Builds a RandomForest classifier
	- Target: `Risk_Label` where “high risk” = reactions in the top 10 most frequent reactions
	- Features used: `Age`, `Sex`, `Year` (extracted from `Report_Date`)
	- Saves model artifact: `notebooks/adr_risk_model.pkl`
	- Includes SHAP-based explainability

### Streamlit app

`app/streamlit_app.py` loads `notebooks/adr_risk_model.pkl` and predicts ADR risk from:

- Age (slider)
- Sex (Male/Female mapped to `1/2`)
- Year (2013–2015)

The app uses a probability threshold of `0.2` to show “High Risk” vs “Low Risk”.

---

## Project structure

```text
.
├─ app/
│  └─ streamlit_app.py
├─ data/
│  ├─ processed/
│  │  └─ doxorubicin_3000_faers.csv
│  └─ raw/
│     └─ faers/
│        └─ doxorubicin_3000_raw.json
├─ notebooks/
│  ├─ 01_Data_Collection.ipynb
│  ├─ 02_EDA.ipynb
│  ├─ 03_Signal_Detection_PRR.ipynb
│  ├─ 04_Model_Building.ipynb
│  └─ adr_risk_model.pkl
├─ main.py
├─ requirements.txt
├─ pyproject.toml
└─ README.md
```

---

## Setup (Windows)

Python version used in this repo is **3.13** (see `.python-version` and `pyproject.toml`).

### Option A — venv + pip

From the repo root:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Option B — uv (if you use uv)

This repo includes a `uv.lock` file.

```powershell
uv sync
```

---

## Run the Streamlit app

From the repo root:

```powershell
streamlit run app/streamlit_app.py
```

If the model file is missing, re-run the model notebook (`04_Model_Building.ipynb`) to regenerate `notebooks/adr_risk_model.pkl`.

---

## Reproduce the analysis

Open and run the notebooks in order:

1. `notebooks/01_Data_Collection.ipynb` (downloads + saves data)
2. `notebooks/02_EDA.ipynb` (EDA)
3. `notebooks/03_Signal_Detection_PRR.ipynb` (PRR)
4. `notebooks/04_Model_Building.ipynb` (train + save model)

Note on paths: the notebooks use relative paths like `../data/...`, so run them with the working directory set to the `notebooks/` folder (VS Code’s Jupyter usually does this automatically).

---

## Notes & limitations

- **FAERS ≠ incidence**: reporting frequency is not the same as real-world risk.
- **Single-drug dataset**: the model is trained only on Doxorubicin reports.
- **Risk_Label is heuristic**: “high risk” is defined as “top-10 most frequent reactions”, not a clinically validated outcome.
- **PRR notebook uses placeholders**: replace the comparator counts (`C`, `D`) with real non-doxorubicin data for meaningful signal detection.

---

## Quick troubleshooting

- `ModuleNotFoundError`: install dependencies from `requirements.txt`.
- Streamlit can’t find the model: run `streamlit run app/streamlit_app.py` from the repo root so `./notebooks/adr_risk_model.pkl` resolves.
