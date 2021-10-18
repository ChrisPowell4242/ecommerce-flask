from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, username, email, password):
        self.username=username
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(200))
    price = db.Column(db.Numeric(10, 2))
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product = db.relationship('User', backref='owner', lazy=True)

    def __init__(self, name, price, description, user_id):
        self.name = name
        self.price = price
        self.description = description
        self.user_id = user_id

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(200))
    price = db.Column(db.Numeric(10, 2))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    def __init__(self, name, price, user_id, product_id):
        self.name = name
        self.price = price

        self.user_id = user_id
        self.product_id = product_id

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(200))
    content = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id