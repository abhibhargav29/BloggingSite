from flask import Flask, render_template, request, redirect
import pymysql as mysql
from datetime import datetime
import time
import sys

#Initialize app
app = Flask(__name__)

#Login page function
@app.route("/", methods=["GET","POST"])
def LogIn():

    if(request.method == "POST"):
        username = request.form["user"]
        password = request.form["pass"]
        query1 = f"SELECT password FROM Users WHERE UserName = '{username}'"
        try:
            cur.execute(query1)
            originalPass = cur.fetchall()[0][0]
            if(originalPass==password):
                return redirect(f"/{username}")
            else:
                return redirect(f"/")
        except:
            return redirect(f"/")

    return render_template("LogIn.html")

#New user function
@app.route("/NewUser", methods=["GET","POST"])
def Register():

    if(request.method=="POST"):
        username = request.form["user"]
        password = request.form["pass"]
        realname = request.form["name"]
        query = f"INSERT INTO Users VALUES('{username}','{realname}','{password}')"
        if(username=="" or password==""):
            return redirect("/NewUser")
        try:
            cur.execute(query)
            con.commit()
            return redirect("/")
        except:
            return redirect("/NewUser")

    return render_template("Register.html")

#Main page function
@app.route("/<string:user>", methods=["GET","POST"])
def MainWindow(user):
    cur.execute("SELECT * FROM BlogPosts")
    rows = cur.fetchall()
    if(request.method == "POST"):
        title = request.form["title"]
        content = request.form["content"]
        query = f"INSERT INTO BlogPosts(BlogTitle,AuthorUserName,BlogText) VALUES('{title}', '{user}', '{content}')"
        try:
            cur.execute(query)
            con.commit()
            print("done")
            return redirect(f"/{user}")
        except:
            print("failed")
            return redirect(f"/{user}")

    return render_template(("Main.html"), allPosts=rows, userName=user)

#Delete function
@app.route("/delete/<string:user>/<int:id>")
def deletePost(user,id):
    query = f"DELETE FROM BlogPosts WHERE BlogId={id} AND AuthorUserName='{user}'"
    try:
        cur.execute(query)
        con.commit()
    except:
        print("failed")
        return redirect(f"/{user}")
    return redirect(f"/{user}")


#Edit window
@app.route("/edit/<string:user>/<int:id>", methods=["GET","POST"])
def editPost(user,id):
    try:
        cur.execute(f"SELECT * FROM BlogPosts WHERE BlogId={id} AND AuthorUserName='{user}'")
        post = cur.fetchall()
    except:
        print("failed")
        return redirect(f"/{user}")

    if(len(post)==0):
        return redirect(f"/{user}")

    if(request.method=="POST"):
        title = request.form["title"]
        content = request.form["content"]
        try:
            query = f"UPDATE BlogPosts SET BlogTitle='{title}', BlogText='{content}' WHERE BlogId={id}"
            cur.execute(query)
            con.commit()
        except:
            return redirect(f"/{user}")
        return redirect(f"/{user}")
    
    return render_template("Edit.html", postp=post, userName=user)

#Driver code
if __name__ == "__main__":
    try:
        con = mysql.connect(host="localhost", user="root", password="4647", database="blogs")
        cur = con.cursor()
    except:
        print("connection failed")
        time.sleep(1)
        sys.exit()
    
    app.run(debug=True)
