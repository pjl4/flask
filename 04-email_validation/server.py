from flask import Flask,render_template,session,request,redirect,flash
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
import re
app = Flask(__name__)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    mysql=connectToMySQL("emaildb")
    query="SELECT * FROM email"
    all_email=mysql.query_db(query)

    return render_template("success.html",email=all_email)

@app.route('/delete',methods=["POST"])
def delete():
    mysql=connectToMySQL("emaildb")
    query="DELETE FROM email WHERE email = %(email)s"
    data={
        'email': request.form['email']
    }
    mysql.query_db(query,data)
    return redirect('/success')


@app.route('/add',methods=["POST"])
def create():
    mysql=connectToMySQL("emaildb")

    query="SELECT * FROM email WHERE email=%(email)s;"
    data={
        'email': request.form['email']
    }
    if len(request.form['email']) <1:
        flash ("Email cannot be blank")
    if not EMAIL_REGEX.match(request.form['email']):
        flash ("Email is not valid")
    if mysql.query_db(query,data):
        flash ("Email is taken")
    if '_flashes' in session.keys():
        return redirect("/")
    
    query2= "INSERT INTO email (email,created_at) VALUES (%(email)s,NOW());"
    mysql=connectToMySQL("emaildb")
    
    new_email_id=mysql.query_db(query2,data)
    return redirect('/success')

if __name__ == "__main__":
    app.run(debug=True)