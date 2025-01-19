from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

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
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    commentaire = db.Column(db.String(500), nullable=False)  

    user = db.relationship('User', backref=db.backref('commentaires', lazy=True)) 

    def __repr__(self):
        return f'<Commentaire {self.commentaire}>'


# Route de test
@app.route('/')
def home():
    return "Connexion à la base de données réussie !"

# Route pour récupérer tous les utilisateurs
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour ajouter un utilisateur avec mot de passe crypté
@app.route('/register/<login>/<password>', methods=['POST'])
def add_user(login, password):
    try:
        hashed_password = generate_password_hash(password)
        new_user = User(login=login, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Utilisateur ajouté avec succès'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour vérifier un utilisateur (connexion)
@app.route('/login/<login>/<password>', methods=['POST'])
def login(login, password):
    user = User.query.filter_by(login=login).first()
    if user and check_password_hash(user.password, password):
        return jsonify({'message': 'Connexion réussie'}), 200
    else:
        return jsonify({'message': 'Identifiants incorrects'}), 401

# Route pour ajouter un commentaire
@app.route('/addComment', methods=['POST'])
def add_comment():
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

        return jsonify({'message': 'Commentaire ajouté avec succès'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


