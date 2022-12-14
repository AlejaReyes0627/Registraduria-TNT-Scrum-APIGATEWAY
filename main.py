from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import create_access_token, verify_jwt_in_request
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from waitress import serve
import datetime
import requests
import re


app = Flask(__name__)
cors = CORS(app)
# Metodo login
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def create_token():
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-security"]+'/usuarios/validar'
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        user = response.json()
        expires = datetime.timedelta(seconds=60 * 60*24)
        access_token = create_access_token(
            identity=user, expires_delta=expires)
        return jsonify({"token": access_token, "user_id": user["_id"]})
    else:
        return jsonify({"msg": "Bad username or password"}), 401


#######################################################
@app.before_request
def before_request_callback():
    print("1")
    endPoint=limpiarURL(request.path)
    excludedRoutes=["/login"]
    if excludedRoutes.__contains__(request.path):
        print("ruta excluida ",request.path)
        pass
    elif verify_jwt_in_request():
        usuario = get_jwt_identity()
        if usuario["rol"]is not None:
            print("2")
            tienePersmiso=validarPermiso(endPoint,request.method,usuario["rol"]["_id"])
            if not tienePersmiso:
                return jsonify({"message": "Permission denied"}), 401
        else:
            return jsonify({"message": "Permission denied"}), 401
        
def limpiarURL(url):
    partes = request.path.split("/")
    for laParte in partes:
        if re.search('\\d', laParte):
            url = url.replace(laParte, "?")
    return url

def validarPermiso(endPoint,metodo,idRol):
    print("3")
    url=dataConfig["url-backend-security"]+"/permisos-roles/validar-permiso/rol/"+str(idRol)
    print(idRol)
    print(url)
    tienePermiso=False
    headers = {"Content-Type": "application/json; charset=utf-8"}
    body={
        "url":endPoint,
        "metodo":metodo
    }
    print(body)
    response = requests.get(url,json=body, headers=headers)
    print("4")
    try:
        data=response.json()
        print("5")
        if("_id" in data):
            tienePermiso=True
            print("6")
    except:
        pass
    return tienePermiso
##################################CANDIDATOS########################################


@app.route("/candidatos",methods=['GET'])
def getUsuarios():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/candidatos'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/candidatos",methods=['POST'])
def crearUsuario():
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/candidatos'
    response = requests.post(url, headers=headers,json=data)
    json = response.json()
    print(json)
    return jsonify(json)

@app.route("/candidatos/<string:id>",methods=['GET'])
def getUsuario(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/candidatos/'+id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/candidatos/<string:id>",methods=['PUT'])
def modificarUsuario(id):
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/candidatos/'+id
    response = requests.put(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)

@app.route("/candidatos/<string:id>",methods=['DELETE'])
def eliminarUsuario(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/candidatos/' + id
    print(url)
    response =requests.delete(url, headers=headers)
    return jsonify(response.status_code==204)

@app.route("/candidatos/<string:id>/partidos/<string:id2>",methods=['PUT'])
def editarUsuario(id,id2):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + "/candidatos/" + id + "/partidos/" + id2
    print(url)
    response =requests.put(url, headers=headers)
    return jsonify(response.status_code==204)

#################################MESAS#########################################


@app.route("/mesas",methods=['GET'])
def getMesas():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/mesas'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/mesas",methods=['POST'])
def crearMesas():
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/mesas'
    response = requests.post(url, headers=headers,json=data)
    json = response.json()
    print(json)
    return jsonify(json)

@app.route("/mesas/<string:id>",methods=['GET'])
def getMesas2(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/mesas/'+id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/mesas/<string:id>",methods=['PUT'])
def modificarMesas(id):
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/mesas/'+id
    response = requests.put(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)

@app.route("/mesas/<string:id>",methods=['DELETE'])
def eliminarMesas(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/mesas/' + id
    print(url)
    response =requests.delete(url, headers=headers)
    return jsonify(response.status_code==204)

#################################RESULTADOS#########################################

@app.route("/resultados",methods=['GET'])
def getResultados():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/resultados'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/resultados/candidatos/<string:cedula_candidato>/mesas/<string:numero_mesa>",methods=['POST'])
def crearResultados():
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/resultados/candidatos/<string:cedula_candidato>/mesas/<string:numero_mesa'
    response = requests.post(url, headers=headers,json=data)
    json = response.json()
    print(json)
    return jsonify(json)


#################################PARTIDOS#########################################


@app.route("/partidos", methods=['GET'])
def getUsuarios4():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/partidos'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)


@app.route("/partidos", methods=['POST'])
def crearUsuario6():
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/partidos'
    response = requests.post(url, headers=headers, json=data)
    json = response.json()
    print(json)
    return jsonify(json)


@app.route("/partidos/<string:id>", methods=['GET'])
def getUsuario2(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/partidos/'+id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)


@app.route("/partidos/<string:id>", methods=['PUT'])
def modificarUsuario234(id):
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/partidos/'+id
    response = requests.put(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)


@app.route("/partidos/<string:id>", methods=['DELETE'])
def eliminarUsuario77657(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-resgistraduria"] + '/partidos/' + id
    print(url)
    response = requests.delete(url, headers=headers)
    return jsonify(response.status_code == 204)


@app.route("/", methods=['GET'])
def test():
    json = {}
    json["message"] = "Server running ..."
    return jsonify(json)


def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data


if __name__ == '__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" +
          str(dataConfig["port"]))
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])
