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
    ValidationResponse,
    MoleculeImageResponse,
    ExampleMolecule,
    ExamplesResponse,
)
from app.utils.molecule import (
    TOX21_TASKS,
    is_valid_smiles,
    smiles_to_graph,
    categorize_solubility,
    smiles_to_image_base64,
)

ml_models = {}

MODELS_DIR = Path(__file__).parent / "models"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Učitavanje modela...")

    esol_model = GCN(num_features=9, hidden_dim=128, num_tasks=1)
    esol_model.load_state_dict(torch.load(MODELS_DIR / "gcn_esol.pt", weights_only=True))
    esol_model.eval()
    ml_models["esol"] = esol_model

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
    smiles = request.smiles.strip()

    if not is_valid_smiles(smiles):
        raise HTTPException(status_code=400, detail=f"Neispravan SMILES: '{smiles}'")

    try:
        graph = smiles_to_graph(smiles)

        with torch.no_grad():
            solubility = ml_models["esol"](graph).item()

            tox_logits = ml_models["tox21"](graph)
            tox_probs = torch.sigmoid(tox_logits).squeeze().numpy()

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
    
@app.post("/validate", response_model=ValidationResponse)
def validate(request: PredictionRequest):
    smiles = request.smiles.strip()
    valid = is_valid_smiles(smiles)
    return ValidationResponse(
        smiles=smiles,
        valid=valid,
        message="SMILES je ispravan" if valid else "Neispravan SMILES",
    )


@app.post("/molecule-image", response_model=MoleculeImageResponse)
def molecule_image(request: PredictionRequest):
    smiles = request.smiles.strip()

    if not is_valid_smiles(smiles):
        raise HTTPException(status_code=400, detail=f"Neispravan SMILES: '{smiles}'")

    image = smiles_to_image_base64(smiles)
    return MoleculeImageResponse(smiles=smiles, image=image)


@app.get("/examples", response_model=ExamplesResponse)
def examples():
    examples_list = [
        ExampleMolecule(name="Voda", smiles="O", description="Najjednostavnija molekula"),
        ExampleMolecule(name="Etanol", smiles="CCO", description="Alkohol u pićima"),
        ExampleMolecule(name="Kofein", smiles="CN1C=NC2=C1C(=O)N(C(=O)N2C)C", description="Stimulans u kavi i čaju"),
        ExampleMolecule(name="Aspirin", smiles="CC(=O)OC1=CC=CC=C1C(=O)O", description="Lijek protiv boli i upale"),
        ExampleMolecule(name="Glukoza", smiles="OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O", description="Šećer u krvi"),
        ExampleMolecule(name="Paracetamol", smiles="CC(=O)NC1=CC=C(O)C=C1", description="Lijek protiv bolova"),
        ExampleMolecule(name="Nikotin", smiles="CN1CCCC1c1cccnc1", description="Spoj u duhanu"),
        ExampleMolecule(name="Heksan", smiles="CCCCCC", description="Lipofilni ugljikovodik"),
    ]
    return ExamplesResponse(examples=examples_list)