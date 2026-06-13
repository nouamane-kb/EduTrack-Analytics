import pandas as pd
import os
import random

# On crée le dossier 'data' si besoin
data_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(data_dir, exist_ok=True)

# 1. Génération des étudiants
etudiants = pd.DataFrame({
    'matricule': [f'E00{i}' for i in range(1, 6)],
    'nom': ['Dupont', 'Martin', 'Lefebvre', 'Petit', 'Garcia'],
    'prenom': ['Jean', 'Marie', 'Luc', 'Sophie', 'Pierre'],
    'classe_id': [1, 1, 2, 2, 1]
})
etudiants.to_csv(os.path.join(data_dir, 'etudiants.csv'), index=False)

# 2. Génération des notes
notes = pd.DataFrame({
    'etudiant_id': [1, 2, 3, 4, 5],
    'module_id': [1, 1, 2, 2, 3],
    'valeur': [14.5, 12.0, 16.0, 08.5, 11.0],
    'date_evaluation': ['2026-05-10', '2026-05-10', '2026-05-11', '2026-05-11', '2026-05-12']
})
notes.to_csv(os.path.join(data_dir, 'notes.csv'), index=False)

# 3. Génération des absences
absences = pd.DataFrame({
    'etudiant_id': [1, 3, 5],
    'date_absence': ['2026-05-15', '2026-05-16', '2026-05-17'],
    'justifiee': [1, 0, 1]
})
absences.to_csv(os.path.join(data_dir, 'absences.csv'), index=False)

print("✅ SUCCÈS : Tes fichiers CSV de test ont été créés dans le dossier 'data' !")