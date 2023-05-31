import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.secret_key = 'tucutaca'

login_manager = LoginManager()
login_manager.init_app(app)

# User class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print("step 1")

        # Perform authentication logic here

        # Check if the email and password are valid
        if (email == 'user@example.com' and password == 'password'):
            print('login succesful')
            # Authentication successful
            user = User(1)  # Create a User object with the ID
            login_user(user)  # Log in the user
            return redirect(url_for('add_client'))
        else:
            # Authentication failed
            return render_template('login.html', message='Invalid email or password')

    return render_template('login.html')


def initialize_database():
    conn = sqlite3.connect('clients.db') # connects to the database or creates one if it doesn't exist 
    cursor = conn.cursor() # to execute SQL commands
    # client table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            bday TEXT,
            email TEXT,
            phone TEXT,
            address TEXT
        )
    ''')
    # tag table         
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_name TEXT,
            company TEXT,
            client_id INTEGER,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')

    conn.close()

initialize_database()

@login_required
@app.route('/templates/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        name = request.form['name']
        bday = request.form['bday']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        conn = sqlite3.connect('clients.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO clients (name, bday, email, phone, address) VALUES (?, ?, ?, ?, ?)',
                       (name, bday, email, phone, address))
        conn.commit()
        conn.close()

        return redirect(url_for('clients'))

    return render_template('add_client.html')

@login_required
@app.route('/clients')
def clients():
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()
    conn.close()
    return render_template('clients.html', clients=clients)


# create tag -----> medicare, obamacare & life insurance
def client_tag(tag_name, company, client_id):

    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tags (tag_name, company, client_id) VALUES (?, ?, ?)', (tag_name, company, client_id))
    conn.commit()
    conn.close()

    print('Tag created')

# to get clients based on the tag assigned 
def get_client_by_tag(tag_name):
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT clients.* FROM clients
        INNER JOIN tags ON clients.id = tags.client_id
        WHERE tags.tag_name = ?
    ''', (tag_name,))

    clients = cursor.fetchall()
    conn.close()

    return clients


@app.route('/search', methods=['GET', 'POST'])
def search_clients():
    if request.method == 'POST':
        tag_name = request.form['tag_name']

        clients = get_client_by_tag(tag_name)

        return render_template('search.html', clients=clients)

    return render_template('search.html')


# get all clients period

def get_all_clients():
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()
    conn.close()
    return clients


# @app.route('/login')
# def home():
#     return render_template('login.html')


@app.route('/index')
@login_required
def index():
    return redirect(url_for('add_clients'))


# If I have login, I need logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Run the Flask application
if __name__ == '__main__':
    #initialize_database()
    app.run()


# Run the Flask application



#-------test stuff----------------
# add_client('John Doe', '1985-07-15', 'john@example.com', '1234567890', '123 Main St')
# add_client('Jane Smith', '1990-03-22', 'jane@example.com', '9876543210', '456 Elm St')
# add_client('Alice Johnson', '1978-11-01', 'alice@example.com', '5555555555', '789 Oak St')
# add_client('Bob Williams', '1982-09-10', 'bob@example.com', '9999999999', '321 Pine St')

# client_tag('Medicare', 'ABC Insurance', 1)
# client_tag('Life Insurance', 'XYZ Insurance', 2)
# client_tag('ObamaCare', 'DEF Insurance', 3)
# client_tag('Medicare', 'ABC Insurance', 4)
# client_tag('Life Insurance', 'XYZ Insurance', 4)

# # Retrieve clients by tag
# medicare_clients = get_client_by_tag('Medicare')
# print("Medicare Clients:")
# for client in medicare_clients:
#     print(client)

# life_insurance_clients = get_client_by_tag('Life Insurance')
# print("Life Insurance Clients:")
# for client in life_insurance_clients:
#     print(client)

# # Retrieve all clients
# all_clients = get_all_clients()
# print("All Clients:")
# for client in all_clients:
#     print(client)