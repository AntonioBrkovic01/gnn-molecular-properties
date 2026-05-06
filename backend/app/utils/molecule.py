import torch
from torch_geometric.utils import from_smiles
from rdkit import Chem
import io
import base64

from rdkit.Chem import Draw

TOX21_TASKS = [
    'NR-AR', 'NR-AR-LBD', 'NR-AhR', 'NR-Aromatase',
    'NR-ER', 'NR-ER-LBD', 'NR-PPAR-gamma',
    'SR-ARE', 'SR-ATAD5', 'SR-HSE', 'SR-MMP', 'SR-p53',
]


def is_valid_smiles(smiles: str) -> bool:
    if not smiles or not smiles.strip():
        return False
    mol = Chem.MolFromSmiles(smiles)
    return mol is not None


def smiles_to_graph(smiles: str):
    graph = from_smiles(smiles)
    graph.batch = torch.zeros(graph.x.size(0), dtype=torch.long)
    return graph


def categorize_solubility(log_sol: float) -> str:
    if log_sol >= 0:
        return "Visoko topljivo"
    elif log_sol >= -2:
        return "Topljivo"
    elif log_sol >= -4:
        return "Slabo topljivo"
    else:
        return "Vrlo slabo topljivo"
    
def smiles_to_image_base64(smiles: str, size: int = 400) -> str:
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    img = Draw.MolToImage(mol, size=(size, size))

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"