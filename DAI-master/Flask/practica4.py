# -*- coding: utf-8 -*-
import re
from flask import Flask,request, url_for,render_template,redirect
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

mongoClient = MongoClient('localhost',27017)
@app.route("/")
def web_incial():
	db = mongoClient.test
	collection = db.restaurants
	cursor = collection.find()
	datos = {"cursor":cursor}
	return render_template('full4.html',contenido=datos)

@app.route("/delete",methods = ['POST'])
def borrar_restaurante():
	id=str(request.form['but'])
	db = mongoClient.test
	collection = db.restaurants
	result = collection.delete_many({"restaurant_id":id})
	return redirect(url_for('web_incial'))

@app.route("/edit_restaurant",methods = ['POST'])
def formulario_editar_restaurante():
	id=str(request.form['but1'])
	db = mongoClient.test
	collection = db.restaurants
	result = collection.find({"restaurant_id":id})
	datos = {"cursor":result}
	return render_template('edit4.html',contenido = datos)

@app.route("/editar",methods = ['POST'])
def editar_restaurante():
	nombre=str(request.form['nomb'])
	cocina=str(request.form['cocina'])
	calle=str(request.form['calle'])
	barrio=str(request.form['barrio'])
	edificio=str(request.form['edificio'])
	id=str(request.form['aux'])
	db = mongoClient.test
	collection = db.restaurants
	collection.update({'restaurant_id':id},{'$set' : {'name':nombre}},upsert=False,multi=False)
	collection.update({'restaurant_id':id},{'$set' : {'cuisine':cocina}},upsert=False,multi=False)
	collection.update({'restaurant_id':id},{'$set' : {'borough':barrio}},upsert=False,multi=False)
	collection.update({'restaurant_id':id},{'$set' : {'address.street':calle}},upsert=False,multi=False)
	collection.update({'restaurant_id':id},{'$set' : {'address.building':edificio}},upsert=False,multi=False)
	return redirect(url_for('web_incial'))

@app.route("/filtrado",methods = ['POST'])
def filtrar():
	campo = str(request.form['campo'])
	palabra = str(request.form['filtro'])
	db = mongoClient.test
	collection = db.restaurants
	result = collection.find({campo:{'$regex':'.*' + palabra + '.*'}})
	datos = {"cursor":result}
	return render_template('full4.html',contenido = datos)

@app.route("/add_rest")
def formulario_ingresar_restaurante():
	datos = {}
	return render_template('add4.html',contenido = datos)	
	
@app.route("/add",methods = ['POST'])	
def igresar_restaurante():
	nombre = str(request.form['nombre'])
	id = str(request.form['id'])
	barrio = str(request.form['barrio'])
	edificio = str(request.form['edificio'])
	lat = request.form['latitud']
	long = request.form['longitud']
	cocina = str(request.form['cocina'])
	cod = str(request.form['codigopostal'])
	calle = str(request.form['calle'])

	db = mongoClient.test
	collection = db.restaurants
	result = collection.insert_one(
	{
		"address": {
			"street": calle,
			"zipcode": cod,
			"building": edificio,
			"coord": [lat, long]
		},
		"borough": barrio,
		"cuisine": cocina,
		"grades": [

		],
		"name": nombre,
		"restaurant_id": id
	}
	)
	return redirect(url_for('web_incial'))

@app.errorhandler(404)
def page_not_found(error):
	return "Página no encontrada", 404

if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)