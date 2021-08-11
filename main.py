#Importacion de librerias
import psycopg2
from flask import Flask, render_template, request, url_for, redirect

from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy

#creacion de objeto de tipo flask

app = Flask(__name__, static_url_path='/static')

#conexion de mysql
db = SQLAlchemy(app)
conn = psycopg2.connect(
    host="ec2-34-228-100-83.compute-1.amazonaws.com",
    database="d8g14uqvcj54pd",
    user="pxdoxruuqshtup",
    password="3751dae87212b13d06c20be2201e22759da7fef31df081a1b1151d82a79ed73d"
)

app = Flask(__name__, static_url_path='/static')
#Creacion de ruta raiz para la pagina principal
@app.route('/')
#Creacion de funcion para mostrar el index
def index():

    return render_template('index.html')

@app.route("/rejilla")
def rejilla_html():
    return render_template("html_rejilla.html")


@app.route("/compra")
def compra_html():

    #conn = mysql.connect(app)
    connectar = conn.cursor()

    connectar.execute("SELECT * FROM cotizacion")

    datos = connectar.fetchall()

    print(datos)
    connectar.close()
    return render_template("compra.html", lista_productos=datos)


@app.route("/guardar_formulario", methods=["POST"])
def guardar_formulario():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    email = request.form["email"]
    producto = request.form["producto"]
    descripcion = request.form["descripcion"]

    #abrimos una conexion
    #crea una interaccion a la conexion de la bd
    connectar = conn.cursor()
    #crea una interaccion a la conexion de la bd
    connectar.execute("INSERT INTO cotizacion (nombre, apellido, email, producto, descripcion) VALUES(%s,%s,%s,%s,%s)",
                      (nombre, apellido, email, producto, descripcion))


    #actualiza la conexion
    conn.commit()
    #cerramos la iteraccion y limpia la conexion para que quede vacia
    connectar.close()

    #return "Dato insertado: "  +  nombre  +  "  "  +  apellido  + "  " +  producto  +  "   "  +  email  +  "  "  +  descripcion
    return redirect("/compra")

@app.route("/eliminar_producto/<string:id>")
def eliminar_producto(id):

    connectar = conn.cursor()

    connectar.execute("DELETE FROM cotizacion WHERE id={0}".format(id))
    conn.commit()
    connectar.close()

    return redirect("/compra")

@app.route("/consultar_producto/<id>")
def consultar_producto(id):

    connectar = conn.cursor()

    connectar.execute("SELECT * FROM cotizacion where id= %s", (id))
    dato = connectar.fetchone()
    print(dato)
    connectar.close()

    return render_template("form_editar_producto.html", producto=dato)

@app.route("/editar_producto/<id>", methods=['POST'])
def editar_producto(id):
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    email = request.form["email"]
    producto = request.form["producto"]
    descripcion = request.form["descripcion"]

    connectar = conn.cursor()
    connectar.execute("UPDATE cotizacion SET nombre=%s, apellido=%s, email=%s, producto=%s, descripcion=%s WHERE id=%s", (nombre, apellido, email, producto, descripcion, id))
    conn.commit()
    connectar.close()

    return redirect("/compra")

@app.route("/Bootstrap")
def Bootstrap_html():
    return render_template("Bootstrap.html")


#Definicion del archivo principal de ejecucion
if __name__ == '__main__':
    #Configuracion del puerto de escucha del servidor web
    app.run(port=80,debug=True)
