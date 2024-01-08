from .LibraryController import LibraryController
from flask import Flask, render_template, request, make_response, redirect, flash

app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')
app.secret_key = "library"

library = LibraryController()

@app.before_request
def get_logged_user():
	if '/css' not in request.path and '/js' not in request.path:
		token = request.cookies.get('token')
		time = request.cookies.get('time')
		if token and time:
			request.user = library.get_user_cookies(token, float(time))
			if request.user:
				request.user.token = token


@app.after_request
def add_cookies(response):
	if 'user' in dir(request) and request.user and request.user.token:
		session = request.user.validate_session(request.user.token)
		response.set_cookie('token', session.hash)
		response.set_cookie('time', str(session.time))
	return response


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/catalogue')
def catalogue():
	title = request.values.get("title", "")
	author = request.values.get("author", "")
	page = int(request.values.get("page", 1))
	books, nb_books = library.search_books(title=title, author=author, page=page - 1)
	# === Recomendaciones del sistema ===
	if 'user' in dir(request) and request.user and request.user.token:
		user = request.user
		# Obtener libros recomendados
		recommended_books = library.get_recommended_books(user)
	else:
		recommended_books = []
	# ===================================
	total_pages = (nb_books // 6) + 1
	return render_template('catalogue.html', books=books, title=title, author=author, current_page=page,
	                       total_pages=total_pages, recommended_books=recommended_books, max=max, min=min)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'user' in dir(request) and request.user and request.user.token:
		return redirect('/')
	email = request.values.get("email", "")
	password = request.values.get("password", "")
	user = library.get_user(email, password)
	if user:
		session = user.new_session()
		resp = redirect("/")
		resp.set_cookie('token', session.hash)
		resp.set_cookie('time', str(session.time))
	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = render_template('login.html')
	return resp


@app.route('/logout')
def logout():
	path = request.values.get("path", "/")
	resp = redirect(path)
	resp.delete_cookie('token')
	resp.delete_cookie('time')
	if 'user' in dir(request) and request.user and request.user.token:
		request.user.delete_session(request.user.token)
		request.user = None
	return resp


@app.route('/administrador')
def administrador():
	return render_template('administrador.html')

@app.route('/gestorUsuarios')
def gestorUsuarios():
	return render_template('gestorUsuarios.html')

@app.route('/crearUsuario', methods=['GET', 'POST'])
def crearUsuario():
	if request.method == 'POST':
		nombre = request.values.get("nombre")
		apellidos = request.values.get("apellidos")
		fecha_nac= request.values.get("fecha_nac")
		email = request.values.get("email")
		password = request.values.get("password")
		mensaje = library.add_user(nombre, apellidos, fecha_nac, email, password)
		return redirect('/msg?mensaje=' + mensaje) 
	else:
		return render_template('crearUsuario.html')

@app.route('/borrarUsuario', methods=['GET', 'POST'])
def borrarUsuario():
	if request.method == 'POST':
		email = request.form.get("email")
		mensaje = library.delete_user(email)
		return redirect('/msg?mensaje=' + mensaje)
	else:
		return render_template('borrarUsuario.html')

@app.route('/gestorLibros')
def gestorLibros():
	return render_template('gestorLibros.html')

@app.route('/añadirLibro', methods=['GET', 'POST'])
def añadirLibro():
	if request.method == 'POST':
		titulo = request.form.get("titulo")
		autor = request.form.get("autor")
		cover = request.form.get("cover")
		descripccion = request.form.get("descripcion")
		library.add_book(titulo, autor, cover, descripccion)
		return redirect('/administrador')
	else:
		return render_template('añadirLibro.html')

@app.route('/borrarLibro', methods=['GET', 'POST'])
def borrarLibro():
	if request.method == 'POST':
		titulo = request.form.get("titulo")
		autor = request.form.get("autor")
		library.delete_book(titulo, autor)
		return redirect('/administrador')
	else:
		return render_template('borrarLibro.html')

@app.route('/msg', methods=['GET'])
def mensaje():
	mensaje = request.values.get("mensaje","")
	return render_template('msg.html', mensaje=mensaje)