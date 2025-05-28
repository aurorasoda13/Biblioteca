import pymysql.cursors
from flask import Flask, render_template, request, redirect

connection = pymysql.connect(
    host='138.41.20.102',
    port=53306,
    user='soda',
    password='studente',
    database='5bi_2025'
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/catalogo')
def catalogo():
    cursor = connection.cursor()
    sql = 'SELECT Copertina, Titolo, Autore, nome, IDLibro FROM A_Libro inner join A_Genere on A_Libro.IDGenere=A_Genere.IDGenere'
    cursor.execute(sql)
    result = cursor.fetchall()
    sql='SELECT nome FROM A_Genere'
    cursor.execute(sql)
    generi = cursor.fetchall()
    cursor.close()
    return render_template("catalogo.html", result=result, generi=generi)

@app.route('/filtragenere', methods=['POST'])
def filtragenere():
    nome = request.form['nome']
    cursor = connection.cursor()
    sql = 'SELECT Copertina, Titolo, Autore, nome, IDLibro FROM A_Libro inner join A_Genere on A_Libro.IDGenere=A_Genere.IDGenere WHERE nome=%s'
    cursor.execute(sql, (nome,))
    result = cursor.fetchall()
    sql='SELECT nome FROM A_Genere'
    cursor.execute(sql)
    generi = cursor.fetchall()
    cursor.close()
    return render_template("catalogo.html", result=result, generi=generi)

@app.route('/libro', methods=['POST'])
def libro():
    IDLibro = request.form['IDLibro']
    cursor = connection.cursor()
    sql = "SELECT Copertina, Titolo, Autore, nome, descrizione, Link, IDLibro FROM A_Libro inner join A_Genere on A_Libro.IDGenere=A_Genere.IDGenere WHERE IDLibro = %s"
    cursor.execute(sql, (IDLibro,))
    libro = cursor.fetchall()
    cursor.close()


    cursor = connection.cursor()
    sql = "SELECT Nome, Recensione FROM A_Recensione WHERE IDLibro = %s"  
    cursor.execute(sql, (IDLibro,))
    recensioni = cursor.fetchall()
    cursor.close()
    
    
    return render_template("libro.html", libro=libro, recensioni=recensioni)



@app.route('/recensione', methods=['POST'])
def recensione():
    IDLibro = request.form['IDLibro']
    cursor = connection.cursor()
    sql = "SELECT Copertina, Titolo, Autore, nome, descrizione, IDLibro FROM A_Libro inner join A_Genere on A_Libro.IDGenere=A_Genere.IDGenere WHERE IDLibro = %s"
    cursor.execute(sql, (IDLibro,))
    result = cursor.fetchall()
    cursor.close()
    return render_template("recensione.html", result=result)


@app.route('/executerecensione', methods=['POST'])
def executerecensionerecensione():
    nome=request.form['nome']
    recensione=request.form['recensione']
    IDLibro=request.form['IDLibro']
    cursor=connection.cursor()
    sql="INSERT INTO A_Recensione (nome, recensione, IDLibro) VALUES (%s, %s, %s)"
    print(sql)
    cursor.execute(sql, (nome, recensione, IDLibro))
    connection.commit()
    cursor.close()
    return redirect("/catalogo")

@app.route('/newlibro', methods=['GET'])
def newlibro():
    cursor=connection.cursor()
    sql="SELECT nome FROM A_Genere"
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    return render_template("insert.html", result=result)

@app.route('/executeinsert', methods=['POST'])
def executeinsert():
    Titolo=request.form['Titolo']
    Autore=request.form['Autore']
    Link=request.form['Link']
    nome=request.form['nome']
    print(nome)
    Copertina=request.form['Copertina']
    descrizione=request.form['descrizione']
    cursor=connection.cursor()
    sql="SELECT IDGenere FROM A_Genere WHERE nome=%s"
    cursor.execute(sql, (nome, ))
    result=cursor.fetchone()
    print(result[0])
    sql="INSERT INTO A_Libro (Titolo, Autore, Link, Copertina, descrizione, IDGenere) VALUES (%s, %s, %s, %s, %s, %s)"
    print(sql)
    cursor.execute(sql, (Titolo, Autore, Link, Copertina, descrizione, result[0]))
    connection.commit()
    cursor.close()
    return redirect("/catalogo")


app.run(host='0.0.0.0', port=81)
