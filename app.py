from flask import Flask, render_template,flash, request,session,redirect,url_for
from flask_pymongo import PyMongo,ObjectId
from flask_session import Session
import bcrypt
import smtplib

app = Flask(__name__)
app.secret_key='Hello cafe'

app.config['MONGO_URI']="mongodb://localhost/Cafe"
mongo = PyMongo(app)
db = mongo.db.users
db2=mongo.db.prices
orders=mongo.db.orders
total=mongo.db.total

@app.route("/")
def index():
    # if 'user' in session:
    #     return 'You are logged in as '+ session['user']
    session['total']=0
    return render_template("index.html")
    
@app.route("/users", methods=['GET'])
def getUsers():
    return render_template("Display.html", newuser=db.find({},{"_id":0}))

@app.route("/register", methods=['GET','POST'])
def signup():
    if request.method == "POST":
        existing_user=db.find_one({'email':request.form['email']})

        if existing_user is None:
            hashpw=bcrypt.hashpw(request.form['password'].encode('utf-8'),bcrypt.gensalt())
            db.insert_one({'name': request.form['name'],
            'email': request.form['email'],
            'password':hashpw
            })
            session['user']=request.form['name']
            return render_template('Signin.html',word="Registered successfully!")
        flash(f'User already exist','hello')
    return render_template("signup.html")

@app.route("/Signin", methods=['GET','POST'])
def login():
    if request.method == "POST":
        login_user=db.find_one({'email':request.form['email']})

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'),login_user['password'])==login_user['password']:
                session['user']=login_user['name']
                return redirect('/')
            flash(f'Invalid email or password','danger')
    return render_template("signin.html")

@app.route("/SignOut", methods=['GET','POST'])
def logout():
    session['user']=None
    return redirect('/')

def updateCost():
    db2.insert_one({
        'Item': 'Coffee',
        'Cost':60,
        })
    

@app.route('/OrderDetails',methods=['GET','POST'])
def totalItems():
    if request.method == "POST":
        customers()
        orders.delete_many({})
        session['total']=0
        session['customer']=0
        return redirect("/")
    return render_template("Total.html",newuser=orders.find({}),total=session['total'])


@app.route('/Menu',methods=['GET','POST'])
def orderItems():
    global totalCount
    if request.method == "POST":
        ItemName = request.form.get("Item")
        quantity = int(request.form.get("quantity"))
        cost=db2.find_one({'Item':ItemName},{'_id':0,'Cost':1})
        qtyCost=cost['Cost']*quantity
        session['total'] +=qtyCost
        orders.insert_one({
        'Item': ItemName,
        'Cost':cost['Cost'],
        'Quantity':quantity,
        'qtyCost':qtyCost,
        })
        return render_template("AddingOrders.html",newuser=orders.find(),display=db2.find({},{"_id":0}),total=session['total'])
    return render_template("AddingOrders.html",newuser=orders.find(),display=db2.find({},{"_id":0}),total=session['total'])

@app.route('/update/<id>',methods=['GET','POST'])
def updateItem(id):
    if request.method == "POST":
        fqty=orders.find_one({'_id': ObjectId(id)},{'Quantity':1,'qtyCost':1})
        session['total']=session['total']-fqty['qtyCost']
        quantity = int(request.form.get("quantity"))
        cost=orders.find_one({'_id': ObjectId(id)},{'Cost':1})
        qtyCost=cost['Cost']*quantity
        orders.update_one({'_id': ObjectId(id)},{'$set':{'Quantity':quantity,'qtyCost':qtyCost}})
        session['total'] += qtyCost
        return redirect('/OrderDetails')
    return render_template("update.html",newuser=orders.find({'_id': id}),total=session['total'])

@app.route('/delete/<id>',methods=['GET','POST'])
def deleteItem(id):
    session['total'] -= orders.find_one({'_id': ObjectId(id)},{'qtyCost':1})['qtyCost']
    orders.delete_one({'_id': ObjectId(id)})
    return redirect('/OrderDetails')

@app.route('/Customer',methods=['GET','POST'])
def customersinfo():
    email=request.form.get("email")
    session['customer']=email
    return redirect('/')

def customers():
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("krishnakanha324@gmail.com", "lwwkgnghvuhjaegs")
    query=orders.find({},{'Item':1,'Cost':1})
    print(query[0]['Item'])
    message = "-------------Welcome to Coffe on clouds-----------\n"
    for item in query:
        st=str(item['Item'])
        c=str(item['Cost'])
        val ="Item :"+st+" Cost :"+c+"\n"
        message=message+val
    message=message+"Total:"+str(session['total'])
    print(message)
    try:
        val=session['customer']
        #s.sendmail("krishnakanha324@gmail.com", val, message)
        print('notification sent')
    except:
        print('error sending notification')
        s.quit()
if __name__ == "__main__":
    app.run(debug=True, port=2000) 
