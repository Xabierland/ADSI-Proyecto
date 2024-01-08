from . import BaseTestClass
from bs4 import BeautifulSoup

class TestAdmin(BaseTestClass):
    def test_entrarFuncionAdminSinSer(self):
        """Test para comprobar que no se muestra la pantalla de administrador"""
        res = self.client.get('/administrador')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features='html.parser')

        # Se tiene que mostrar el siguiente h2: ¡No tienes acceso, no eres administrador!
        text = "¡No tienes acceso, no eres administrador!"
        self.assertEqual(1, len(page.find_all(lambda tag: tag.name == "h2" and text in tag.text)))

    def test_entrarFuncionAdminSiendo(self):
        """Test para comprobar que se muestra la pantalla de administrador"""
        self.login("admin@gmail.com","admin")
        res = self.client.get('/administrador')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features='html.parser')

        # Se tiene que mostrar el siguiente h1: Opciones de administrador
        text = "Opciones de administrador"
        self.assertEqual(1, len(page.find_all(lambda tag: tag.name == "h1" and text in tag.text)))

    def test_crearUsuarioCampos(self):
        self.login("admin@gmail.com","admin")
        res = self.client.get('/crearUsuario')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertIsNotNone(page.find('form').find('input', id='nombre'))
        self.assertIsNotNone(page.find('form').find('input', id='apellidos'))
        self.assertIsNotNone(page.find('form').find('input', id='fecha_nac'))
        self.assertIsNotNone(page.find('form').find('input', id='email'))
        self.assertIsNotNone(page.find('form').find('input', id='contrasena'))
        self.assertIsNotNone(page.find('form').find('input', id='repetirContrasena'))
        self.assertIsNotNone(page.find('form').find('button', type='submit'))

    def test_crearUsuariosBien(self):
        nombre= "Prueba"
        apellidos= "Unitaria"
        fecha_nac='2000-01-01'
        email="pruebaunitaria@gmail.com"
        password= "pruebaunitaria"
        self.login("admin@gmail.com","admin")
        res = self.crearUsuario(nombre,apellidos,fecha_nac,email,password)
        #page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(302, res.status_code)
        text="Usuario%20creado%20correctamente"
        self.assertEqual('/msg?mensaje='+text, res.location)
        res1 = self.db.select(f"SELECT name,last_name,birth_date,email,password FROM User WHERE email='{email}'")
        self.assertEqual(1,len(res1))
        self.assertEqual(nombre,res1[0][0])
        self.assertEqual(apellidos,res1[0][1])
        self.assertEqual(fecha_nac,res1[0][2])
        self.assertEqual(email,res1[0][3])

    def test_noCreaUsuario(self):
        nombre= "Usuario"
        apellidos= "Uno"
        fecha_nac='2002-02-02'
        email="user@gmail.com"
        password= "user"
        self.login("admin@gmail.com","admin")
        res = self.crearUsuario(nombre,apellidos,fecha_nac,email,password)
        self.assertEqual(302, res.status_code)
        text1 = "Usuario%20ya%20existe"
        self.assertEqual('/msg?mensaje='+text1, res.location)
        page = BeautifulSoup(res.data, features='html.parser')
        text = "Usuario ya existe"
        # Se tiene que mostrar el siguiente h1: Opciones de administrador
        #self.assertEqual(1, len(page.find_all(lambda tag: tag.name == "h2" and text in tag.text)))
    
    def test_borrarUsuarioCampos(self):
        self.login("admin@gmail.com","admin")
        res = self.client.get('/borrarUsuario')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertIsNotNone(page.find('form').find('input', id='email'))
        self.assertIsNotNone(page.find('form').find('button', type='submit'))

    def test_añadirLibroCampos(self):
        self.login("admin@gmail.com","admin")
        res = self.client.get('/añadirLibro')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertIsNotNone(page.find('form').find('input', id='titulo'))
        self.assertIsNotNone(page.find('form').find('input', id='autor'))
        self.assertIsNotNone(page.find('form').find('input', id='cover'))
        self.assertIsNotNone(page.find('form').find('input', id='descripcion'))
        self.assertIsNotNone(page.find('form').find('button', type='submit'))

    
    def test_BorrarLibroCampos(self):
        self.login("admin@gmail.com","admin")
        res = self.client.get('/borrarLibro')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertIsNotNone(page.find('form').find('input', id='titulo'))
        self.assertIsNotNone(page.find('form').find('input', id='autor'))
        self.assertIsNotNone(page.find('form').find('button', type='submit'))