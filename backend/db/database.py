import sqlite3
import os

# 1. BASE_DIR est maintenant le dossier 'db' (car ton fichier python est dedans)
BASE_DIR = os.path.dirname(__file__)

# 2. On remonte d'un cran pour atteindre le dossier 'backend'
BACKEND_DIR = os.path.dirname(BASE_DIR)

# 3. On crée le dossier 'data' proprement dans 'backend'
DB_DIR = os.path.join(BACKEND_DIR, "data")
DB_PATH = os.path.join(DB_DIR, "edutrack.db")

# 4. schema.sql est dans le même dossier que ce script python
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

def init_db():
    print("Démarrage de l'initialisation de la base de données...")
    
    # Création du dossier 'data'
    os.makedirs(DB_DIR, exist_ok=True)
    
    # Connexion et création du fichier SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Lecture de ton fichier schema.sql
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            schema_script = f.read()
            
        # Exécution du code SQL
        cursor.executescript(schema_script)
        conn.commit()
        print(f"✅ SUCCÈS : Base de données créée avec succès dans : {DB_PATH}")
        
    except FileNotFoundError:
        print(f"❌ ERREUR : Le fichier {SCHEMA_PATH} est introuvable.")
    except Exception as e:
        print(f"❌ ERREUR LORS DE L'EXÉCUTION SQL : {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()