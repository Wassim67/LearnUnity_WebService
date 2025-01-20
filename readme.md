# Système d'Utilisateurs et de Commentaires avec Flask


## Fonctionnalités

- **Inscription des utilisateurs** avec mots de passe cryptés. # Pas implémenté sur unity
- **Connexion des utilisateurs** pour vérifier leurs identifiants.
- **Gestion des commentaires** : les utilisateurs peuvent poster des commentaires associés à leurs comptes.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- **Python 3.7** ou une version supérieure.
- **Base de données MySQL**.
- **Pip** (gestionnaire de paquets Python).

## Installation

Suivez les étapes ci-dessous pour installer et configurer l'application sur votre machine locale.

1. **Clonez le dépôt Git** :
   ``
   git clone https://github.com/Wassim67/LearnUnity_WebService``
2. **Créez un environnement virtuel :**

   ``bash
   python -m venv venv``
   
3. **Activez l'environnement virtuel :**
     * ``source venv/bin/activate`` #mac/linux
	 * ``venv\Scripts\activate`` # Windows
	 
4. **Installez les dépendances:**
	 `pip install -r requirements.txt`

5. **Configurez vos variables d'environnement :**
```python
FLASK_APP=main.py
FLASK_ENV=development
DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost
DB_NAME=unityWassim
DATABASE_URL=mysql+pymysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}
```
6 **Démarrer l'application**:

```python
python main.py
```

