from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def db():
    return sqlite3.connect("db.db")

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        c = db()
        cur = c.cursor()
        cur.execute("INSERT INTO empresas(nome,cnpj,status) VALUES(?,?,?)",
        (request.form["nome"], request.form["cnpj"], "Ativa"))
        c.commit()
        c.close()
        return redirect("/")
    
    c = db()
    cur = c.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS empresas(id INTEGER PRIMARY KEY, nome TEXT, cnpj TEXT, status TEXT)")
    dados = cur.execute("SELECT * FROM empresas").fetchall()
    c.close()

    return render_template("index.html", dados=dados)

@app.route("/bloquear/<int:id>")
def bloquear(id):
    c = db()
    cur = c.cursor()
    cur.execute("UPDATE empresas SET status='Bloqueada' WHERE id=?", (id,))
    c.commit()
    c.close()
    return redirect("/")

@app.route("/excluir/<int:id>")
def excluir(id):
    c = db()
    cur = c.cursor()
    cur.execute("DELETE FROM empresas WHERE id=?", (id,))
    c.commit()
    c.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
