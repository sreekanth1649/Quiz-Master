from flask import Flask
from config import Config
from models import db, User  
from flask import Blueprint, render_template, request, redirect, url_for
from flask_migrate import Migrate  
from flask_login import LoginManager

from routes.auth import auth_bp
from routes.user import user_bp
from routes.admin import admin_bp  
  

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(admin_bp, url_prefix="/admin")  

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  

@app.route("/")
def home():
    return render_template("index.html")




if __name__ == "__main__":
    app.run(debug=True)
