from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
CORS(app)
# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)

# Modèle pour les utilisateurs
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'

    def to_dict(self):
        return {
            'id': self.id,
            'login': self.login
        }

class Commentaire(db.Model):
    id_commentaire	 = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    commentaire = db.Column(db.String(500), nullable=False)  

    user = db.relationship('User', backref=db.backref('commentaires', lazy=True)) 

    def __repr__(self):
        return f'<Commentaire {self.commentaire}>'


# Route de test
@app.route('/')
def home():
    """
    Route de test pour vérifier la connexion à la base de données.
    """
    return "Connexion à la base de données réussie !"

# Route pour récupérer tous les utilisateurs
@app.route('/users', methods=['GET'])
def get_users():
    """
    Route pour récupérer la liste de tous les utilisateurs.
    Retourne une liste des utilisateurs au format JSON.
    """
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def validate_json(data, required_fields):
    """
    Valide les champs requis dans les données JSON.

    :param data: Les données JSON extraites de la requête.
    :param required_fields: Liste des champs requis.
    :return: Tuple (is_valid, message). is_valid est un booléen, message est un texte en cas d'erreur.
    """
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return False, f"Les champs suivants sont requis : {', '.join(missing_fields)}"
    return True, None


@app.route('/register', methods=['POST'])
def add_user():
    """
    Route pour ajouter un nouvel utilisateur à la base de données.
    Reçoit un JSON contenant le login et le mot de passe.
    """
    try:
        # Récupérer les données JSON
        data = request.get_json()

        # Valider les champs requis
        is_valid, error_message = validate_json(data, ['login', 'password'])
        if not is_valid:
            return jsonify({'error': error_message}), 400

        # Extraire les champs
        login = data['login']
        password = data['password']

        # Vérifier si le login existe déjà
        existing_user = User.query.filter_by(login=login).first()
        if existing_user:
            return jsonify({'error': 'Cet identifiant est déjà utilisé. Veuillez en choisir un autre.'}), 409

        # Hasher le mot de passe
        hashed_password = generate_password_hash(password)

        # Créer un nouvel utilisateur
        new_user = User(login=login, password=hashed_password)

        # Ajouter l'utilisateur à la base de données
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Utilisateur ajouté avec succès'}), 201
    except Exception as e:
        # En cas d'erreur, annuler la transaction
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    """
    Route pour permettre à un utilisateur de se connecter.
    Vérifie les identifiants (login et mot de passe).
    """
    try:
        # Récupérer les données JSON
        data = request.get_json()

        # Valider les champs requis
        is_valid, error_message = validate_json(data, ['login', 'password'])
        if not is_valid:
            return jsonify({'status': 'error', 'message': error_message}), 400

        # Extraire les champs
        login = data['login']
        password = data['password']

        # Vérifier les identifiants
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            # Connexion réussie, renvoyer le statut et l'ID utilisateur
            return jsonify({'status': 'success', 'id_user': user.id}), 200
        else:
            # Identifiants incorrects
            return jsonify({'status': 'error', 'message': 'Identifiants incorrects'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500



# Route pour ajouter un commentaire
@app.route('/addComment', methods=['POST'])
def add_comment():
    """
    Route pour ajouter un commentaire à un utilisateur.
    Reçoit un JSON contenant l'id_user et le commentaire.
    """
    try:
        # Récupérer les données JSON envoyées dans la requête
        data = request.get_json()

        id_user = data.get('id_user')  
        commentaire = data.get('commentaire')  


        if not id_user or not commentaire:
            return jsonify({'error': 'id_user et commentaire sont requis'}), 400

        new_comment = Commentaire(id_user=id_user, commentaire=commentaire)

        db.session.add(new_comment)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Commentaire crée avec succès !'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

@app.route('/getCommentCount', methods=['POST'])
def get_comment_count():
    """
    Route pour récupérer le nombre de commentaires d'un utilisateur.
    Reçoit un JSON contenant l'id_user.
    """
    try:
        # Récupérer les données JSON envoyées dans le corps de la requête
        data = request.get_json()

        # Vérifier que id_user est présent dans les données
        id_user = data.get('id_user')
        if not id_user:
            return jsonify({'status': 'error', 'message': 'id_user est requis'}), 400

        # Vérifier si l'utilisateur existe
        user = User.query.get(id_user)
        if not user:
            return jsonify({'status': 'error', 'message': 'Utilisateur non trouvé'}), 404

        # Compter le nombre de commentaires de l'utilisateur
        comment_count = Commentaire.query.filter_by(id_user=id_user).count()

        # Retourner le nombre de commentaires
        return jsonify({'status': 'success', 'comment_count': comment_count}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Route pour récupérer tous les commentaires de tous les utilisateurs
@app.route('/getAllComments', methods=['GET'])
def get_all_comments():
    """
    Route pour récupérer tous les commentaires de tous les utilisateurs.
    Retourne une liste de tous les commentaires avec les informations des utilisateurs.
    """
    try:
        commentaires = Commentaire.query.all()
        result = []
        for commentaire in commentaires:
            result.append({
                'commentaire_id': commentaire.id_commentaire,
                'user_id': commentaire.id_user,
                'user_login': commentaire.user.login, 
                'commentaire': commentaire.commentaire
            })

        return jsonify({'status': 'success', 'comments': result}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)


