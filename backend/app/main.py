from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="GNN Molecular Property Prediction",
    description="Predikcija fizikalno-kemijskih svojstava molekula pomoću grafovskih neuronskih mreža",
    version="0.1.0",
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
    return {"status": "healthy"}
