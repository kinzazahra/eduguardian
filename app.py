from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -------------------------
# Knowledge Vault Layer
# -------------------------

def init_db():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        attendance INTEGER,
        marks INTEGER

    )
    """)

    conn.commit()
    conn.close()

init_db()


# -------------------------
# Student Interface Layer
# -------------------------

@app.route("/")
def home():

    return render_template("index.html")


@app.route("/student")
def student():

    return render_template("student.html")


# -------------------------
# Pedagogical Agent Layer
# -------------------------

@app.route("/submit", methods=["POST"])

def submit():

    name = request.form["name"]
    attendance = request.form["attendance"]
    marks = request.form["marks"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO students(name, attendance, marks)
    VALUES (?, ?, ?)
    """, (name, attendance, marks))

    conn.commit()
    conn.close()

    return render_template("prediction.html")


# -------------------------
# Mastery Engine Layer
# EduChampion Integration
# -------------------------

@app.route("/prediction")

def prediction():

    return render_template("prediction.html")


# -------------------------
# Faculty Dashboard Layer
# -------------------------

@app.route("/faculty")

def faculty():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")

    data = cur.fetchall()

    conn.close()

    return render_template("faculty.html", data=data)


# -------------------------

if __name__ == "__main__":

    app.run(debug=True)