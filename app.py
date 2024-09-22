from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import RadioField, IntegerField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask.globals import session

from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from flask import flash

import os
app = Flask(__name__)

##Requiere crear una clave secreta para los forms
##app.config["SECRET_KEY"] = "mykeysecret"

app.config.from_mapping(
    SECRET_KEY = 'dev',
    UPLOAD_FOLDER = 'uploads'
)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


##Creamos formulario para registrar usuario
class IniciarSesion(FlaskForm):
    username = StringField("Nombre de usuario:", validators=[DataRequired(),Length(min=4, max=25)])
    password = PasswordField("Password:", validators=[DataRequired(),Length(min=8, max=15)])
    submit = SubmitField("Iniciar sesión")    

class RegistrarMascota(FlaskForm):
    responsable_nombre  = StringField("Nombre de responsable:")
    responsable_id      = IntegerField("Numero de ID:")
    mascota_nombre      = StringField("Nombre de la mascota:")
    mascota_sexo        = RadioField("Selecciona el sexo",
                                     choices=[('0','Macho'),('1','Hembra')])
    mascota_raza        = StringField("Raza:")
    mascota_peso        = IntegerField("Peso:")
    mascota_apoyo_emocional  = RadioField("¿Es de apoyo emocional?",
                                           choices=[('0','Si'),('1','No')])
    submit = SubmitField("Registrar") 

class cargarArchivo(FlaskForm):
    file = FileField("Seleccionar archivo:")
    submit = SubmitField("Cargar Archivo")

@app.route('/')
def pagina_principal():
    usuario = {}
    if 'usuario' in session:
        usuario = session['usuario']

    return render_template('index.html', usuario=usuario)

@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def pagina_inicio_sesion():
    # username = ''
    # password = ''
    usuario = {
        'username' : '',
        'password' : ''
    }
    ##Instanciamos IniciarSesion en form
    form = IniciarSesion()
    ##Obtenemos datos del forms
    
    
    if form.validate_on_submit():
        # username = form.username.data
        # password = form.password.data
        usuario['username'] = form.username.data
        usuario['password'] = form.password.data
    session['usuario'] = usuario
    return render_template('iniciar_sesion.html', form=form, username=usuario['username'],password=usuario['password'])
    #return render_template('iniciar_sesion.html', form=form, username=username,password=password)
   

@app.route('/registro_mascota', methods=['GET','POST'])
def pagina_registro_mascotas():
    #instanciamos RegistrarMascota en form
    form = RegistrarMascota()
    #Obtenemos datos del form:
    
    if form.validate_on_submit():
        responsable_nombre     = form.responsable_nombre.data
        responsable_id          = form.responsable_id.data
        mascota_nombre         = form.mascota_nombre.data
        mascota_sexo           = form.mascota_sexo.data
        mascota_raza           = form.mascota_raza.data
        mascota_peso           = form.mascota_peso.data
        mascota_apoyo_emocional= form.mascota_apoyo_emocional.data

        return f"""Datos registrados: {responsable_nombre},{responsable_id},{mascota_nombre},{mascota_sexo},{mascota_raza},{mascota_peso},{mascota_apoyo_emocional}"""
        

    return render_template("registro_mascota.html", form=form)

@app.route('/cargar_archivo', methods=["POST","GET"])
def cargar_archivo():
    form = cargarArchivo()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        try:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        except ValueError as error:
            return f"error: {error} path:{os.path.join(app.config['UPLOAD_FOLDER'], filename)}"
    return render_template("cargar_archivo.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)