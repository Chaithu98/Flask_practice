from flask import Flask, render_template,flash, request,session
from flask_pymongo import PyMongo
from flask_session import Session

app = Flask(__name__)
app.secret_key='Hello cafe'

app.config['MONGO_URI']="mongodb://localhost/Cafe"
mongo = PyMongo(app)
db = mongo.db.users
db2=mongo.db.prices
orders=mongo.db.orders

@app.route("/",methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/users", methods=['GET'])
def getUsers():
    return render_template("Display.html", newuser=db.find({},{"_id":0}))

@app.route("/register", methods=['GET','POST'])
def insertDetails():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        db.insert_one({
        'name': name,
        'email': email,
        'password':password
        })
        return render_template("index.html")
    return render_template("signup.html")

@app.route("/Signin", methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        session['email']=email
        if db.count_documents({'email':email})!=0 and db.count_documents({'password':password})!=0:
            flash(f'Email id already exixts','danger')
        return render_template("index.html")
    return render_template("signin.html")

def updateCost():
    db2.insert_one({
        'Item': 'Coffee',
        'Cost':60,
        })

@app.route('/Total',methods=['GET','POST'])
def totalItems():
    if request.method == "POST":
        ItemName = request.form.get("name")
        quantity = int(request.form.get("quantity"))
        cost=db2.find_one({'Item':ItemName},{'_id':0,'Cost':1})
        cost=cost['Cost']
        orders.insert_one({
        'Item': ItemName,
        'Cost':cost,
        'Quantity':quantity,
        })
        return render_template("AddingOrders.html",display=db2.find({},{"_id":0}))
    return render_template("Total.html")

@app.route('/Adding',methods=['GET','POST'])
def orderItems():
    return render_template("AddingOrders.html",newuser=orders.find({},{"_id":0}),display=db2.find({},{"_id":0}))
if __name__ == "__main__":
    app.run(debug=True, port=2000) 
