import hashlib
import sqlite3
import json
import os

salt = "library"

### Borra la base de datos
if os.path.exists("datos.db"):
	os.remove("datos.db")

con = sqlite3.connect("datos.db")
cur = con.cursor()

### Crea la base de datos
cur.execute("""
	CREATE TABLE Session(
		session_hash varchar(32) primary key,
		user_id integer,
		last_login float,
		FOREIGN KEY(user_id) REFERENCES User(id)
	)
""")

cur.execute("""
	CREATE TABLE Book(
		id integer primary key AUTOINCREMENT,
		title varchar(50),
		author integer,
		cover varchar(50),
		description TEXT,
		FOREIGN KEY(author) REFERENCES Author(id)
	)
""")

cur.execute("""
	CREATE TABLE Theme(
		id integer primary key AUTOINCREMENT,
		name varchar(40)
	)
""")

cur.execute("""
	CREATE TABLE BookTheme(
		book_id integer,
		theme_id integer,
		FOREIGN KEY(book_id) REFERENCES Book(id),
		FOREIGN KEY(theme_id) REFERENCES Theme(id)
	)
""")

cur.execute("""
	CREATE TABLE Copy(
		id integer primary key AUTOINCREMENT,
		book_id integer,
		FOREIGN KEY(book_id) REFERENCES Book(id)
	)
""")

cur.execute("""
    CREATE TABLE Borrow(
		user_id integer,
		copy_id integer,
		borrow_date date,
		return_date date,
		FOREIGN KEY(user_id) REFERENCES User(id),
		FOREIGN KEY(copy_id) REFERENCES Copy(id)
	)
""")

cur.execute("""
	CREATE TABLE Author(
		id integer primary key AUTOINCREMENT,
		name varchar(40)
	)
""")

cur.execute("""
	CREATE TABLE User(
		id integer primary key AUTOINCREMENT,
		name varchar(20),
		email varchar(30),
		password varchar(32)
	)
""")

cur.execute("""
   CREATE TABLE Friend(
		user_id integer,
		friend_id integer,
		FOREIGN KEY(user_id) REFERENCES User(id),
		FOREIGN KEY(friend_id) REFERENCES User(id)
	)
""")

### Insert users
with open('usuarios.json', 'r') as f:
	usuarios = json.load(f)['usuarios']

for user in usuarios:
	dataBase_password = user['password'] + salt
	hashed = hashlib.md5(dataBase_password.encode())
	dataBase_password = hashed.hexdigest()
	cur.execute(f"""INSERT INTO User VALUES (NULL, '{user['nombres']}', '{user['email']}', '{dataBase_password}')""")
	con.commit()

### Insert books, copies, authors and themes
with open('libros.tsv', 'r', encoding="UTF-8") as f:
	libros = [x.split("\t") for x in f.readlines()]

for author, title, cover, description, theme in libros:
    try:
        theme = theme.strip()
        # Verificar si el autor ya existe
        res = cur.execute("SELECT id FROM Author WHERE name=?", (author,))
        author_row = res.fetchone()
        if author_row is None:
            # Si no existe, insertar el autor
            cur.execute("INSERT INTO Author VALUES (NULL, ?)", (author,))
            con.commit()
            author_id = cur.lastrowid
        else:
            # Si existe, obtener su ID
            author_id = author_row[0]

        # Verificar si el tema ya existe
        res = cur.execute("SELECT id FROM Theme WHERE name=?", (theme,))
        theme_row = res.fetchone()
        if theme_row is None:
            # Si no existe, insertar el tema
            cur.execute("INSERT INTO Theme VALUES (NULL, ?)", (theme,))
            con.commit()
            theme_id = cur.lastrowid
        else:
            # Si existe, obtener su ID
            theme_id = theme_row[0]

        # Insertar el libro
        cur.execute("INSERT INTO Book VALUES (NULL, ?, ?, ?, ?)",
					(title, author_id, cover, description.strip()))
        con.commit()
        book_id = cur.lastrowid

		# Crear tres copias del libro
        for i in range(3):
            cur.execute("INSERT INTO Copy VALUES (NULL, ?)", (book_id,))
            con.commit()

		# Asociar el libro con el tema
        cur.execute("INSERT INTO BookTheme VALUES (?, ?)", (book_id, theme_id))
        con.commit()

    except Exception as e:
        print(f"Error al procesar el libro {title}: {str(e)}")
        con.rollback()


### Insert friends
# Usuario1 friend of Usuario3
cur.execute("INSERT INTO Friend VALUES (?, ?)", (2, 4))
# Usuario2 friend of Usuario3
cur.execute("INSERT INTO Friend VALUES (?, ?)", (3, 4))
con.commit()

### Insert Borrow
# Usuario1 borrow copy1 from book1
cur.execute("INSERT INTO Borrow VALUES (?, ?, ?, ?)", (2, 1, '2022-01-01', '2022-01-15'))
# Usuario3 borrow copy7 from book3
cur.execute("INSERT INTO Borrow VALUES (?, ?, ?, ?)", (4, 7, '2022-03-01', '2022-03-15'))
con.commit()
