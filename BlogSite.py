from flask import Flask, render_template, request, redirect, Response
from flaskext.mysql import MySQL
from flask_cors import CORS
import pymysql
from datetime import datetime
import time
import sys
import os
import pickle
import re
import face_recognition


#Functions for Face Recognition
def RegisterFace(Username, fileName):
    try:
        with open("faceDict.pkl","rb") as file1:
            face_dict = pickle.load(file1)
    except:
        face_dict = {}
    
    face = face_recognition.load_image_file(fileName)
    if(len(face_recognition.face_locations(face))==0):
        return False
        
    face_encoding = face_recognition.face_encodings(face)
    face_dict[Username] = [face_encoding]

    with open("faceDict.pkl","wb") as file1:
        pickle.dump(face_dict, file1)
    return True

def ValidateFace(Username, fileName):
    with open("faceDict.pkl","rb") as file1:
        face_dict = pickle.load(file1)
        
    newFace = face_recognition.load_image_file(fileName)
    if(len(face_recognition.face_locations(newFace))==0):
        return False
    
    newFace_encodings = face_recognition.face_encodings(newFace)
    for newFace_encoding in newFace_encodings:
        result = face_recognition.compare_faces(face_dict[Username], newFace_encoding)
        x=list(result[0]).count(True)
        if(x/128*100>=75):
            return True
            
    return False


#Initialize app
app = Flask(__name__)
app.secret_key = "secret"
CORS(app)

#Initialize mysql
mysql = MySQL(cursorclass = pymysql.cursors.DictCursor)
app.config['MYSQL_DATABASE_USER'] = "mysqldbuser@blogging-site29-mysqldbserver"
app.config['MYSQL_DATABASE_PASSWORD'] = "gROMSTARK29@"
app.config['MYSQL_DATABASE_DB'] = "mysqldatabase919"
app.config['MYSQL_DATABASE_HOST'] = "blogging-site29-mysqldbserver.mysql.database.azure.com"
mysql.init_app(app)


#Login page
@app.route("/", methods=["GET","POST"])
def LogIn():

    if(request.method == "POST"):
        username = request.form["user"].strip()
        password = request.form["pass"].strip()
        query1 = f"SELECT password FROM Users WHERE UserName = '{username}'"
        try:
            con = mysql.connect()
            cur = con.cursor()
            cur.execute(query1)
            originalPass = cur.fetchall()[0]["password"]
            if(originalPass==password):
                try:
                    with open("faceDict.pkl","rb") as file1:
                        face_dict = pickle.load(file1)
                except:
                    face_dict = {}
                if(username not in face_dict):
                    return redirect(f"/{username}")
                else:
                    return redirect(f"/CheckFace/{username}")
            else:
                return render_template("login.html", flag="1", username=username)
        except:
            return render_template("login.html", flag="2", username="")

    return render_template("LogIn.html", flag="0", username="")

#Check user
@app.route("/CheckFace/<string:username>", methods = ["POST","GET"])
def checkNewFace(username):

    if(request.method=="POST"):
        img = request.files['image']
        img.save(f"{username}.jpg")
        if(ValidateFace(f'{username}', f'{username}.jpg')):
            os.remove(f'{username}.jpg')
            return Response(status=200)
        else:
            os.remove(f'{username}.jpg')
            return Response(status=201)

    return render_template(("CheckFace.html"), username=username)

#New user page
@app.route("/NewUser", methods=["GET","POST"])
def Register():

    if(request.method=="POST"):
        username = request.form["user"].strip()
        password = request.form["pass"].strip()
        realname = request.form["name"].strip()
        query = f"INSERT INTO Users VALUES('{username}','{password}','{realname}')"
        try:
            con = mysql.connect()
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            con.close()
            return redirect(f"/addFace/{username}")
        except Exception as e:
            print(type(e))
            print(e.args)
            return render_template("Register.html", flag="1")

    return render_template("Register.html", flag="0")

#Add user face
@app.route("/addFace/<string:username>", methods=["GET","POST"])
def addNewFace(username):

    if(request.method == "POST"):
        img = request.files['image']
        img.save(f"{username}.jpg")
        x = RegisterFace(f'{username}', f'{username}.jpg')
        if(x):
            os.remove(f'{username}.jpg')
            return Response(status=200)
        else:
            os.remove(f'{username}.jpg')
            return Response(status=201)

    return render_template(("Capture.html"), username=username)

#Main page
@app.route("/<string:user>", methods=["GET","POST"])
def MainWindow(user):
    con = mysql.connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM BlogPosts")
    rows = cur.fetchall()

    if(request.method == "POST"):
        title = request.form["title"]
        content = request.form["content"]
        title = re.sub("'","''",title)
        content = re.sub("'","''",content)
        query = f"INSERT INTO BlogPosts(BlogTitle,AuthorUserName,BlogText) VALUES('{title}', '{user}', '{content}')"
        try:
            con2 = mysql.connect()
            cur2 = con2.cursor()
            cur2.execute(query)
            con2.commit()
            con2.close()
            return redirect(f"/{user}")
        except:
            return redirect(f"/{user}")

    return render_template(("Main.html"), allPosts=rows, userName=user)

#Delete page
@app.route("/delete/<string:user>/<int:id>")
def deletePost(user,id):
    query = f"DELETE FROM BlogPosts WHERE BlogId={id} AND AuthorUserName='{user}'"
    try:
        con = mysql.connect()
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        con.close()
    except:
        return redirect(f"/{user}")
    return redirect(f"/{user}")


#Edit page
@app.route("/edit/<string:user>/<int:id>", methods=["GET","POST"])
def editPost(user,id):
    con = mysql.connect()
    cur = con.cursor()
    cur.execute(f"SELECT * FROM BlogPosts WHERE BlogId={id} AND AuthorUserName='{user}'")
    post = cur.fetchall()

    if(request.method=="POST"):
        title = request.form["title"]
        content = request.form["content"]
        title = re.sub("'","''",title)
        content = re.sub("'","''",content)
        try:
            con2 = mysql.connect()
            cur2 = con2.cursor()
            query = f"UPDATE BlogPosts SET BlogTitle='{title}', BlogText='{content}' WHERE BlogId={id}"
            cur2.execute(query)
            con2.commit()
            con2.close()
            return redirect(f"/{user}")
        except:
            return redirect(f"/{user}")
    
    return render_template("Edit.html", postp=post[0], userName=user)


if __name__ == "__main__":
    app.run(debug=True)
