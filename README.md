# Primjena grafovskih neuronskih mreža za predviđanje fizikalno-kemijskih svojstava molekula

## Opis

Primjena GAT (Graph Attention Network) modela za predikciju topljivosti (ESOL dataset) i toksičnosti (Tox21 dataset) molekula. Molekule se predstavljaju kao grafovi gdje su atomi čvorovi, a kemijske veze bridovi.

Web aplikacija omogućuje unos molekularnih struktura (SMILES notacija) i dobivanje predikcija u stvarnom vremenu.

## Tech stack

- **ML:** PyTorch, PyTorch Geometric, RDKit
- **Backend:** FastAPI
- **Frontend:** React (Vite)
- **Dataseti:** MoleculeNet (ESOL, Tox21)

## Struktura projekta

```
backend/
  app/
    main.py          # FastAPI entry point
    models/          # GNN arhitekture i spremljeni modeli
    schemas/         # Pydantic sheme
    utils/           # RDKit, feature extraction, helpers
  notebooks/         # Jupyter/Colab eksperimenti
    01_dataset_analysis.ipynb
    02_data_preparation.ipynb
    03_model_training.ipynb
    04_evaluation.ipynb
  data/              # Dataseti
  tests/             # Testovi
frontend/
  src/               # React aplikacija
```

## Setup

### Backend
```bash
cd backend
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
