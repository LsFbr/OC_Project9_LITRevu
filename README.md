# OC_Project9_LITRevu# LITRevu

---

LITRevu est une application web développée avec **Django** permettant à une communauté d’utilisateurs de :

* Publier des critiques de livres ou d’articles
* Demander des critiques via des tickets
* Suivre d’autres utilisateurs pour voir leurs publications
* Consulter un flux personnalisé regroupant tickets et critiques

---

# Installation

## Prérequis

* Python 3.10+
* pip
* git
* SQLite (fourni par défaut avec Python)
* Navigateur web moderne

---

## 0. Placez-vous dans le répertoire où vous souhaitez cloner le projet

```bash
cd chemin/vers/le/repertoire
```

## 1. Clonez le projet

```bash
git clone https://github.com/<TON_COMPTE>/OC_Project9_LITRevu.git
cd OC_Project9_LITRevu
```

## 2. Créez un environnement virtuel

#### Windows

```bash
python -m venv venv
```

#### Linux / MacOS

```bash
python3 -m venv venv
```

## 3. Activez l’environnement virtuel

#### Windows

```bash
.\venv\Scripts\activate
```

#### Linux / MacOS

```bash
source venv/bin/activate
```

## 4. Installez les dépendances

```bash
pip install -r requirements.txt
```

## 5. Base de données

Une base SQLite est utilisée par défaut (`db.sqlite3`).
Le projet est livré avec des données de test pour évaluer l’application.

Si vous souhaitez repartir d’une base vide :

```bash
python manage.py migrate
```

---

# Utilisation

## Lancer l’application

```bash
python manage.py runserver
```

Accédez à l’application dans votre navigateur à l’adresse :

```
http://127.0.0.1:8000
```

## Guide rapide pour l’utilisateur

* **Page d’accueil / Connexion** : créez un compte ou connectez-vous avec vos identifiants.
* **Page Flux** : consultez les derniers tickets et critiques publiés par vous-même et les utilisateurs que vous suivez. Depuis cette page, vous pouvez accéder rapidement à la création de tickets ou de critiques.
* **Page Abonnements** : recherchez un utilisateur à suivre, affichez la liste de vos abonnements et désabonnez-vous si nécessaire.
* **Vos posts** : visualisez vos propres tickets et critiques regroupés et gérez-les facilement.
