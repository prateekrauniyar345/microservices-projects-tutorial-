from flask import Blueprint, Flask, session
from flask_login import LoginManager, UserMixin
from flask_bootstrap import Bootstrap
from app.frontend import frontend_blueprint


# User class for Flask-Login
class User(UserMixin):
    """User class that works with Flask-Login"""
    def __init__(self, user_id):
        self.id = user_id


app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'frontend.login'

bootstrap = Bootstrap(app)


# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load user from session"""
    # Check if user exists in session
    if 'user' in session:
        return User(user_id)
    return None


app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

app.register_blueprint(frontend_blueprint)

if __name__ == '__main__':
    print("app is running on port 5010", flush=True)
    app.run(debug=True, host='0.0.0.0', port=5010, use_reloader=True)

