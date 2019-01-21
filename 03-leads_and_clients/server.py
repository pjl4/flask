from flask import Flask,render_template,session,request,redirect
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
app = Flask(__name__)

@app.route('/')
def index():
    mysql=connectToMySQL("lead_gen_business")
    query="SELECT CONCAT(clients.first_name,' ', clients.last_name) AS Name, leads.leads_id, sites.site_id,COUNT(clients.client_id) AS leads FROM clients LEFT JOIN sites ON clients.client_id=sites.client_id LEFT JOIN leads ON sites.site_id=leads.site_id GROUP BY clients.client_id ORDER BY leads DESC;"
    all_leads=mysql.query_db(query)
    
    return render_template('index.html',clients=all_leads)



if __name__ == "__main__":
    app.run(debug=True)