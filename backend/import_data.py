import pandas as pd
import sqlite3
import os

# 1. Configuration des chemins (simplifiée car le fichier est dans 'backend')
BASE_DIR = os.path.dirname(__file__) # C'est le dossier 'backend'
DATA_DIR = os.path.join(BASE_DIR, "data") # C'est le dossier 'backend/data'
DB_PATH = os.path.join(DATA_DIR, "edutrack.db")

def importer_csv(fichier_nom, table_name):
    """Importe un fichier CSV dans la base de données après nettoyage."""
    fichier_path = os.path.join(DATA_DIR, fichier_nom)
    
    try:
        # Vérifier si le fichier existe
        if not os.path.exists(fichier_path):
            print(f"⚠️ Le fichier {fichier_nom} est introuvable dans {DATA_DIR}")
            return

        # Lecture du fichier avec Pandas
        df = pd.read_csv(fichier_path)
        
        # Nettoyage automatique de base
        df.columns = df.columns.str.strip().str.lower()
        df = df.drop_duplicates()
        
        # Connexion à SQLite et insertion
        conn = sqlite3.connect(DB_PATH)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.close()
        
        print(f"✅ Succès : {len(df)} lignes importées depuis {fichier_nom} dans la table '{table_name}'")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'import de {fichier_nom} : {e}")

if __name__ == "__main__":
    print("🚀 Démarrage du pipeline d'importation des données...")
    
    importer_csv('etudiants.csv', 'etudiants')
    importer_csv('notes.csv', 'notes')
    importer_csv('absences.csv', 'absences')
    
    print("🎉 Importation terminée ! La base de données est prête et remplie.")