
from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(_file_))
import os
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "templates"))




app.secret_key = "eduguard_secret"

def get_db():
    return sqlite3.connect("eduguard.db")

# ✅ Database Setup
conn = get_db()
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS students (name TEXT, roll TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS teachers (name TEXT, subject TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS attendance (roll TEXT, status TEXT)")

conn.commit()
conn.close()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        return "Invalid Login"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users VALUES (?,?)", (username,password))
        conn.commit()
        conn.close()

        return redirect("/")
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("index.html")
    return redirect("/")

@app.route("/student", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO students VALUES (?,?)", (name,roll))
        conn.commit()
        conn.close()

        return redirect("/dashboard")
    return render_template("student.html")

@app.route("/teacher", methods=["GET", "POST"])
def teacher():
    if request.method == "POST":
        name = request.form["name"]
        subject = request.form["subject"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO teachers VALUES (?,?)", (name,subject))
        conn.commit()
        conn.close()

        return redirect("/dashboard")
    return render_template("teacher.html")

# ✅ QR Attendance (Code-based for now)
@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    if request.method == "POST":
        roll = request.form["roll"]
        status = "Present"

        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO attendance VALUES (?,?)", (roll,status))
        conn.commit()
        conn.close()

        return "Attendance Marked Successfully"

    return render_template("attendance.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
