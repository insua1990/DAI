 # -*- coding: utf-8 -*-
from flask import Flask,request, url_for,render_template
import mandelbrot
import random
app = Flask(__name__)

@app.route("/user/pepe")
def pepe():
    return "CONTENIDO WEB ESTATICO PARA PEPE"

@app.route("/user/zerjillo")
def zerjillo():
    return "CONTENIDO WEB ESTATICO PARA ZERJILLO"

@app.route("/user/<name>")
def usuario(name):
    return "CONTENIDO WEB ESTATICO PARA EL USUARIO : " + name

@app.route("/mandelbrot" , methods = ['POST'])
def mand():
    x1 = float(request.form['x1'])
    y1 = float(request.form['y1'])
    x2 = float(request.form['x2'])
    y2 = float(request.form['y2'])
    witdh= int(request.form['witdh'])
    mandelbrot.renderizaMandelbrot(x1,y1,x2,y2,witdh,500,"static/mandelbrot.png")
    image='<img src=' + url_for('static',filename='mandelbrot.png') + ' width="50%"  >'
    return image

@app.route("/")
def hello():
    enlace='<a href=' + "http://localhost:8080/static/index2.html" + '>' + "IR A PRACTICA 2" + "</a>" 
    return enlace
	
@app.route("/svg")
def svg():
	colors=['blue','black']
	bucle=random.randint(1,100)
	imagen='<svg height="500px" width="500px">'
	for i in range(100):
		forma={'1':'<circle cx="'+str(random.randint(1,500))+'" cy="'+str(random.randint(1,500))+'" r="'+str(random.randint(1,20))+'" stroke="'+colors[random.randint(0,1)]+'" stroke-width="'+str(random.randint(1,2))+'" fill="'+colors[random.randint(0,1)] +'" />'}
		imagen=imagen+forma[str(1)]

	imagen=imagen+'</svg>'
	return imagen


@app.errorhandler(404)
def page_not_found(error):
    return "Pagina no encontrada", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)