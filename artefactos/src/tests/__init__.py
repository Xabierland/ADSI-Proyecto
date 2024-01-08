import unittest
from controller import webServer
from model import Connection

class BaseTestClass(unittest.TestCase):
	def setUp(self):
		self.app = webServer.app
		self.client = self.app.test_client()
		self.db = Connection()
		
	def tearDown(self):
		pass

	def login(self, email, password):
		return self.client.post('/login', data=dict(
			email=email,
			password=password
		))
	
	def crearUsuario(self, nombre, apellidos, fecha_nac, email, password):
		return self.client.post('/crearUsuario', data=dict(
			nombre=nombre,
			apellidos=apellidos,
			fecha_nac=fecha_nac,
			email = email,
			password=password
		))
	
	def borrarUsuario(self, email):
		return self.client.post('/borrarUsuario', data=dict(
			email=email
		))
	
	def añadirLibro(self, titulo, autor, cover, descripcion):
		return self.client.post('/añadirLibro', data=dict(
			titulo=titulo,
			autor=autor,
			cover=cover,
			descripcion=descripcion
		))
	
	def borrarLibro(self, titulo, autor):
		return self.client.post('/borrarLibro', data=dict(
			titulo=titulo,
			autor=autor
		))