import streamlit as st # type: ignore
import pandas as pd # type: ignore
import matplotlib.pyplot as plt

# Charger les scores enregistrés
@st.cache
def load_data():
    try:
        return pd.read_csv("training_scores.csv")  # Fichier généré après l'entraînement
    except FileNotFoundError:
        return pd.DataFrame({"episode": [], "score": []})  # Retourne un DataFrame vide si pas de fichier

# Interface Streamlit
st.title("📊 Suivi des Performances de l'IA")
st.write("Ce tableau de bord affiche l'évolution du score de l'agent IA.")

# Charger les données
scores = load_data()

if not scores.empty:
    # Graphique d'évolution des scores
    st.subheader("📈 Progression du Score")
    fig, ax = plt.subplots()
    ax.plot(scores["episode"], scores["score"], label="Score par épisode", color="blue")
    ax.set_xlabel("Épisode")
    ax.set_ylabel("Score")
    ax.set_title("Évolution du score de l'agent")
    ax.legend()
    st.pyplot(fig)

    # Affichage des métriques principales
    st.subheader("📊 Statistiques Globales")
    st.metric(label="Meilleur Score", value=scores["score"].max())
    st.metric(label="Score Moyen", value=scores["score"].mean())

else:
    st.write("Aucune donnée d'entraînement disponible. Lancez `main.py` pour générer des scores.")

# Rafraîchissement automatique du tableau de bord toutes les 10 secondes
st.experimental_rerun()
