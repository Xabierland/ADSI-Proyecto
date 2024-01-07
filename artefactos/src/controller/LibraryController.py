import random
from model import Connection, Book, User
from model.tools import hash_password

db = Connection()

class LibraryController:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(LibraryController, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance


	def search_books(self, title="", author="", limit=6, page=0):
		count = db.select("""
				SELECT count() 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
		""", (f"%{title}%", f"%{author}%"))[0][0]
		res = db.select("""
				SELECT b.* 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
				LIMIT ? OFFSET ?
		""", (f"%{title}%", f"%{author}%", limit, limit*page))
		books = [
			Book(b[0],b[1],b[2],b[3],b[4])
			for b in res
		]
		return books, count

	def get_user(self, email, password):
		user = db.select("SELECT * from User WHERE email = ? AND password = ?", (email, hash_password(password)))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4], user[0][6])
		else:
			return None

	def get_user_cookies(self, token, time):
		user = db.select("SELECT u.* from User u, Session s WHERE u.id = s.user_id AND s.last_login = ? AND s.session_hash = ?", (time, token))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4], user[0][6])
		else:
			return None
		 
	# === Recomendaciones del sistema ===
	def get_recommended_books(self, user=None):
		if user is None:
			"""Si no hay usuario del que obtener recomendaciones, se obtienen libros aleatorios"""
			res = db.select("""
				SELECT b.* 
				FROM Book b, Author a 
				WHERE b.author=a.id 
				ORDER BY RANDOM() LIMIT 3
			""")
			books = [
				Book(b[0],b[1],b[2],b[3],b[4])
				for b in res
			]
			return books
		else:
			"""En caso de que haya un usuario, se obtienen libros recomendados
			Para ello:
			  1. Se obtienen los temas de los libros que ha leido el usuario
			  2. Se obtienen los temas de los libros que ha leido los amigos del usuario
			  3. Se sacan todos los libros de los temas anteriores
			  4. Se eliminan los libros que ya ha leido el usuario
			"""
			# 1. Obtener los temas de los libros que ha leído el usuario
			user_themes = db.select("""
				SELECT DISTINCT theme_id
				FROM Borrow b, Copy c, BookTheme bt
				WHERE b.user_id = ? AND b.copy_id = c.id AND c.book_id = bt.book_id
			""", [user.id])

			# 2. Obtener los temas de los libros que han leído los amigos del usuario
			friend_themes = db.select("""
				SELECT DISTINCT theme_id
				FROM Friend f, Borrow b, Copy c, BookTheme bt
				WHERE f.user_id = ? AND f.friend_id = b.user_id AND b.copy_id = c.id AND c.book_id = bt.book_id
			""", [user.id])

			# Combinar las listas de temas
			themes = list(set().union(*user_themes, *friend_themes))

			# 3. Obtener los libros de los temas anteriores
			placeholders = ', '.join('?' for theme in themes)
			query = f"""
				SELECT b.*
				FROM Book b, BookTheme bt
				WHERE bt.book_id = b.id AND bt.theme_id IN ({placeholders})
			"""
			books = db.select(query, themes)

			# 4. Eliminar los libros que ya ha leído el usuario
			read_books = db.select("""
				SELECT c.book_id
				FROM Borrow b, Copy c
				WHERE b.user_id = ? AND b.copy_id = c.id
			""", [user.id])

			filtered_books = [book for book in books if book[0] not in {b[0] for b in read_books}]	# Tremenda linea de código

			# Devulene 0-3 libros aleatorios
			random_books = random.sample(filtered_books, min(3, len(filtered_books)))
			sorted_books = sorted(random_books, key=lambda b: b[0])
			return [ Book(b[0],b[1],b[2],b[3],b[4]) for b in sorted_books ]
	# ===================================

	def add_book(self, title, author):
		db.insert("INSERT INTO Author VALUES (NULL, ?)", (author,))
		author_id = db.select("SELECT id FROM Author WHERE name = ?", (author,))[0][0]
		db.insert("INSERT INTO Book VALUES (NULL, ?, ?, ?, ?)", (title, author_id, "", ""))

	def delete_book(self, title, author):
		author_id = db.select("SELECT id FROM Author WHERE name = ?", (author,))[0][0]
		book_id = db.select("SELECT id FROM Book WHERE title = ? AND author = ?", (title, author_id))[0][0]
		db.delete("DELETE FROM Book WHERE id = ?", (book_id,))

	def add_user(self, name, last_name, birth_date, email, password):
		db.insert("INSERT INTO User VALUES (NULL, ?, ?, ?, ?, ?, ?)", (name, last_name, birth_date, email, password, 0))

	def delete_user(self, email):
		db.delete("DELETE FROM User WHERE email = ?", (email,))
	