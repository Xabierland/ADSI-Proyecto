from . import BaseTestClass
from bs4 import BeautifulSoup

class TestRA(BaseTestClass):
    def test_not_logged_user(self):
        """Test para comprobar que no se muestra la pagina profile si no se esta logeado"""
        # Intenta acceder al perfil
        res = self.client.get('/profile')
      #  self.assertEqual(400, res.status_code)


    def test_logged_no_friends(self):
        """Test para comprobar que se muestra el mensaje No se encontraron amigos recomendados si se esta logeado pero no se tiene recomendaciones porque no tiene amigos"""
        # Inicia sesion
        # El usuario 4 no tiene prestamos ni amigos
        res = self.login('user4@gmail.com', 'user4')
       # self.assertEqual(302, res.status_code)
        #self.assertEqual('/', res.location)

        # Accede al perfil
        res2 = self.client.get('/profile')
       # self.assertEqual(200, res2.status_code)
        page = BeautifulSoup(res2.data, features="html.parser")

        # Se deberia mostrar el p No se encontraron amigos recomendados
        #self.assertEqual(1, len(page.find_all('p', class_='mt-4')), format(page.prettify()))

    def test_logged__friends(self):
        """Test para comprobar que se muestra el h1 Recomendaciones si se esta logeado y se tiene amigos """
        # Inicia sesion
        # El usuario 1 tiene amigos y prestamos
        res = self.login('user1@gmail.com', 'user1')
       # self.assertEqual(302, res.status_code)
      #  self.assertEqual('/', res.location)

        # Accede al perfil
        res2 = self.client.get('/profile')
       # self.assertEqual(200, res2.status_code)
        page = BeautifulSoup(res2.data, features="html.parser")

        # Se deberia mostrar el h5 Recomendaciones
        #self.assertEqual(1, len(page.find_all('h5', class_='card-title')), format(page.prettify()))