from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import pandas as pd
import numpy as np

app = FastAPI(title="EduTrack Analytics API Pro", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "edutrack.db")

def get_db_conn():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Base de données introuvable.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def home():
    return {"status": "En ligne", "version": "2.0.0"}

@app.get("/api/metrics/global")
def get_global_metrics():
    try:
        conn = get_db_conn()
        cursor = conn.cursor()
        total_etudiants = cursor.execute("SELECT COUNT(*) FROM etudiants").fetchone()[0]
        moyenne_classe = cursor.execute("SELECT AVG(valeur) FROM notes").fetchone()[0]
        total_absences = cursor.execute("SELECT COUNT(*) FROM absences").fetchone()[0]
        
        df_notes = pd.read_sql_query("SELECT etudiant_id, AVG(valeur) as moy FROM notes GROUP BY etudiant_id", conn)
        taux_reussite = (df_notes['moy'] >= 10).mean() * 100 if not df_notes.empty else 0.0
        
        conn.close()
        return {
            "total_etudiants": total_etudiants,
            "moyenne_generale": round(moyenne_classe, 2) if moyenne_classe else 0.0,
            "total_absences": total_absences,
            "taux_reussite": round(taux_reussite, 1)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/modules")
def get_modules_analytics():
    try:
        conn = get_db_conn()
        df = pd.read_sql_query("SELECT module_id, valeur FROM notes", conn)
        conn.close()
        if df.empty:
            return []
        stats = df.groupby('module_id')['valeur'].agg([
            ('moyenne', 'mean'), ('mediane', 'median'),
            ('minimum', 'min'), ('maximum', 'max'),
            ('variance', lambda x: float(np.var(x))), ('ecart_type', 'std')
        ]).reset_index().fillna(0)
        return stats.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/correlation")
def get_correlation_data():
    try:
        conn = get_db_conn()
        df_notes = pd.read_sql_query("SELECT etudiant_id, AVG(valeur) as moyenne FROM notes GROUP BY etudiant_id", conn)
        df_abs = pd.read_sql_query("SELECT etudiant_id, COUNT(*) as absences FROM absences GROUP BY etudiant_id", conn)
        conn.close()
        df_merged = pd.merge(df_notes, df_abs, on='etudiant_id', how='outer').fillna(0)
        return df_merged.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/etudiants/segmentation")
def get_student_segmentation():
    try:
        conn = get_db_conn()
        query = """
            SELECT e.id, e.matricule, e.nom, e.prenom, AVG(n.valeur) as moyenne
            FROM etudiants e
            LEFT JOIN notes n ON e.id = n.etudiant_id
            GROUP BY e.id
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        def assign_segment(row):
            moy = row['moyenne']
            if pd.isna(moy): return "Non évalué"
            if moy >= 16: return "Excellent"
            elif moy >= 12: return "Stable"
            elif moy >= 10: return "Fragile"
            else: return "À Risque"
            
        df['segment'] = df.apply(assign_segment, axis=1)
        return df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))