import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ⚙️ CONFIGURATION (Plus de CSS ici, le config.toml gère tout !)
st.set_page_config(page_title="Dashboard Titanic - TP5", page_icon="🚢", layout="wide")

# 💾 CHARGEMENT DES DONNÉES
@st.cache_data
def load_data():
    df = sns.load_dataset('titanic')
    df['mortalite_pct'] = (1 - df['survived']) * 100
    df['taille_famille'] = df['sibsp'] + df['parch'] + 1
    df['age'] = df['age'].fillna(df['age'].median())
    return df

df = load_data()

# 🎛️ SIDEBAR (Filtres globaux)
st.sidebar.markdown("<div style='text-align: center; font-size: 80px;'>🚢</div>", unsafe_allow_html=True)
st.sidebar.title("Filtres d'Analyse")

sexe_filtre = st.sidebar.multiselect("Genre", options=df['sex'].unique(), default=df['sex'].unique())
classe_filtre = st.sidebar.multiselect("Classe Sociale", options=sorted(df['pclass'].unique()), default=sorted(df['pclass'].unique()))
age_min, age_max = st.sidebar.slider("Tranche d'âge", int(df['age'].min()), int(df['age'].max()), (0, 80))

df_filtre = df[
    (df['sex'].isin(sexe_filtre)) & 
    (df['pclass'].isin(classe_filtre)) & 
    (df['age'] >= age_min) & (df['age'] <= age_max)
]

# 🖼️ TITRE PRINCIPAL
st.title("🧊 Le Naufrage du RMS Titanic")
st.markdown("### *Analyse des protocoles d'évacuation d'urgence (TP5)*")
st.markdown("---")

if df_filtre.empty:
    st.error("⚠️ Veuillez ajuster vos filtres, aucune donnée ne correspond.")
else:
    # 📈 CRÉATION DES 3 ONGLETS (1 par Visualisation, selon la consigne)
    tab1, tab2, tab3 = st.tabs(["🎫 Acte 1 : Inégalité de Classe", "🚻 Acte 2 : Le Fossé du Genre", "👨‍👩‍👧 Acte 3 : L'Effet Famille"])
    
    # --- ONGLET 1 : LA CLASSE SOCIALE ---
    with tab1:
        st.subheader("La 3ème classe : un taux de perte inacceptable")
        
        # Les 3 KPIs Actionnables pour la classe
        c1, c2, c3 = st.columns(3)
        survie_1ere = df_filtre[df_filtre['pclass'] == 1]['survived'].mean() * 100 if not df_filtre[df_filtre['pclass'] == 1].empty else 0
        perte_3eme = df_filtre[df_filtre['pclass'] == 3]['mortalite_pct'].mean() if not df_filtre[df_filtre['pclass'] == 3].empty else 0
        ecart_social = survie_1ere - (100 - perte_3eme)
        
        c1.metric("Taux de survie (1ère Classe)", f"{survie_1ere:.1f}%", help="Action : Définir ce taux comme standard minimum d'évacuation.")
        c2.metric("Taux de perte (3ème Classe)", f"{perte_3eme:.1f}%", help="Action : Auditer les voies de secours des ponts inférieurs.")
        c3.metric("Différentiel Social de Survie", f"{ecart_social:.1f} pts", help="Action : KPI à réduire à 0 pour garantir l'équité.")
        
        # Graphique Interactif (Matplotlib filtré par Streamlit)
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        fig1.patch.set_facecolor('#0B1D3A')
        ax1.set_facecolor('#0B1D3A')
        
        sns.barplot(data=df_filtre, x='pclass', y='mortalite_pct', errorbar=None, palette=['#E74C3C', '#BDC3C7', '#BDC3C7'], ax=ax1)
        ax1.tick_params(colors='white')
        ax1.set_ylabel("Mortalité (%)", color='white')
        for spine in ax1.spines.values(): spine.set_visible(False)
        st.pyplot(fig1)

    # --- ONGLET 2 : LE GENRE ---
    with tab2:
        st.subheader("\"Les femmes et les enfants d'abord\" : un code fatal pour les hommes")
        
        # Les 3 KPIs Actionnables pour le genre
        c1, c2, c3 = st.columns(3)
        survie_femmes = df_filtre[df_filtre['sex'] == 'female']['survived'].mean() * 100 if not df_filtre[df_filtre['sex'] == 'female'].empty else 0
        survie_hommes = df_filtre[df_filtre['sex'] == 'male']['survived'].mean() * 100 if not df_filtre[df_filtre['sex'] == 'male'].empty else 0
        gap_genre = survie_femmes - survie_hommes
        
        c1.metric("Taux d'accès canots (Femmes)", f"{survie_femmes:.1f}%", help="Action : Évaluer le succès de la consigne maritime.")
        c2.metric("Taux d'accès canots (Hommes)", f"{survie_hommes:.1f}%", help="Action : Identifier le besoin en canots supplémentaires.")
        c3.metric("Fossé de Survie (Genre)", f"{gap_genre:.1f} pts", help="Action : Mesurer la sévérité du filtrage à l'embarquement.")
        
        # Graphique Interactif
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        fig2.patch.set_facecolor('#0B1D3A')
        ax2.set_facecolor('#0B1D3A')
        
        sns.barplot(data=df_filtre, y='sex', x='mortalite_pct', errorbar=None, palette=['#BDC3C7', '#E74C3C'], ax=ax2)
        ax2.tick_params(colors='white')
        ax2.set_ylabel("", color='white')
        ax2.set_xlabel("Mortalité (%)", color='white')
        for spine in ax2.spines.values(): spine.set_visible(False)
        st.pyplot(fig2)

    # --- ONGLET 3 : LA FAMILLE & L'ÂGE ---
    with tab3:
        st.subheader("Les groupes de taille moyenne ont mieux organisé leur évacuation")
        
        # Les 3 KPIs Actionnables pour la famille
        c1, c2, c3 = st.columns(3)
        survie_enfants = df_filtre[df_filtre['age'] < 16]['survived'].mean() * 100 if not df_filtre[df_filtre['age'] < 16].empty else 0
        taille_famille_opt = df_filtre.groupby('taille_famille')['survived'].mean().idxmax() if not df_filtre.empty else 0
        survie_isoles = df_filtre[df_filtre['taille_famille'] == 1]['survived'].mean() * 100 if not df_filtre[df_filtre['taille_famille'] == 1].empty else 0
        
        c1.metric("Taux de survie (Enfants <16ans)", f"{survie_enfants:.1f}%", help="Action : Analyser la vulnérabilité des mineurs.")
        c2.metric("Survie des passagers isolés", f"{survie_isoles:.1f}%", help="Action : Créer des points de ralliement pour personnes seules.")
        c3.metric("Taille famille optimale (Survie)", f"{taille_famille_opt} pers.", help="Action : Définir la capacité optimale des groupes d'évacuation.")
        
        # Graphique Interactif
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        fig3.patch.set_facecolor('#0B1D3A')
        ax3.set_facecolor('#0B1D3A')
        
        sns.lineplot(data=df_filtre, x='taille_famille', y='survived', color='#F1C40F', marker='o', ax=ax3)
        ax3.tick_params(colors='white')
        ax3.set_ylabel("Taux de survie", color='white')
        ax3.set_xlabel("Taille de la Famille", color='white')
        for spine in ax3.spines.values(): spine.set_visible(False)
        st.pyplot(fig3) 