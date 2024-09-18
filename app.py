from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def pagina_principal():
    return render_template('index.html')


@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def pagina_inicio_sesion():
    return render_template('iniciar_sesion.html')
   

@app.route('/registro_mascota')
def pagina_registro_mascotas():
    return render_template("registro_mascota.html")

@app.route('/modelo_ifrs')
def pagina_modelo_ifrs():
    return render_template("modelo_ifrs.html")


if __name__ == '__main__':
    app.run()