from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__,template_folder='templates', static_folder='staticFiles')

# connect to the MySQL database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="testbase"
)

@app.route("/")
def index():
    # retrieve all blog posts from the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return render_template("index.html", posts=posts)

@app.route("/blogs", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        # get the form data and insert it into the database
        title = request.form["title"]
        content = request.form["content"]
        cursor = db.cursor()
        cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        db.commit()
        return redirect(url_for("index"))
    else:
        # show the form to create a new post
        return render_template("blogs.html")
@app.route("/signInUp", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        # todo add accounts to database this includes a check here to see if it is a login or a sign up and the logic to handle either
        return render_template("signInUp.html")
    else:
        # show the show the signup form
        return render_template("signInUp.html")
    
@app.route("/vision", methods=["GET", "POST"])
def show_vision():
        # show the show the vision page
        return render_template("vision.html")

if __name__ == "__main__":
    app.run(debug=True)