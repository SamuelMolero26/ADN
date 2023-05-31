from flask import Flask, redirect, url_for, Blueprint
from data import app, initialize_database, login_manager
from data import login, add_client, clients, search_clients, logout

# Register the login manager
login_manager.init_app(app)

# Initialize the database
initialize_database()

# Import the routes from data.py
from data import login, add_client, clients, search_clients, logout

# route registration
login  = Blueprint('login', __name__)

add_client = Blueprint('add_client', __name__)

clients = Blueprint('clients',__name__)

search_clients = Blueprint('search_clients',__name__)

logout = Blueprint('logout', __name__)




# Set the root URL ("/") to redirect to the login page
@app.route("/")
def root():
    return redirect(url_for("login"))

if __name__ == '__main__':
    
    app.run(debug=True)