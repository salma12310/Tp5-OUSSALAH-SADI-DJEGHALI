# 🚢 Dashboard Titanic - TP5 Dataviz

Ce projet est un dashboard interactif développé avec **Streamlit** pour la validation du TP5 du module d'Analyse Exploratoire de Données et Dataviz. 

L'objectif de cette application est de restituer une analyse orientée prise de décision en appliquant la structure exigée par le TP5 : un titre percutant, des KPIs d'aide à la décision, et une navigation structurée en onglets.

---

##  Conformité aux attentes du TP5

* **Structure par onglets :** Le dashboard est divisé en 3 onglets distincts, correspondant chacun à l'une de nos 3 visualisations (Acte 1, Acte 2, Acte 3).
* **Principe de Minto :** Chaque graphique est précédé d'un titre formulant une conclusion claire et directe.
* **KPIs Actionnables :** Chaque onglet présente exactement **3 KPIs actionnables** (et non de simples "vanity metrics"). Ils ont été pensés pour auditer les protocoles de sécurité maritimes.
* **Fichier de configuration :** Le design "Nuit Océanique" (couleurs, polices) est géré proprement via un fichier `config.toml` placé dans un dossier `.streamlit` à la racine.

---

## 📂 Arborescence du projet

```text
📁 Tp5-OUSSALAH-SADI-DJEGHALI/
├── 📄 app.py               # Script principal du dashboard Streamlit
├── 📄 README.md            # Documentation du projet 
└── 📁 .streamlit/
    └── ⚙️ config.toml      # Fichier de configuration du thème visuel


 Installation et Exécution
Les données du Titanic sont chargées automatiquement via la librairie seaborn. Aucun fichier CSV n'a besoin d'être téléchargé manuellement.

**1. Installer les dépendances :**
Ouvrez votre terminal et exécutez la commande suivante :

```bash
pip install streamlit pandas seaborn matplotlib

streamlit run app.py 
