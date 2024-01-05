from . import BaseTestClass
from bs4 import BeautifulSoup

class TestRS(BaseTestClass):
    def test_not_logged(self):
        """Test para comprobar que no se muestra el h1 Recomendaciones si no se esta logeado"""
        # Accede al catalogo
        res = self.client.get('/catalogue')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")

        # No se deberia mostrar el h1 Recomendaciones
        self.assertEqual(0, len(page.find_all('h1', class_='display-4')))

    def test_logged_no_borrows_no_friends(self):
        """Test para comprobar que se muestra el h1 Recomendaciones si se esta logeado pero no se tiene recomendaciones porque no tiene prestamo ni amigos"""
        # Inicia sesion
        # El usuario 4 no tiene prestamos ni amigos
        res = self.login('user4@gmail.com', 'user4')
        self.assertEqual(302, res.status_code)
        self.assertEqual('/', res.location)

        # Accede al catalogo
        res2 = self.client.get('/catalogue')
        self.assertEqual(200, res2.status_code)
        page = BeautifulSoup(res2.data, features="html.parser")

        # Se deberia mostrar el h1 Recomendaciones
        self.assertEqual(1, len(page.find_all('h1', class_='display-4')), format(page.prettify()))

        # No se deberian mostrar recomendaciones
        recomendaciones_div = page.find('div', id='Recomendaciones')
        self.assertEqual(0, len(recomendaciones_div.find_all('div', class_='card')), format(page.prettify()))

    def test_logged_borrows_no_friends(self):
        """Test para comprobar que se muestra el h1 Recomendaciones si se esta logeado y se tiene prestamos pero no amigos"""
        # Inicia sesion
        # El usuario 3 tiene prestamos pero no amigos
        res = self.login('user3@gmail.com', 'user3')
        self.assertEqual(302, res.status_code)
        self.assertEqual('/', res.location)

        # Accede al catalogo
        res2 = self.client.get('/catalogue')
        self.assertEqual(200, res2.status_code)
        page = BeautifulSoup(res2.data, features="html.parser")

        # Se deberia mostrar el h1 Recomendaciones
        self.assertEqual(1, len(page.find_all('h1', class_='display-4')), format(page.prettify()))

        # Se deberia mostrar una recomendacion en base a su prestamo
        # Como su prestamo es el libro3 que comparte tema con el libro4 saldra el libro4
        recomendaciones_div = page.find('div', id='Recomendaciones')
        self.assertEqual(1, len(recomendaciones_div.find_all('div', class_='card')), format(page.prettify()))
        self.assertEqual('Libro 04', recomendaciones_div.find('div', class_='card').find('h5').get_text())

    def test_logged_no_borrows_friends(self):
        """Test para comprobar que se muestra el h1 Recomendaciones si se esta logeado y se tiene amigos pero no prestamos"""
        # Inicia sesion
        # El usuario 2 tiene amigos pero no prestamos
        res = self.login('user2@gmail.com', 'user2')
        self.assertEqual(302, res.status_code)
        self.assertEqual('/', res.location)

        # Accede al catalogo
        res2 = self.client.get('/catalogue')
        self.assertEqual(200, res2.status_code)
        page = BeautifulSoup(res2.data, features="html.parser")

        # Se deberia mostrar el h1 Recomendaciones
        self.assertEqual(1, len(page.find_all('h1', class_='display-4')), format(page.prettify()))

        # Se deberia mostrar una recomendacion en base a sus amigos
        # Como su amigo es el usuario3 y este tiene prestamos, se motrara los libros del mismo tema que los prestamos de su amigo.
        # En este caso, el libro3 y el libro4
        recomendaciones_div = page.find('div', id='Recomendaciones')
        self.assertEqual(2, len(recomendaciones_div.find_all('div', class_='card')), format(page.prettify()))
        self.assertEqual('Libro 03', recomendaciones_div.find_all('div', class_='card')[0].find('h5').get_text())
        self.assertEqual('Libro 04', recomendaciones_div.find_all('div', class_='card')[1].find('h5').get_text())

    def test_logged_borrows_friends(self):
        """Test para comprobar que se muestra el h1 Recomendaciones si se esta logeado y se tiene amigos y prestamos"""
        # Inicia sesion
        # El usuario 1 tiene amigos y prestamos
        res = self.login('user1@gmail.com', 'user1')
        self.assertEqual(302, res.status_code)
        self.assertEqual('/', res.location)

        # Accede al catalogo
        res2 = self.client.get('/catalogue')
        self.assertEqual(200, res2.status_code)
        page = BeautifulSoup(res2.data, features="html.parser")

        # Se deberia mostrar el h1 Recomendaciones
        self.assertEqual(1, len(page.find_all('h1', class_='display-4')), format(page.prettify()))

        # Se deberia mostrar 3 recomendaciones
        # La primera en base al prestamo del usuario1 (nosotros) del libro1, que como comparte tema con el libro2, saldra el libro2 pero no el libro1 porque ya ha sido leido.
        # La segunda en base al prestamo del usuario3 que es su amigo, este tiene como prestamo el libro3 que tambien comparte tema con el libro4 por tanto, el libro3 y el libro4 saldran como recomendaciones.
        recomendaciones_div = page.find('div', id='Recomendaciones')
        self.assertEqual(3, len(recomendaciones_div.find_all('div', class_='card')), format(page.prettify()))
        self.assertEqual('Libro 02', recomendaciones_div.find_all('div', class_='card')[0].find('h5').get_text())
        self.assertEqual('Libro 03', recomendaciones_div.find_all('div', class_='card')[1].find('h5').get_text())
        self.assertEqual('Libro 04', recomendaciones_div.find_all('div', class_='card')[2].find('h5').get_text())
