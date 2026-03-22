from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS empresas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        cnpj TEXT,
        status TEXT
    )
    """)
    return conn

@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        cursor.execute("INSERT INTO empresas (nome, cnpj, status) VALUES (?, ?, ?)",
                       (request.form["nome"], request.form["cnpj"], "Ativa"))
        conn.commit()
        return redirect("/")

    empresas = cursor.execute("SELECT * FROM empresas").fetchall()
    conn.close()

    return render_template("index.html", empresas=empresas)

@app.route("/bloquear/<int:id>")
def bloquear(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE empresas SET status='Bloqueada' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/excluir/<int:id>")
def excluir(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empresas WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
