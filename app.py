from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

# Ensure pymysql is used as MySQLdb
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# Update the SQLAlchemy Database URI to use PyMySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bloging'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(12), nullable=True, default=datetime.utcnow().strftime('%Y-%m-%d'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        message = request.form.get('message')

        # Check if data is captured correctly
        print(f"Received: {name}, {email}, {mobile}, {message}")

        entry = Contact(name=name, email=email, mobile=mobile, message=message)
        db.session.add(entry)
        db.session.commit()
        print("Data committed to the database")

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
