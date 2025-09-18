# LITRevu

---

LITRevu est une application web développée avec **Django** permettant à une communauté d’utilisateurs de :

* Publier des critiques de livres ou d’articles
* Demander des critiques via des tickets
* Suivre d’autres utilisateurs pour voir leurs publications
* Consulter un flux personnalisé regroupant tickets et critiques

Le code respecte les conventions PEP8 et l’interface suit les bonnes pratiques d’accessibilité (WCAG)

---

# Installation et utilisation avec la base fournie

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
git clone https://github.com/LsFbr/OC_Project9_LITRevu.git
cd OC_Project9_LITRevu
```

## 2. Créez et activez un environnement virtuel

#### Windows

```bash
python -m venv venv
.\venv\Scripts\activate
```

#### Linux / MacOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Installez les dépendances

```bash
pip install -r requirements.txt
```

## 4. Lancer l’application avec la base fournie

Le fichier `db.sqlite3` est déjà inclus dans le projet et contient des données de test. Vous pouvez directement démarrer l’application :

Placez-vous dans le répertoire litrevu :

```bash
cd litrevu
```

Lancez l'application :

```bash
python manage.py runserver
```

Puis ouvrez votre navigateur à l’adresse :

```
http://127.0.0.1:8000
```

### Identifiants de test

* **Utilisateur standard**
  * Identifiant : `SerialReader`
  * Mot de passe : `read`

* **Superutilisateur (accès admin)**
  * Identifiant : `admin`
  * Mot de passe : `admin`

  Le super utilisateur permet l'accès à l'interface d'administration de l'application à l'adresse : [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

# Guide rapide pour l’utilisateur

* **Page d’accueil / Connexion** : connectez-vous avec les identifiants fournis ou créez un nouveau compte.
* **Flux** : consultez les derniers tickets et critiques publiés par vous-même et les utilisateurs que vous suivez.
* **Tickets** : publiez un nouveau ticket pour demander une critique, ou modifiez/supprimez vos tickets existants.
* **Critiques** : rédigez une critique en réponse à un ticket ou créez une critique indépendante.
* **Abonnements** : recherchez un utilisateur à suivre, affichez vos abonnements et désabonnez-vous si nécessaire.
* **Vos posts** : visualisez vos propres tickets et critiques regroupés.

---

# (Optionnel) Initialiser une base de données vide

Si vous souhaitez repartir de zéro :

1. Supprimez le fichier `db.sqlite3` fourni.
2. Appliquez les migrations :

```bash
python manage.py migrate
```

3. Créez un superutilisateur :

```bash
python manage.py createsuperuser
```

4. Lancez le serveur et connectez-vous avec ce compte.

---

# Vérification du code avec Flake8

Pour analyser la qualité du code et vérifier la conformité à la PEP8 :

```bash
flake8 --format=html --htmldir=flake8_report
```

Le rapport sera disponible dans le dossier `flake8_report`.
