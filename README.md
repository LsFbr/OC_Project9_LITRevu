# LITRevu

---

LITRevu est une application web développée avec **Django** permettant à une communauté d’utilisateurs de :

* Publier des critiques de livres ou d’articles
* Demander des critiques via des tickets
* Suivre d’autres utilisateurs pour voir leurs publications
* Consulter un flux personnalisé regroupant tickets et critiques

Le code respecte les conventions PEP8 et l’interface suit les bonnes pratiques d’accessibilité (WCAG)

---

# Installation

## Prérequis

* Python 3.10+
* pip
* git
* SQLite (fourni par défaut avec Python)

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

L'application utilise SQLite par défaut (`db.sqlite3`). Le fichier `db.sqlite3` **n'est pas fourni** et **n'est pas versionné** dans Git. Vous devez donc **initialiser une base vide** avant le premier lancement :

```bash
python manage.py migrate
```

## 6. Site d’administration

Pour gérer les utilisateurs et le contenu via l’interface d’administration de Django, vous devez créer un superutilisateur :

```bash
python manage.py createsuperuser
```

Suivez les instructions (nom d’utilisateur, email, mot de passe), puis lancez le serveur et connectez-vous à :

```
http://127.0.0.1:8000/admin/
```

Depuis cette interface, vous pouvez consulter, créer, modifier ou supprimer les différents modèles de l’application (tickets, critiques, abonnements, utilisateurs, etc.).

---

# Utilisation

## Lancer l’application
Déplacez vous dans le répertoire litrevu :

```bash
cd litrevu
```
Lancez l'application :

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
* **Page Ticket** : publiez un nouveau ticket pour demander une critique sur un livre ou un article, ou modifiez/supprimez vos tickets existants.
* **Page Critique** : rédigez une critique en réponse à un ticket ou créez une critique indépendante. Vous pouvez également modifier ou supprimer vos critiques.
* **Page Abonnements** : recherchez un utilisateur à suivre, affichez la liste de vos abonnements et désabonnez-vous si nécessaire.
* **Vos posts** : visualisez vos propres tickets et critiques regroupés et gérez-les facilement.

---

# Vérification du code avec Flake8

Pour analyser la qualité du code et vérifier la conformité à la PEP8, vous pouvez générer un rapport Flake8.

Générez un rapport HTML :

```bash
flake8 --format=html --htmldir=flake8_report
```

Le rapport sera disponible dans le dossier `flake8_report`.
