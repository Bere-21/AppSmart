#Importacion de librerias
from flask import Flask,render_template
#creacion de objeto de tipo flask
app = Flask(__name__)
#Creacion de ruta raiz para la pagina principal
@app.route('/')
#Creacion de funcion para mostrar el index
def index():

    return render_template('index.html')


#Definicion del archivo principal de ejecucion
if __name__ == '__main__':
    #Configuracion del puerto de escucha del servidor web
    app.run(port=80,debug=True)
