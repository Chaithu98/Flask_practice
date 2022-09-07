from flask import Flask, render_template, request, jsonify, Response, json
from flask_pymongo import PyMongo, ObjectId

app = Flask(__name__)

app.config['MONGO_URI']="mongodb://localhost/Cafe"
mongo = PyMongo(app)
db = mongo.db.users


@app.route("/")
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
       id = db.insert_one({
        'name': name,
        'email': email
        })
       return "Your name is : "+name +" and email is : "+ email +" and your account is successfully created"
    return render_template("Success.html")


@app.route("/registration", methods=["GET"])
def createUsers():
    pass
    # id = db.insert_one({
    #     'name': request.json['name'],
    #     'email': request.json['email']
    # })
    # print("=======================================")
    # print(id.inserted_id)
    # print("=======================================")

    # #data = jsonify({'id':str(ObjectId(id.inserted_id)), 'msg':"User created successfully"})

    # return Response(
    #     mimetype="application/json",
    #     status=201,
    #     response=json.dumps({"message": "User created successfully", "id":str(id.inserted_id)})
    # )

if __name__ == "__main__":
    app.run(debug=True, port=2000)


# mongo -->   { 
#                  name: tom
#                  email: tom@gmail.com            
# }
