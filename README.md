# Primjena grafovskih neuronskih mreža za predviđanje fizikalno-kemijskih svojstava molekula

## Opis

Primjena GAT (Graph Attention Network) modela za predikciju topljivosti (ESOL dataset) i toksičnosti (Tox21 dataset) molekula. Molekule se predstavljaju kao grafovi gdje su atomi čvorovi, a kemijske veze bridovi.

Web aplikacija omogućuje unos molekularnih struktura (SMILES notacija) i dobivanje predikcija u stvarnom vremenu.

## Tech stack

- **ML:** PyTorch, PyTorch Geometric, RDKit
- **Backend:** FastAPI
- **Frontend:** React (Vite)
- **Dataseti:** MoleculeNet (ESOL, Tox21)
