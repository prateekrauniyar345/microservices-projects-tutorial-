from flask import Blueprint

# Initialize the frontend blueprint
frontend_blueprint = Blueprint(
    'frontend',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)

# Import routes to register them with the blueprint
from . import routes
