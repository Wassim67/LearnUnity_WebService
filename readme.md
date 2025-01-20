Système d'Utilisateurs et de Commentaires avec Flask

Cette application basée sur Flask permet aux utilisateurs de s'inscrire, de se connecter et de poster des commentaires.

Fonctionnalités
* Inscription des utilisateurs avec des mots de passe cryptés.
* Connexion des utilisateurs pour vérifier leurs identifiants.
* Les utilisateurs peuvent poster des commentaires liés à leurs comptes.

Prérequis
* Python 3.7 ou version supérieure
* Base de données MySQL
* Pip (gestionnaire de paquets Python)

Installation

* Clonez ce dépôt : git clone https://github.com/Wassim67/LearnUnity_WebService

* Créez un environnement virtuel : python -m venv venv
source venv/bin/activate   # Sur Windows : venv\Scripts\activate

* Installez les dépendances : pip install -r requirements.txt

* Configurez vos variables d'environnement : 
 - Créez un fichier .env à la racine du projet.
  
FLASK_APP=main.py
FLASK_ENV=development
DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost
DB_NAME=unityWassim
DATABASE_URL=mysql+pymysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}


* Demarrer l'application : python main.py


L'application unity est prête à être utilisé.