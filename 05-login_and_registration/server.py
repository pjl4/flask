from flask import Flask,render_template,session,request,redirect,flash
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
import re
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt=Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=["POST"])
def create():
    mysql=connectToMySQL("loginDB")
    user=request.form
    query="SELECT * FROM users WHERE email=%(email)s;"
    data={
        'email': user['email']
    }
    if len(user['email']) <1:
        flash ("Email cannot be blank")
    if not EMAIL_REGEX.match(user['email']):
        flash ("Email is not valid")
    if mysql.query_db(query,data):
        flash ("Email or password incorrect")
    if (len(user['first_name']) < 2):
        flash("First Name must not be blank")
    if  re.search("[0-9]",user['first_name']):
        flash("First name cannot contain numbers")
    if  re.search("[0-9]",user['last_name']):
        flash("Last name cannot contain numbers")
    if (len(user['last_name']) < 2):
        flash("Last Name must not be blank")
    if (len(user['password'])<8):
        flash("Password must be more than 8 characters")
    if (user['password']!=user['confirm']):
        flash("Passwords must match")
    if not re.search("[A-Z]",user['password']):
        flash("Password must contain 1 Upper Case")
    if not re.search("[0-9]",user['password']):
        flash("Password must contain 1 Number")
    if '_flashes' in session.keys():
        return redirect("/")
    
    pw_hash = bcrypt.generate_password_hash(user['password'])
    query2= "INSERT INTO users (first_name,last_name,email,pw_hash) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(pw_hash)s);"
    data2={
        'first_name': user['first_name'],
        'last_name':user['last_name'],
        'email': user['email'],
        'pw_hash': pw_hash
    }
    mysql=connectToMySQL("logindb")
    
    new_user=mysql.query_db(query2,data2)
    flash("Successfully Registered!")
    session['first_name']=user['first_name']
    return redirect('/success')
@app.route('/login',methods=['POST'])
def login():
    mysql=connectToMySQL("loginDB")
    user=request.form
    query="SELECT * FROM users WHERE email=%(email)s;"
    data={
        'email': user['email']
    }
    result=mysql.query_db(query,data)
    if result:
        if bcrypt.check_password_hash(result[0]['pw_hash'], user['passwordLogin']):
            session['first_name']=result[0]['first_name']
            return redirect('/success')
    flash("You could not be logged in.")
    return redirect('/dashboard')
@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')
if __name__ == "__main__":
    app.run(debug=True)