from asyncio.windows_events import NULL
from genericpath import exists
from xml.etree.ElementTree import tostring
from flask import Flask, render_template, request, redirect, url_for, make_response
import mysql.connector

app = Flask(__name__,template_folder='templates', static_folder='staticFiles')

# connect to the MySQL database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="blog_db"
)

@app.route("/")
def index():
    # retrieve all blog posts from the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    try:
        return render_template("index.html", posts=posts, userID = int(cookie()))
    except:
        return redirect(url_for("cookie"))

@app.route("/blogs", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        # get the form data and insert it into the database
        title = request.form["title"]
        content = request.form["content"]
        cursor = db.cursor()
        cursor.execute("INSERT INTO posts (title, content, created_by) VALUES (%s, %s, %s)", (title, content, int(cookie())))
        db.commit()
        return redirect(url_for("index"))
    else:
        # show the form to create a new post
        return render_template("blogs.html",userID = int(cookie()))
@app.route("/signInUp", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        # logs user in
        username = request.form["username"]
        password = request.form["password"]
        cursor = db.cursor()
        cursor.execute("SELECT id FROM logins WHERE username = %(usernameStored)s and user_password = %(password_stored)s;", {"usernameStored": username, "password_stored": password})
        try:
            userIDStored = cursor.fetchall()
            userIDStored = userIDStored[0]
       
            res = make_response(redirect(url_for("index")))
            res.set_cookie('userID', str(userIDStored[0]) , max_age=60*60*24*365*2)
            return res
        except:
            res = make_response(redirect(url_for("create_account")))
            res.set_cookie('userID', "0" , max_age=60*60*24*365*2)
            return res
    else:
        # show the show the signup form
        return render_template("signInUp.html", userID = int(cookie()))
@app.route("/signUP", methods=["GET", "POST"])
def signUP():
    if request.method == "POST":
        # todo add accounts to database this includes a check here to see if it is a login or a sign up and the logic to handle either
        username = request.form["userName"]
        password = request.form["Password"]
        cursor = db.cursor()
        cursor.execute("INSERT INTO logins (username, user_password) VALUES (%s, %s)", (username, password))
        db.commit()
        cursor.execute("SELECT id FROM logins WHERE username = %(usernameStored)s and user_password = %(password_stored)s;", {"usernameStored": username, "password_stored": password})
        userIDStored = cursor.fetchall()
        userIDStored = userIDStored[0]
        print(userIDStored[0])
        res = make_response(redirect(url_for("index")))
        res.set_cookie('userID', str(userIDStored[0]) , max_age=60*60*24*365*2)
        return res
    else:
        # show the show the signup form
        return redirect(url_for("create_account"))  
@app.route("/signout", methods=["GET", "POST"])
def signout():
       
            cursor = db.cursor()
            cursor.execute("SELECT * FROM posts")
            posts = cursor.fetchall()
            res = make_response(redirect(url_for("index")))
            res.set_cookie('userID', '0', max_age=60*60*24*365*2)
           
            return res


    
@app.route("/vision", methods=["GET", "POST"])
def show_vision():
        # show the show the vision page
        return render_template("vision.html", userID = int(cookie()))

@app.route('/cookie/')
def cookie():
    if not request.cookies.get('userID'):
        res = make_response(redirect(url_for("index")))
        res.set_cookie('userID', '0', max_age=60*60*24*365*2)
    else:
        res = (request.cookies.get('userID'))
    return res



if __name__ == "__main__":
    app.run(debug=True)