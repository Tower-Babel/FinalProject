from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# connect to the MySQL database
db = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="yourdatabase"
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

if __name__ == "__main__":
    app.run(debug=True)