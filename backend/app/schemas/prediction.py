from pydantic import BaseModel, Field
from typing import List


class PredictionRequest(BaseModel):
    smiles: str = Field(..., description="SMILES notacija molekule", examples=["CCO"])


class ToxicityTask(BaseModel):
    task: str
    probability: float
    is_toxic: bool


class PredictionResponse(BaseModel):
    smiles: str
    valid: bool

    solubility: float = Field(..., description="Predviđena topljivost u log mol/L")
    solubility_category: str

    hydration_energy: float = Field(..., description="Slobodna energija hidracije u kcal/mol")

    lipophilicity: float = Field(..., description="Logaritam particijskog koeficijenta (logD)")
    lipophilicity_category: str

    toxicity_tasks: List[ToxicityTask]
    avg_toxicity_risk: float
    high_risk_count: int


class ErrorResponse(BaseModel):
    detail: str

class ValidationResponse(BaseModel):
    smiles: str
    valid: bool
    message: str


class MoleculeImageResponse(BaseModel):
    smiles: str
    image: str = Field(..., description="Base64-kodirana PNG slika")


class ExampleMolecule(BaseModel):
    name: str
    smiles: str
    description: str


class ExamplesResponse(BaseModel):
    examples: List[ExampleMolecule]