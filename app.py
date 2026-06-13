import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="EduTrack Analytics PRO", page_icon="🎓", layout="wide")

API_URL = "http://127.0.0.1:8000"

st.title("🎓 Système Décisionnel - EduTrack Analytics")
st.markdown("Plateforme d'analyse des performances académiques conforme aux spécifications Ynov.")

# --- NAVIGATION SIDEBAR ---
menu = st.sidebar.selectbox("Navigation", ["Vue Globale & KPIs", "Analyses Spécifiques (Modules & Classes)", "Profils & Segmentation"])

# --- ONGLET 1 : VUE GLOBALE ---
if menu == "Vue Globale & KPIs":
    st.subheader("📊 Indicateurs de Performance Établissement")
    
    try:
        res = requests.get(f"{API_URL}/api/metrics/global").json()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Étudiants", res["total_etudiants"])
        col2.metric("Moyenne Générale", f"{res['moyenne_generale']} / 20")
        col3.metric("Taux de Réussite", f"{res['taux_reussite']}%")
        col4.metric("Volume Absences", res["total_absences"])
    except:
        st.error("Erreur de communication avec l'API Backend.")

    st.markdown("---")
    st.subheader("📉 Analyses des Corrélations & Distributions")
    
    # Récupération des données pour les graphiques
    try:
        corr_data = requests.get(f"{API_URL}/api/analytics/correlation").json()
        df_corr = pd.DataFrame(corr_data)
        
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.markdown("**1. Corrélation : Impact des Absences sur la Moyenne (Nuage de points)**")
            if not df_corr.empty:
                fig1 = px.scatter(df_corr, x="absences", y="moyenne", trendline="ols",
                                  labels={"absences": "Nombre d'absences", "moyenne": "Moyenne / 20"},
                                  template="plotly_white", color_discrete_sequence=['#FF4B4B'])
                st.plotly_chart(fig1, use_container_width=True)
                
        with col_g2:
            st.markdown("**2. Distribution Globale des Notes (Boîte à moustaches)**")
            if not df_corr.empty:
                fig2 = px.box(df_corr, y="moyenne", points="all", 
                              labels={"moyenne": "Notes Générales"}, template="plotly_white")
                st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.info("Ajoutez des données supplémentaires pour générer les graphiques de distribution complexes.")

# --- ONGLET 2 : MODULES & CLASSES ---
elif menu == "Analyses Spécifiques (Modules & Classes)":
    st.subheader("📚 Statistiques Descriptives Obligatoires par Module")
    
    try:
        mod_data = requests.get(f"{API_URL}/api/analytics/modules").json()
        if mod_data:
            df_mod = pd.DataFrame(mod_data)
            
            # Formatage propre pour affichage de la table de données
            st.dataframe(df_mod.style.format({
                "moyenne": "{:.2f}", "mediane": "{:.2f}", 
                "variance": "{:.2f}", "ecart_type": "{:.2f}"
            }), use_container_width=True)
            
            st.markdown("---")
            col_g3, col_g4 = st.columns(2)
            
            with col_g3:
                st.markdown("**3. Comparatif des Moyennes par Module**")
                fig3 = px.bar(df_mod, x="module_id", y="moyenne", color="module_id",
                             labels={"module_id": "Code Module", "moyenne": "Note Moyenne"}, template="plotly_white")
                st.plotly_chart(fig3, use_container_width=True)
                
            with col_g4:
                st.markdown("**4. Dispersion du niveau par Module (Écart-type)**")
                fig4 = px.line(df_mod, x="module_id", y="ecart_type", markers=True,
                              labels={"module_id": "Code Module", "ecart_type": "Écart-type"}, template="plotly_white")
                st.plotly_chart(fig4, use_container_width=True)
        else:
            st.warning("Aucune note enregistrée pour le calcul des indicateurs.")
    except Exception as e:
        st.error(f"Erreur : {e}")

# --- ONGLET 3 : SEGMENTATION & PROFILS ---
elif menu == "Profils & Segmentation":
    st.subheader("👥 Segmentation Algorithmique des Étudiants")
    
    try:
        seg_data = requests.get(f"{API_URL}/api/etudiants/segmentation").json()
        df_seg = pd.DataFrame(seg_data)
        
        if not df_seg.empty:
            # Graphique 5 : Répartition des profils
            st.markdown("**5. Répartition des Groupes d'Étudiants (Segmentation)**")
            segment_counts = df_seg['segment'].value_counts().reset_index()
            segment_counts.columns = ['Segment', 'Nombre']
            
            fig5 = px.pie(segment_counts, values='Nombre', names='Segment', 
                          color_discrete_map={'Excellent':'#2EA043', 'Stable':'#238636', 'Fragile':'#D29922', 'À Risque':'#F85149'},
                          template="plotly_white", hole=0.4)
            st.plotly_chart(fig5, use_container_width=True)
            
            st.markdown("---")
            st.markdown("**Registre Matriculaire Complet et Affectation de Profil**")
            st.dataframe(df_seg[['matricule', 'nom', 'prenom', 'moyenne', 'segment']], use_container_width=True)
    except Exception as e:
        st.error(f"Erreur de segmentation : {e}")