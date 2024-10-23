from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

# Initialize the Flask app
app = Flask(__name__)

# Configuration for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.Integer, nullable=True)
    BirthPlace = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'

india_data = {
    "states": [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", 
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", 
        "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", 
        "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", 
        "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", 
        "West Bengal", "Andaman and Nicobar Islands", "Chandigarh", 
        "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Lakshadweep", 
        "Puducherry", "Ladakh", "Jammu and Kashmir"
    ],
    
    "first_names": [
        "Amit", "Raj", "Pooja", "Sunita", "Rohit", "Sanjay", "Neha", "Kiran", 
        "Naveen", "Manisha", "Deepak", "Asha", "Arun", "Ravi", "Kavita", "Sumit", 
        "Anita", "Prakash", "Vikram", "Ritu", "Suresh", "Vinay", "Anjali", "Kapil", 
        "Pankaj", "Priya", "Jitendra", "Siddharth", "Aishwarya", "Anand", 
        "Rajesh", "Sneha", "Varun", "Komal", "Ashok", "Swati", "Shweta", "Rahul", 
        "Dinesh", "Harish", "Mohan", "Nikhil", "Meena", "Gaurav", "Arpita", 
        "Ajay", "Vijay", "Monika", "Santosh", "Rani", "Sakshi"
    ],

    "surnames": [
        "Sharma", "Verma", "Rao", "Patel", "Singh", "Gupta", "Das", "Kumar", 
        "Iyer", "Reddy", "Yadav", "Choudhary", "Mishra", "Ghosh", "Rathore", 
        "Bhat", "Jain", "Thakur", "Naidu", "Nair", "Mehta", "Pillai", "Khan", 
        "Prajapati", "Sen", "Bose", "Agarwal", "Malhotra", "Joshi", "Pandey", 
        "Bhatt", "Desai", "Kapoor", "Tiwari", "Shukla", "Menon", "Roy", "Shetty", 
        "Chakraborty", "Dubey", "Dwivedi", "Mahajan", "Saxena", "Chauhan", 
        "Banerjee", "Kulkarni", "Jha", "Murthy", "Garg", "Pathak", "Biswas"
    ]
}

# Home Route - Read (R)
@app.route('/')
def index():
    # Create the database and tables if they don't exist
    db.create_all()
    users = User.query.all()
    return render_template('index.html', users=users)

# Add User - Create (C)
@app.route('/add', methods=['POST'])
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    if username and email:
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('index'))

# Update User - Update (U)
@app.route('/update/<int:id>', methods=['POST'])
def update_user(id):
    user = User.query.get_or_404(id)
    username = request.form.get('username')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    BirthPlace = request.form.get('BirthPlace')
    if username and email and (phone_number or BirthPlace):
        user.username = username
        user.email = email
        user.phone_number = phone_number
        user.BirthPlace = BirthPlace
        db.session.commit()
    return redirect(url_for('index'))

# Delete User - Delete (D)
@app.route('/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/autoGenerate', methods=['POST'])
def autoGenerate():
    autogen = int(request.form.get("generateB"))
    for i in range(autogen):
        username = random.choice(india_data["first_names"]) + " " + random.choice(india_data["surnames"])
        email = username.replace(" ", ".") + "@gmail.com"
        phone_number = random.randrange(1000000000, 10000000000)
        BirthPlace = random.choice(india_data["states"])
        new_user = User(username=username, email=email, phone_number=phone_number, BirthPlace=BirthPlace)
        db.session.add(new_user)
        db.session.commit()
        print(f"Completed : {i}")
    return redirect(url_for('index'))
    
# Main Entry Point
if __name__ == "__main__":

    # Start the Flask app
    app.run(debug=True)
