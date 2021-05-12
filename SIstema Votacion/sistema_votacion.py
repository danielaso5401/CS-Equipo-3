from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:12345678@127.0.0.1:8081/sistema_votacion"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # par q no de warnings

db = SQLAlchemy(app)
ma = Marshmallow(app)



class Roles(db.Model):
    idroles = db.Column(db.Integer, primary_key=True)
    roles_descripcion = db.Column(db.String(100))
    roles=db.relationship('Usuario', backref='roles',lazy=True)
    def __init__(self, roles_descripcion):
        self.roles_descripcion=roles_descripcion

class Usuario(db.Model):
    idusuario = db.Column(db.Integer, primary_key=True)
    usuario_name = db.Column(db.String(100))
    usuario_usuario = db.Column(db.String(100))
    usuario_contraseña = db.Column(db.String(100))
    roles_idRoles = db.Column(db.Integer,db.ForeignKey('roles.idroles'),nullable=False)
    def __init__(self, usuario_name, usuario_usuario, usuario_contraseña,roles_idRoles):
        self.usuario_name = usuario_name
        self.usuario_usuario = usuario_usuario
        self.usuario_contraseña = usuario_contraseña
        self.roles_idRoles = roles_idRoles

class Elector(db.Model):
    id_elector = db.Column(db.Integer, primary_key=True)
    elector_name = db.Column(db.String(100))
    elector_dni = db.Column(db.String(8))
    elector_huella = db.Column(db.String(100))
    ubigeo_idUbigeo = db.Column(db.Integer,db.ForeignKey('ubigeo.idubigeo'),nullable=False)

    def __init__(self,elector_name,elector_dni,elector_huella,ubigeo_idUbigeo):
        self.elector_name=elector_name
        self.elector_dni=elector_dni
        self.elector_huella=elector_huella
        self.ubigeo_idUbigeo = ubigeo_idUbigeo

class Ubigeo(db.Model):
    idubigeo = db.Column(db.Integer, primary_key=True)
    ubigeo_distrito= db.Column(db.String(45))
    ubigeo_ciudad= db.Column(db.String(45))
    ubigeo_pais= db.Column(db.String(45))
    electores = db.relationship('Elector', backref='ubigeo', lazy=True)

    def __init__(self,ubigeo_distrito,ubigeo_ciudad,ubigeo_pais):
        self.ubigeo_distrito= ubigeo_distrito
        self.ubigeo_ciudad= ubigeo_ciudad
        self.ubigeo_pais= ubigeo_pais



class Candidato(db.Model):
    idCandidato = db.Column(db.Integer, primary_key=True)
    candidato_name = db.Column(db.String(100))
    candidato_dni = db.Column(db.String(8))
    candidato_partpol = db.Column(db.String(100))
    candidato_fotocant = db.Column(db.String(100))
    candidato_fotopart = db.Column(db.String(100))

    def __init__(self, candidato_name, candidato_dni, candidato_partpol, candidato_fotocant, candidato_fotopart):
        self.candidato_name = candidato_name
        self.candidato_dni = candidato_dni
        self.candidato_partpol = candidato_partpol
        self.candidato_fotocant = candidato_fotocant
        self.candidato_fotopart = candidato_fotopart

db.create_all()

class RolesSchema(ma.Schema):
    class Meta:
        fields = ('idroles','roles_descripcion')

roles_schema = RolesSchema()
roles_schemas = RolesSchema(many=True)

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('idusuario','usuario_name','usuario_usuario','usuario_contraseña',"roles_idRoles")

usuario_schema = UsuarioSchema()
usuario_schemas = UsuarioSchema(many=True)

class ElectorSchema(ma.Schema):
    class Meta:
        fields = ('id_elector',"elector_name","elector_dni","elector_huella","ubigeo_idUbigeo")

elector_schema = ElectorSchema()
elector_schemas = ElectorSchema(many=True)

class UbigeoSchema(ma.Schema):
    class Meta:
        fields = ("idubigeo","ubigeo_distrito", "ubigeo_ciudad", "ubigeo_pais")

ubigeo_schema = UbigeoSchema()
ubigeo_schemas = UbigeoSchema(many=True)

class CandidatoSchema(ma.Schema):
    class Meta:
        fields = ("idCandidato","candidato_name", "candidato_dni", "candidato_partpol", "candidato_fotocant", "candidato_fotopart")

candidato_schema = CandidatoSchema()
candidato_schemas = CandidatoSchema(many=True)


@app.route('/create_roles', methods=['POST'])
def create_roles():
    print(request.json)

    roles_descripcion = request.json['roles_descripcion']
    new_rol = Roles(roles_descripcion)
    db.session.add(new_rol)
    db.session.commit()

    return roles_schema.jsonify(new_rol)

@app.route('/get_roles', methods=['GET'])
def roles():
    all_roles = Roles.query.all()
    result = roles_schemas.dump(all_roles)
    return jsonify(result)

@app.route('/create_usuario', methods=['POST'])
def create_usuario():
    print(request.json)

    usuario_name=request.json['usuario_name']
    usuario_usuario=request.json['usuario_usuario']
    usuario_contraseña=request.json['usuario_contraseña']
    roles_idRoles=request.json['roles_idRoles']

    new_usuario = Usuario(usuario_name,usuario_usuario,usuario_contraseña,roles_idRoles)

    db.session.add(new_usuario)
    db.session.commit()

    return usuario_schema.jsonify(new_usuario)

@app.route('/get_usuario', methods=['GET'])
def usuarios():
    all_usuarios = Usuario.query.all()
    result = usuario_schemas.dump(all_usuarios)
    return jsonify(result)

@app.route('/create_elector', methods=['POST'])
def create_elector():
    print(request.json)
    elector_name=request.json["elector_name"]
    elector_dni=request.json["elector_dni"]
    elector_huella=request.json["elector_huella"]
    ubigeo_idUbigeo=request.json['ubigeo_idUbigeo']

    new_elector = Elector(elector_name,elector_dni,elector_huella,ubigeo_idUbigeo)

    db.session.add(new_elector)
    db.session.commit()

    return elector_schema.jsonify(new_elector)

@app.route('/get_elector', methods=['GET'])
def electores():
    all_electores = Elector.query.all()
    result = elector_schemas.dump(all_electores)
    return jsonify(result)

@app.route('/create_ubigeo', methods=['POST'])
def create_ubigeo():
    print(request.json)
    ubigeo_distrito=request.json["ubigeo_distrito"]
    ubigeo_ciudad=request.json["ubigeo_ciudad"]
    ubigeo_pais=request.json["ubigeo_pais"]


    new_ubigeo = Ubigeo(ubigeo_distrito,ubigeo_ciudad,ubigeo_pais)

    db.session.add(new_ubigeo)
    db.session.commit()

    return ubigeo_schema.jsonify(new_ubigeo)

@app.route('/get_ubigeo', methods=['GET'])
def ubigeos():
    all_ubigeos = Ubigeo.query.all()
    result = ubigeo_schemas.dump(all_ubigeos)
    return jsonify(result)

@app.route('/create_candidato', methods=['POST'])
def create_candidato():
    print(request.json)
    candidato_name=request.json["candidato_name"]
    candidato_dni=request.json["candidato_dni"]
    candidato_partpol=request.json["candidato_partpol"]
    candidato_fotocant=request.json["candidato_fotocant"]
    candidato_fotopart=request.json["candidato_fotopart"]

    new_candidato = Candidato(candidato_name, candidato_dni, candidato_partpol, candidato_fotocant, candidato_fotopart)

    db.session.add(new_candidato)
    db.session.commit()

    return candidato_schema.jsonify(new_candidato)

@app.route('/get_candidato', methods=['GET'])
def candidatos():
    all_candidatos = Candidato.query.all()
    result = candidato_schemas.dump(all_candidatos)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=8002)
