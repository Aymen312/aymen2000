

Un site éducatif en **français**, créé avec **Python et Streamlit**, pour apprendre et
réviser au collège et au lycée. Les niveaux sont indicatifs ; ce premier catalogue
ne remplace pas un programme scolaire officiel complet.

## Ce que propose le site

- **8 cours** : mouvement et vitesse, loi d'Ohm, masse et poids, énergie ; accords,
  conjugaison, compréhension de texte et argumentation.
- **24 exercices** avec indices et corrections expliquées. Les réponses numériques
  et les réponses courtes sont vérifiées automatiquement ; les rédactions proposent
  un modèle à comparer à sa propre réponse.
- **32 questions de quiz**, avec score, explications et possibilité de recommencer.
- **4 outils interactifs de physique**, avec graphiques et hypothèses du modèle.
- Un suivi de progression pendant la session, avec **export et restauration JSON**.
- Des fiches de cours téléchargeables au format Markdown.

## Lancer sur son ordinateur

Python 3.12 est la version testée.

```bash
git clone https://github.com/Aymen312/aymen2000.git
cd aymen2000
python -m venv .venv
```

Activer l'environnement :

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Puis installer et lancer :

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Le site est ensuite accessible à l'adresse locale affichée par Streamlit,
généralement `http://localhost:8501`.
Le dépôt est public : il peut être cloné sans autorisation spéciale.

## Déployer sur Streamlit Community Cloud

1. Ouvrir [Streamlit Community Cloud](https://share.streamlit.io/) et connecter le
   compte GitHub qui a accès au dépôt. Pour un dépôt privé, donner à Streamlit
   l'accès nécessaire au dépôt.
2. Choisir **Create app**, puis renseigner :

   | Champ | Valeur |
   | --- | --- |
   | Repository | `Aymen312/aymen2000` |
   | Branch | `main` |
   | Main file path | `streamlit_app.py` |
   | Python version, dans Advanced settings | `3.12` |

3. Cliquer sur **Deploy**. `requirements.txt` et `.streamlit/config.toml` sont déjà
   présents. L'application ne nécessite aucune clé API ni secret.
4. Streamlit fournit l'URL du site après le déploiement. Vérifier les paramètres de
   partage avant de transmettre cette URL aux élèves.

Voir la [documentation officielle de déploiement](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

## Modifier les ressources

- `curriculum.py` : leçons, objectifs, exemples, exercices et quiz.
- `streamlit_app.py` : pages et interactions du site.
- `learning.py` : vérification des réponses et validation des sauvegardes.
- `assets/style.css` : couleurs, typographie et mise en page responsive.
- `assets/learning.svg` : illustration originale de la page d'accueil.
- `.streamlit/config.toml` : thème et configuration Streamlit.

Pour ajouter un cours, créer une entrée dans `LESSONS` avec un identifiant unique.
Chaque question de quiz indique ses choix, sa bonne réponse et une explication.
Les exercices sont de type `numeric`, `text` ou `written`.

## Progression et confidentialité

Il n'y a pas de compte élève ni de base de données. La progression reste dans
`st.session_state` : elle peut disparaître à la fermeture de la session ou au
redémarrage du serveur. Télécharger le fichier JSON depuis **Ma progression**,
puis le réimporter lors d'une nouvelle session pour la restaurer. L'import remplace
la progression actuelle. Les services d'hébergement peuvent produire leurs propres
journaux techniques.

## Vérifier le projet

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Les tests couvrent les parcours Streamlit, les quiz incomplets et corrigés, les
réponses aux exercices, les calculs du laboratoire et les sauvegardes de progression.
Un workflow GitHub Actions exécute ces tests à chaque push et pull request.
