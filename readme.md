# 🏆 GAIP : Game AI Platform  
**Plateforme d'entraînement d'agents IA sur plusieurs jeux**  

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Status](https://img.shields.io/badge/Status-Active-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 Description  
Game AI Platform est une plateforme généralisée permettant de créer, entraîner et tester des agents d'IA sur plusieurs jeux (Snake, Pong…). Grâce à une architecture modulaire et une gestion dynamique des modèles et des environnements, la plateforme est facilement extensible à de nouveaux jeux et modèles.  

---

## 🎯 **Objectifs**  
✅ Entraîner plusieurs types d'agents IA (Q-Learning, DQN...)  
✅ Facilité d'ajout de nouveaux jeux/environnements  
✅ Interaction en temps réel via WebSocket  
✅ Architecture flexible et découplée  

---

## 🏗️ **Structure du Projet**  
📂 **agents/** → Gestion des agents d'IA  
📂 **models/** → Gestion des modèles (Q-Learning, DQN…)  
📂 **games/** → Environnements de jeu (Snake...)  
📂 **backend/** → Serveur WebSocket  
📂 **frontend/** → Interface utilisateur (HTML, JS, CSS)  
📂 **config/** → Fichiers de configuration  
📂 **data/** → Sauvegarde des résultats  
📂 **tests/** → Tests unitaires et d’intégration  

---

## 🌍 **Installation**  
### 1. Cloner le projet :  
```bash
git clone https://github.com/HatimMano/game-ai-platform.git
cd game-ai-platform
```

### 2. Créer un environnement virtuel :  
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances :  
```bash
pip install -r requirements.txt
```

---

## 🏆 **Exécution**  
### ➡️ **Lancer le serveur**  
```bash
python main.py --serve
```

### ➡️ **Lancer l'entraînement**  
```bash
python main.py --train
```

### ➡️ **Tester une partie**  
```bash
python main.py --test
```

### ➡️ **Ouvrir le client**  
- Double-cliquer sur `frontend/index.html`  
- Ou lancer via Streamlit :  
```bash
streamlit run frontend/dashboard.py
```

---

## 🧠 **Fonctionnalités**  
✅ Entraînement en temps réel  
✅ Prédiction automatisée basée sur le modèle  
✅ Sauvegarde et chargement dynamique des modèles  
✅ Gestion centralisée des paramètres dans `settings.py`  
✅ État généralisé avec `to_tensor()`  

---

## 💡 **Ajouter un Nouveau Jeu ou Modèle**  
1. Créer un nouvel environnement dans `games/`  
2. Créer un nouvel agent dans `agents/`  
3. Créer un modèle associé dans `models/`  
4. Définir le comportement dans `settings.py`  
5. Lancer le serveur → Prêt à fonctionner !  

---

## 🛠️ **Tests**  
👉 Lancer les tests unitaires :  
```bash
pytest tests/
```

---

## 🎯 **Améliorations à venir**  
- ✅ Implémenter DQN  
- ✅ Ajouter Pong et d'autres jeux  
- ✅ Ajouter une visualisation des résultats  

---

## 📄 **Licence**  
Ce projet est sous licence MIT — libre d'utilisation, modification et distribution.  

---

👨‍💻 **Développé par Hatim Mano**  
➡️ [https://github.com/HatimMano](https://github.com/HatimMano)  
```

---
