# -*- coding: utf-8 -*-
from flask import Flask,request, url_for,render_template,session,redirect
import shelve

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'


def addweb(url):
	try:
		if session['USER'] != None:
			session['VISIT'].insert(session['COUNT'],url)
			session['COUNT'] = session['COUNT'] + 1
			if session['COUNT'] > 3 :
				session['COUNT'] = session['COUNT'] - 1
			if len(session['VISIT']) > 3:
				session['VISIT'].pop(0)
	except Exception as e:
		print e

@app.route("/")
def hello():
	datos={'logo':'logo.png','header':' HELLO WORLD!!! ','menu':[{'text':'HOME','link':'/'},{'text':'SIGN UP','link':'/reg'},{'text':'VISITED WEBS','link':'/visited'},{'text':'EDIT PROFILE','link':'/edit'},{'text':'VIEW PROFILE','link':'/view'}]}
	addweb("/hello")
	return render_template('index3.html',contenido=datos)

@app.route("/reg")
def reg():
	datos = {'logo':'logo.png','header':' SIGN UP ','menu':[{'text':'HOME','link':'/'},{'text':'VISITED WEBS','link':'/visited'},{'text':'EDIT PROFILE','link':'/edit'},{'text':'VIEW PROFILE','link':'/view'}]}
	addweb("/reg")
	return render_template('signup.html',contenido=datos)

@app.route("/view")
def view():
	try:
		stockname_file = shelve.open('stocknames.db')
		usu = session['USER']
		datos = {'logo':'logo.png','header':' VIEW PROFILE ','name':str(stockname_file[usu]['name']),'email':str(stockname_file[usu]['email']),'dni':str(stockname_file[usu]['dni']),'login':str(stockname_file[usu]['login']),'pass':str(stockname_file[usu]['pass']),'menu':[{'text':'HOME','link':'/'},{'text':'SIGN UP','link':'/reg'},{'text':'VISITED WEBS','link':'/visited'},{'text':'EDIT PROFILE','link':'/edit'}]}
		stockname_file.close()
		addweb("/view")
		return render_template('view.html',contenido=datos)
	except Exception as e:
		return hello()
		

@app.route("/visited")
def visited():
	datos = {'logo':'logo.png','header':' VISITED WEBSITES ','menu':[{'text':'HOME','link':'/'},{'text':'SIGN UP','link':'/reg'},{'text':'VIEW PROFILE','link':'/view'},{'text':'EDIT PROFILE','link':'/edit'}]}
	return render_template('visited.html',contenido=datos)	
	
@app.route("/edit")
def edit():
	try:
		stockname_file = shelve.open('stocknames.db')
		usu = session['USER']
		datos = {'logo':'logo.png','header':' EDIT PROFILE ','name':str(stockname_file[usu]['name']),'email':str(stockname_file[usu]['email']),'dni':str(stockname_file[usu]['dni']),'login':str(stockname_file[usu]['login']),'pass':str(stockname_file[usu]['pass']),'menu':[{'text':'HOME','link':'/'},{'text':'SIGN UP','link':'/reg'},{'text':'VISITED WEBS','link':'/visited'},{'text':'VIEW PROFILE','link':'/view'}]}
		stockname_file.close()
		addweb("/edit")
		return render_template('edit.html',contenido=datos)	
	except Exception as e:
		return hello()

@app.route("/login", methods = ['POST'])
def login():
	stockname_file = shelve.open('stocknames.db')
	usu=str(request.form['login'])
	passwd=str(request.form['pass'])
	if stockname_file.has_key(usu):
		if str(stockname_file[usu]['pass']) == passwd: 
			session['USER'] = usu
			session['VISIT'] = []
			session['COUNT'] = 0
	stockname_file.close()
	return redirect(url_for('hello'))

@app.route("/editar", methods = ['POST'])
def editar():
	stockname_file = shelve.open('stocknames.db')
	name=str(request.form['name'])
	email=str(request.form['email'])
	dni=str(request.form['dni'])
	passw=str(request.form['pass'])
	user={ 'name':name,'email':email,'dni':dni,'login':session['USER'],'pass':passw }
	stockname_file[session['USER']] = user
	stockname_file.close()
	return redirect(url_for('edit'))
	
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('hello'))
	
@app.route("/registro", methods = ['POST'])
def registrar():
	name=str(request.form['name'])
	email=str(request.form['email'])
	dni=str(request.form['dni'])
	login=str(request.form['login'])
	passw=str(request.form['pass'])
	user={ 'name':name,'email':email,'dni':dni,'login':login,'pass':passw } 
	stockname_file = shelve.open('stocknames.db')
	stockname_file[login] = user
	stockname_file.close()
	return redirect(url_for('hello'))

@app.errorhandler(404)
def page_not_found(error):
    return "Página no encontrada", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)