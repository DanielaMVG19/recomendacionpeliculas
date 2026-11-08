import unittest
from app import app, grupo_edad, recomendar, GENEROS, CATALOGO


class RecomendadorTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_limites(self):
        for edad, esperado in [(2, '2 a 12'), (12, '2 a 12'), (13, '13 a 17'), (17, '13 a 17'), (18, '18 o más'), (80, '18 o más')]:
            self.assertEqual(grupo_edad(edad), esperado)
        with self.assertRaises(ValueError):
            grupo_edad(1)

    def test_filtros(self):
        for edad in (2, 12, 13, 17, 18, 90):
            for genero in GENEROS:
                resultados = recomendar(edad, genero)
                self.assertTrue(all(p['grupo'] == grupo_edad(edad) and p['genero'] == genero for p in resultados))
                if edad >= 13 or genero != 'Crimen':
                    self.assertTrue(resultados)

    def test_pagina_y_estilos(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        with self.client.get('/style.css') as respuesta:
            self.assertEqual(respuesta.status_code, 200)

    def test_entradas_invalidas(self):
        for edad, genero in [('', 'Drama'), ('hola', 'Drama'), ('3.5', 'Drama'), ('-1', 'Drama'), ('1', 'Drama'), ('20', 'Otro')]:
            respuesta = self.client.post('/', data={'edad': edad, 'genero': genero})
            self.assertEqual(respuesta.status_code, 200)
            self.assertIn('role="alert"', respuesta.get_data(as_text=True))

    def test_recomendacion_y_sin_resultados(self):
        texto = self.client.post('/', data={'edad': '20', 'genero': 'Crimen'}).get_data(as_text=True)
        self.assertIn('El padrino', texto)
        texto = self.client.post('/', data={'edad': '8', 'genero': 'Crimen'}).get_data(as_text=True)
        self.assertIn('No hay películas', texto)
        self.assertNotIn('El padrino', texto)

    def test_catalogo_valido(self):
        for pelicula in CATALOGO:
            self.assertIn(pelicula['genero'], GENEROS)
            self.assertIn(pelicula['grupo'], ('2 a 12', '13 a 17', '18 o más'))
            self.assertTrue(pelicula['titulo'] and pelicula['descripcion'])


if __name__ == '__main__':
    unittest.main()
