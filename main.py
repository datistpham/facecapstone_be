from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="time_keeping"
    )

    # Tạo một đối tượng cursor để truy xuất cơ sở dữ liệu
cursor = mydb.cursor()
app = Flask(__name__)
CORS(app)
@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="time_keeping"
)
mycursor = mydb.cursor()
def get_employee_faces():
    # connect to the database

    # create a cursor object
    

    # execute the query to select all the face image paths from the employees table

    # fetch all the results
    results = mycursor.fetchall()

    # close the database connection
    mydb.close()

    # return the list of face image paths
    return [result[0] for result in results]

@app.route('/')
def hello():
    return 'Hello World!'
@app.route("/signup", methods=["POST"])
async def signup():
    data= request.json
    name= data["name"]
    email= data["email"]
    phone= data["phone"]
    password= data["password"]
    try:
        mycursor.execute(f"SELECT email FROM employees WHERE email = '{email}'")
        results = mycursor.fetchall()
        if(len(results) > 0 ):
            return jsonify({"signup": False, "exist": True})
        mycursor.execute("INSERT INTO employees(name, email, phone, password) VALUES(%s, %s, %s, %s)", (name, email, phone, password))
        mydb.commit()
        mycursor.execute(f"SELECT id FROM employees WHERE email= '{email}'")
        results2= mycursor.fetchall()
        return jsonify({"signup": True, "uid": results2[0]})
    except Exception as e: 
        print(str(e))
        mydb.rollback()
        return {'signup': False}
if __name__ == '__main__':
    app.run(debug=True)