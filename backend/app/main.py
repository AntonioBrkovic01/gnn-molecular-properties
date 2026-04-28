from contextlib import asynccontextmanager
from pathlib import Path

import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models.gcn import GCN
from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
    ToxicityTask,
)
from app.utils.molecule import (
    TOX21_TASKS,
    is_valid_smiles,
    smiles_to_graph,
    categorize_solubility,
)


# Globalni state - modeli se učitavaju jednom pri startu servera
ml_models = {}

MODELS_DIR = Path(__file__).parent / "models"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Učitaj modele pri startu, otpusti pri gašenju."""
    print("Učitavanje modela...")

    # ESOL model (regresija)
    esol_model = GCN(num_features=9, hidden_dim=128, num_tasks=1)
    esol_model.load_state_dict(torch.load(MODELS_DIR / "gcn_esol.pt", weights_only=True))
    esol_model.eval()
    ml_models["esol"] = esol_model

    # Tox21 model (klasifikacija)
    tox_model = GCN(num_features=9, hidden_dim=128, num_tasks=12)
    tox_model.load_state_dict(torch.load(MODELS_DIR / "gcn_tox21.pt", weights_only=True))
    tox_model.eval()
    ml_models["tox21"] = tox_model

    print("Modeli učitani!")
    yield

    ml_models.clear()


app = FastAPI(
    title="GNN Molecular Property Prediction",
    description="Predikcija fizikalno-kemijskih svojstava molekula pomoću grafovskih neuronskih mreža",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "GNN Molecular Property Prediction API"}


@app.get("/health")
def health():
    return {"status": "healthy", "models_loaded": list(ml_models.keys())}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """Predvidi topljivost i toksičnost za zadanu SMILES molekulu."""
    smiles = request.smiles.strip()

    # Validacija
    if not is_valid_smiles(smiles):
        raise HTTPException(status_code=400, detail=f"Neispravan SMILES: '{smiles}'")

    try:
        # Pretvori u graf
        graph = smiles_to_graph(smiles)

        # Predikcija topljivosti (ESOL)
        with torch.no_grad():
            solubility = ml_models["esol"](graph).item()

            # Predikcija toksičnosti (Tox21) - sigmoid daje vjerojatnosti
            tox_logits = ml_models["tox21"](graph)
            tox_probs = torch.sigmoid(tox_logits).squeeze().numpy()

        # Sastavi rezultate toksičnosti
        toxicity_tasks = [
            ToxicityTask(
                task=task_name,
                probability=float(prob),
                is_toxic=bool(prob > 0.5),
            )
            for task_name, prob in zip(TOX21_TASKS, tox_probs)
        ]

        return PredictionResponse(
            smiles=smiles,
            valid=True,
            solubility=round(solubility, 4),
            solubility_category=categorize_solubility(solubility),
            toxicity_tasks=toxicity_tasks,
            avg_toxicity_risk=round(float(tox_probs.mean()), 4),
            high_risk_count=int((tox_probs > 0.5).sum()),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Greška pri predikciji: {str(e)}")