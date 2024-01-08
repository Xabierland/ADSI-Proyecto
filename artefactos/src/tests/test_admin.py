from . import BaseTestClass
from bs4 import BeautifulSoup

class TestAdmin(BaseTestClass):
    def test_entrarFuncionAdminSinSer(self):
        """Comprueba que no se muestra la pantalla de administrador si el admin no esta logeado"""
        res = self.client.get('/administrador')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features='html.parser')

        # Se tiene que mostrar el siguiente h2: ¡No tienes acceso, no eres administrador!
        text = "¡No tienes acceso, no eres administrador!"
        self.assertEqual(1, len(page.find_all(lambda tag: tag.name == "h2" and text in tag.text)))

    def test_entrarFuncionAdminSiendo(self):
        """Comprueba que se muestra la pantalla de administrador si el admin esta logeado"""
        self.login("admin@gmail.com","admin")
        res = self.client.get('/administrador')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features='html.parser')

        # Se tiene que mostrar el siguiente h1: Opciones de administrador
        text = "Opciones de administrador"
        self.assertEqual(1, len(page.find_all(lambda tag: tag.name == "h1" and text in tag.text)))

    def test_crearUsuarioCampos(self):
        """Comprueba si los campos necesarios para crear un usuario están presentes en la página de crear usuario"""
        # Inicio de sesion de admin
        self.login("admin@gmail.com","admin")

        res = self.client.get('/crearUsuario')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features = "html.parser")
        self.assertIsNotNone(page.find('form').find('input', id = 'nombre'))
        self.assertIsNotNone(page.find('form').find('input', id = 'apellidos'))
        self.assertIsNotNone(page.find('form').find('input', id = 'fecha_nac'))
        self.assertIsNotNone(page.find('form').find('input', id = 'email'))
        self.assertIsNotNone(page.find('form').find('input', id = 'contrasena'))
        self.assertIsNotNone(page.find('form').find('input', id = 'repetirContrasena'))
        self.assertIsNotNone(page.find('form').find('button', type = 'submit'))

    def test_crearUsuariosBien(self):
        """Comprueba que se crea un usuario correctamente"""
        # Inicio de sesion de admin
        self.login("admin@gmail.com","admin")

        nombre = "Prueba"
        apellidos = "Unitaria"
        fecha_nac = '2000-01-01'
        email = "pruebaunitaria@gmail.com"
        password= "pruebaunitaria"
        res1 = self.crearUsuario(nombre,apellidos,fecha_nac,email,password)
        self.assertEqual(302, res1.status_code)
        text = "Usuario%20creado%20correctamente"
        self.assertEqual('/msg?mensaje=' + text, res1.location)
        res2 = self.db.select(f"SELECT name,last_name,birth_date,email,password FROM User WHERE email='{email}'")
        self.assertEqual(1,len(res2))
        self.assertEqual(nombre,res2[0][0])
        self.assertEqual(apellidos,res2[0][1])
        self.assertEqual(fecha_nac,res2[0][2])
        self.assertEqual(email,res2[0][3])
        self.borrarUsuario(email)

    def test_noCreaUsuario(self):
        """Prueba que verifica el comportamiento al crear un usuario que ya existe"""
        # Inicio de sesion de admin
        self.login("admin@gmail.com","admin")

        nombre = "Usuario1"
        apellidos = "Sistema"
        fecha_nac ='1990-01-01'
        email ="user1@gmail.com"
        password = "user1"
        res = self.crearUsuario(nombre,apellidos,fecha_nac,email,password)
        self.assertEqual(302, res.status_code)
        text1 = "Usuario%20ya%20existe"
        self.assertEqual('/msg?mensaje=' + text1, res.location)
    
    def test_borrarUsuarioCampos(self):
        """Comprueba si los campos necesarios para borrar un usuario están presentes en la página de borrar usuario"""
        # Inicio de sesion de admin
        self.login("admin@gmail.com","admin")

        res = self.client.get('/borrarUsuario')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertIsNotNone(page.find('form').find('input', id='email'))
        self.assertIsNotNone(page.find('form').find('button', type='submit'))

    def test_borrarUsuarioBien(self):
        """Comprueba que se borra un usuario correctamente"""
        # Inicio de sesion de admin
        self.login("admin@gmail.com","admin")

        nombre = "Prueba"
        apellidos = "Unitaria"
        fecha_nac ='2000-01-01'
        email ="pruebaunitaria@gmail.com"
        password = "pruebaunitaria"
        self.db.insert(f"INSERT INTO User (name,last_name,birth_date,email,password) VALUES ('{nombre}','{apellidos}','{fecha_nac}','{email}','{password}')")
        res = self.borrarUsuario(email)
        self.assertEqual(302, res.status_code)
        text = "Usuario%20borrado%20correctamente"
        self.assertEqual('/msg?mensaje=' + text, res.location)

    def test_noBorraUsuario(self): 
        """Commprueba que no se borra un usuario que no existe o que es admin"""
        # Inicio de sesion de admin
        self.login("admin@gmail.com","admin")

        # Se intenta borrar un usuario que no existe
        email1 = "noborrausuario@pruebaunitaria.com"
        res1 = self.borrarUsuario(email1)
        self.assertEqual(302, res1.status_code)
        text = "El%20email%20no%20existe%20o%20es%20admin" 
        self.assertEqual('/msg?mensaje=' + text, res1.location)

        # Se intenta borrar el usuario admin
        email2 = "admin@gmail.com"
        res2 = self.borrarUsuario(email2)
        self.assertEqual(302, res2.status_code)
        text2 = "El%20email%20no%20existe%20o%20es%20admin" 
        self.assertEqual('/msg?mensaje=' + text2, res2.location)

    def test_añadirLibroCampos(self):         
        """Comprueba si los campos necesarios para añadir un libro están presentes en la página de añadir libro"""
        # Inicio de sesion de admin
        self.login("admin@gmail.com","admin")

        res = self.client.get('/añadirLibro')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertIsNotNone(page.find('form').find('input', id='titulo'))
        self.assertIsNotNone(page.find('form').find('input', id='autor'))
        self.assertIsNotNone(page.find('form').find('input', id='cover'))
        self.assertIsNotNone(page.find('form').find('input', id='descripcion'))
        self.assertIsNotNone(page.find('form').find('button', type='submit'))

    def test_añadirLibroBien(self):
        """Comprueba que se añade un libro correctamente"""
        # Inicio de sesion de admin
        self.login("admin@gmail.com","admin")

        titulo = "Prueba Unitaria"
        autor = "Prueba Unitaria"
        cover = "https://scontent.fbio3-2.fna.fbcdn.net/v/t1.6435-9/170326123_289022702599572_7782433131700673715_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=dd63ad&_nc_ohc=8uj4olDX-ekAX_fiwgY&_nc_ht=scontent.fbio3-2.fna&oh=00_AfBJ0gdk5h6vJI57lqUoLpZ4s46fuVomMeZkTOovpJuY9w&oe=65C3B3E2"
        descripcion = "Prueba Unitaria"

        # Comprueba que se redirige a la pagina de mensaje correcta
        res1 = self.añadirLibro(titulo,autor,cover,descripcion)
        self.assertEqual(302, res1.status_code)
        text = "El%20libro%20se%20ha%20a%C3%B1adido%20correctamente"
        self.assertEqual('/msg?mensaje=' + text, res1.location)

        # Comprueba que el libro esta en la base de datos
        res2 = self.db.select(f"SELECT title,author,cover,description FROM Book WHERE title='{titulo}'")
        autor_id = self.db.select(f"SELECT id FROM Author WHERE name='{autor}'")
        self.assertEqual(1,len(res2))
        self.assertEqual(titulo,res2[0][0])
        self.assertEqual(autor_id[0][0],res2[0][1])
        self.assertEqual(cover,res2[0][2])
        self.assertEqual(descripcion,res2[0][3])
        self.borrarLibro(titulo,autor)

    def test_BorrarLibroCampos(self):
        """Comprueba si los campos necesarios para borrar un libro están presentes en la página de borrar libro"""
        # Inicio de sesion de admin
        self.login("admin@gmail.com","admin")

        res = self.client.get('/borrarLibro')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertIsNotNone(page.find('form').find('input', id='titulo'))
        self.assertIsNotNone(page.find('form').find('input', id='autor'))
        self.assertIsNotNone(page.find('form').find('button', type='submit'))

    def test_borrarLibroBien(self):
        """Comprueba que se borra un libro correctamente"""
        # Inicio de sesion de admin
        self.login("admin@gmail.com","admin")

        titulo = "Prueba Unitaria"
        autor = "Prueba Unitaria"
        cover = "https://scontent.fbio3-2.fna.fbcdn.net/v/t1.6435-9/170326123_289022702599572_7782433131700673715_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=dd63ad&_nc_ohc=8uj4olDX-ekAX_fiwgY&_nc_ht=scontent.fbio3-2.fna&oh=00_AfBJ0gdk5h6vJI57lqUoLpZ4s46fuVomMeZkTOovpJuY9w&oe=65C3B3E2"
        descripccion = "Prueba Unitaria"
        self.añadirLibro(titulo,autor,cover,descripccion)
        res = self.borrarLibro(titulo,autor)
        self.assertEqual(302, res.status_code)
        text = "El%20libro%20se%20ha%20borrado%20correctamente"
        self.assertEqual('/msg?mensaje=' + text, res.location)

    def test_noBorraLibro(self):
        """Comprueba que no se borra un libro que no existe"""
        # Inicio de sesion de admin
        self.login("admin@gmail.com","admin")

        titulo = "Prueba Unitaria"
        autor = "Prueba Unitaria"
        res = self.borrarLibro(titulo,autor)
        self.assertEqual(302, res.status_code)
        text = "El%20libro%20no%20existe"
        self.assertEqual('/msg?mensaje=' + text, res.location)