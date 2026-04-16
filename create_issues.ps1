gh issue create --title "Analiza ESOL i Tox21 dataseta" --body "Kreirati notebook 01_dataset_analysis.ipynb:

- [ ] Ucitavanje ESOL i Tox21 dataseta (MoleculeNet)
- [ ] Osnovne statistike - broj molekula, broj znacajki po atomu, prosjecan broj atoma/veza po molekuli
- [ ] ESOL: histogram distribucije topljivosti (y vrijednosti)
- [ ] Tox21: balans klasa za svih 12 taskova (koliko toksicnih vs netoksicnih), analiza NaN vrijednosti
- [ ] Vizualizacija 4-5 primjera molekula iz svakog dataseta (RDKit Draw)
- [ ] Kratki opisi dataseta u markdown celijama" --label "notebook"

gh issue create --title "Priprema podataka - SMILES u grafove" --body "Kreirati notebook 02_data_preparation.ipynb:

- [ ] Objasnjenje SMILES notacije s primjerima
- [ ] Prikaz pretvorbe jedne molekule SMILES u graf korak po korak
- [ ] Objasnjenje svih 9 znacajki atoma (x) - sto svaki stupac znaci
- [ ] Objasnjenje edge_index - kako su veze kodirane
- [ ] Objasnjenje edge_attr - tipovi veza
- [ ] Vizualizacija grafa molekule (networkx)
- [ ] Podjela dataseta na train/val/test (80/10/10)
- [ ] Kreiranje DataLoadera" --label "notebook"

gh issue create --title "Implementacija GAT modela i trening na ESOL datasetu" --body "Kreirati notebook 03_model_training.ipynb - ESOL dio:

- [ ] Implementacija GAT modela (GATConv, 3 sloja, multi-head attention, batch norm, dropout)
- [ ] Definicija loss funkcije (MSELoss) i optimizera (Adam)
- [ ] Learning rate scheduler (ReduceLROnPlateau)
- [ ] Early stopping mehanizam
- [ ] Trening petlja s logiranjem train/val loss-a svaku epohu
- [ ] Plot train vs val loss krivulje
- [ ] Spremanje najboljeg modela (torch.save)" --label "model"

gh issue create --title "Trening GAT modela na Tox21 datasetu" --body "U istom notebooku 03_model_training.ipynb - Tox21 dio:

- [ ] Prilagodba modela za multi-label klasifikaciju (12 izlaza)
- [ ] BCEWithLogitsLoss s NaN maskiranjem
- [ ] Trening petlja s early stopping
- [ ] Plot train vs val loss krivulje
- [ ] Spremanje najboljeg modela" --label "model"

gh issue create --title "Evaluacija modela i vizualizacija rezultata" --body "Kreirati notebook 04_evaluation.ipynb:

- [ ] ESOL: izracun RMSE, MAE, R2 na test setu
- [ ] ESOL: scatter plot - predikcija vs stvarna topljivost
- [ ] ESOL: analiza gresaka - 5 molekula s najvecom greskom
- [ ] Tox21: AUC-ROC za svaki od 12 taskova
- [ ] Tox21: prosjecni AUC-ROC
- [ ] Tox21: ROC krivulje za top 3 taska
- [ ] Test predikcije na poznatim molekulama (etanol, kofein, aspirin, glukoza)
- [ ] Tablica sazetak rezultata" --label "notebook"

gh issue create --title "FastAPI backend - predikcijski endpoint" --body "Implementirati FastAPI backend:

- [ ] Pydantic shema za request (SMILES string) i response (predikcije)
- [ ] Utility funkcija: SMILES u PyG graf (from_smiles)
- [ ] Ucitavanje spremljenih GAT modela pri pokretanju servera
- [ ] POST /predict endpoint - prima SMILES, vraca topljivost i toksicnost
- [ ] Validacija SMILES inputa (RDKit provjera)
- [ ] Error handling za neispravne SMILES" --label "backend"

gh issue create --title "React frontend - UI za predikciju" --body "Implementirati React frontend:

- [ ] Inicijalizacija React app-a (Vite)
- [ ] Input polje za SMILES s primjerima
- [ ] Poziv na backend /predict endpoint
- [ ] Prikaz rezultata - topljivost (numericka vrijednost + objasnjenje)
- [ ] Prikaz rezultata - toksicnost (12 taskova, vizualni prikaz)
- [ ] Vizualizacija molekule
- [ ] Responsive dizajn
- [ ] Loading state i error handling" --label "frontend"

gh issue create --title "Integracija i zavrsno testiranje" --body "Povezati sve komponente:

- [ ] End-to-end test: SMILES input u backend u model u frontend prikaz
- [ ] Testirati s raznim molekulama
- [ ] Provjera edge caseova (prazan input, neispravan SMILES, velika molekula)
- [ ] Cleanup koda i komentari
- [ ] Azuriranje README s finalnim uputama za pokretanje" --label "integration"
