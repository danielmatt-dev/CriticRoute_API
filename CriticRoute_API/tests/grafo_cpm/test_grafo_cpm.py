import unittest
from datetime import date

from CriticRoute_API.src.core.entities.enums import UnidadTiempo
from CriticRoute_API.src.core.entities.proyecto import Proyecto
from CriticRoute_API.src.core.entities.tarea import Tarea
from CriticRoute_API.src.core.entities.usuario import Usuario
from CriticRoute_API.src.core.use_cases.impl.grafo_cpm_impl import GrafoCPMImpl


class TestGrafoCPM(unittest.TestCase):

    def setUp(self):
        self.proyecto = Proyecto(
            id_proyecto=1,
            usuario=Usuario(email='', password='', username='', id_usuario=None),
            titulo='Proyecto de prueba',
            descripcion='',
            fecha_inicio=date(2024, 11, 21),
            unidad_tiempo=UnidadTiempo.DIAS,
            horas_trabajo_dia=8,
            estado='Habilitado',
            num_decimales=3
        )

        self.tarea1 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=1,
            accion="1.1",
            tiempo_optimista=5,
            tiempo_probable=7,
            tiempo_pesimista=10,
            descripcion='',
            responsables=[]
        )

        self.tarea2 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=2,
            accion="1.2",
            tiempo_optimista=4,
            tiempo_probable=6,
            tiempo_pesimista=8,
            descripcion='',
            responsables=[]
        )

        self.tarea3 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=3,
            accion="1.3",
            tiempo_optimista=5,
            tiempo_probable=7,
            tiempo_pesimista=10,
            descripcion="Fase de pruebas",
            responsables=[]
        )

        self.tarea4 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=4,
            accion="2.1",
            tiempo_optimista=5,
            tiempo_probable=7,
            tiempo_pesimista=10,
            descripcion="Primera fase del proyecto",
            responsables=[]
        )

        self.tarea5 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=5,
            accion="2.2",
            tiempo_optimista=5,
            tiempo_probable=7,
            tiempo_pesimista=10,
            descripcion="Primera fase del proyecto",
            responsables=[]
        )

        self.tarea6 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=6,
            accion="2.3",
            tiempo_optimista=5,
            tiempo_probable=7,
            tiempo_pesimista=10,
            descripcion="Primera fase del proyecto",
            responsables=[]
        )

        self.tarea7 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=7,
            accion="3.1",
            tiempo_optimista=6,
            tiempo_probable=9,
            tiempo_pesimista=12,
            descripcion='',
            responsables=[]
        )

        self.tarea8 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=8,
            accion="3.2",
            tiempo_optimista=6,
            tiempo_probable=9,
            tiempo_pesimista=12,
            descripcion='',
            responsables=[]
        )

        self.tarea9 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=9,
            accion="3.3",
            tiempo_optimista=5,
            tiempo_probable=7,
            tiempo_pesimista=10,
            descripcion='',
            responsables=[]
        )

        self.tarea10 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=10,
            accion="3.4",
            tiempo_optimista=6,
            tiempo_probable=9,
            tiempo_pesimista=12,
            descripcion='',
            responsables=[]
        )

        self.tarea11 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=11,
            accion="4.1",
            tiempo_optimista=5,
            tiempo_probable=7,
            tiempo_pesimista=10,
            descripcion='',
            responsables=[]
        )

        self.tarea12 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=12,
            accion="4.2",
            tiempo_optimista=28,
            tiempo_probable=31,
            tiempo_pesimista=34,
            descripcion='',
            responsables=[]
        )

        self.tarea13 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=13,
            accion="4.3",
            tiempo_optimista=26,
            tiempo_probable=30,
            tiempo_pesimista=34,
            descripcion='',
            responsables=[]
        )

        self.tarea14 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=14,
            accion="4.4",
            tiempo_optimista=5,
            tiempo_probable=7,
            tiempo_pesimista=10,
            descripcion='',
            responsables=[]
        )

        self.tarea15 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=15,
            accion="5.1",
            tiempo_optimista=6,
            tiempo_probable=9,
            tiempo_pesimista=12,
            descripcion='',
            responsables=[]
        )

        self.tarea16 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=16,
            accion="5.2",
            tiempo_optimista=6,
            tiempo_probable=9,
            tiempo_pesimista=12,
            descripcion='',
            responsables=[]
        )

        self.tarea17 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=17,
            accion="5.3",
            tiempo_optimista=5,
            tiempo_probable=7,
            tiempo_pesimista=10,
            descripcion='',
            responsables=[]
        )

        self.tarea21 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=21,
            accion="7.1",
            tiempo_optimista=1,
            tiempo_probable=2,
            tiempo_pesimista=3,
            descripcion='',
            responsables=[]
        )

        self.tarea22 = Tarea.from_basic(
            proyecto=self.proyecto,
            numero_tarea=22,
            accion="7.2",
            tiempo_optimista=1,
            tiempo_probable=2,
            tiempo_pesimista=3,
            descripcion='',
            responsables=[]
        )

        self.grafo = GrafoCPMImpl()
        self.grafo.set_proyecto(proyecto=self.proyecto)

        self.grafo.agregar_tarea(self.tarea1)
        self.grafo.agregar_tarea(self.tarea2)
        self.grafo.agregar_tarea(self.tarea3)
        self.grafo.agregar_tarea(self.tarea4)
        self.grafo.agregar_tarea(self.tarea5)
        self.grafo.agregar_tarea(self.tarea6)
        self.grafo.agregar_tarea(self.tarea7)
        self.grafo.agregar_tarea(self.tarea8)
        self.grafo.agregar_tarea(self.tarea9)
        self.grafo.agregar_tarea(self.tarea10)
        self.grafo.agregar_tarea(self.tarea11)
        self.grafo.agregar_tarea(self.tarea12)
        self.grafo.agregar_tarea(self.tarea13)
        self.grafo.agregar_tarea(self.tarea14)
        self.grafo.agregar_tarea(self.tarea15)
        self.grafo.agregar_tarea(self.tarea16)
        self.grafo.agregar_tarea(self.tarea17)
        self.grafo.agregar_tarea(self.tarea21)
        self.grafo.agregar_tarea(self.tarea22)

        self.grafo.conectar_tareas(1, 2)
        self.grafo.conectar_tareas(2, 3)

        self.grafo.conectar_tareas(4, 5)
        self.grafo.conectar_tareas(5, 6)

        self.grafo.conectar_tareas(3, 7)
        self.grafo.conectar_tareas(6, 7)

        self.grafo.conectar_tareas(7, 8)

        self.grafo.conectar_tareas(8, 9)
        self.grafo.conectar_tareas(8, 10)

        self.grafo.conectar_tareas(9, 11)
        self.grafo.conectar_tareas(10, 11)

        self.grafo.conectar_tareas(11, 12)
        self.grafo.conectar_tareas(11, 13)
        self.grafo.conectar_tareas(11, 14)

        self.grafo.conectar_tareas(12, 15)
        self.grafo.conectar_tareas(12, 16)

        self.grafo.conectar_tareas(13, 17)
        self.grafo.conectar_tareas(14, 15)

        self.grafo.conectar_tareas(15, 21)
        self.grafo.conectar_tareas(16, 21)
        self.grafo.conectar_tareas(17, 21)

        self.grafo.conectar_tareas(21, 22)

    def test_agregar_tarea_duplicada(self):
        # Intentar agregar una tarea con el mismo número de tareas
        with self.assertRaises(ValueError):
            self.grafo.agregar_tarea(self.tarea1)

    def test_encontrar_ruta_critica(self):
        # Ejecutar el cálculo del CPM
        self.grafo.calcular_cpm()

        # Encontrar la ruta crítica
        ruta_critica = self.grafo.buscar_ruta_critica()

        # Verificar que las tareas de la ruta crítica sean las correctas
        ruta_esperada = [self.tarea4,
                         self.tarea5,
                         self.tarea6,
                         self.tarea7,
                         self.tarea8,
                         self.tarea10,
                         self.tarea11,
                         self.tarea12,
                         self.tarea15,
                         self.tarea16,
                         self.tarea21,
                         self.tarea22
                         ]
        self.assertListEqual(ruta_critica, ruta_esperada)

    def test_conectar_tareas_inexistentes(self):
        # Intentar conectar tareas inexistentes
        with self.assertRaises(ValueError):
            self.grafo.conectar_tareas(1, 99)  # Tarea 99 no existe

    def test_tiempos_tempranos(self):
        self.grafo.calcular_cpm()

        self.assertEqual(self.tarea1.inicio_temprano, 0)
        self.assertEqual(self.tarea1.final_temprano, 7.167)

        self.assertEqual(self.tarea2.inicio_temprano, 7.167)
        self.assertEqual(self.tarea2.final_temprano, 13.167)

        self.assertEqual(self.tarea3.inicio_temprano, 13.167)
        self.assertEqual(self.tarea3.final_temprano, 20.334)

        self.assertEqual(self.tarea4.inicio_temprano, 0)
        self.assertEqual(self.tarea4.final_temprano, 7.167)

        self.assertEqual(self.tarea6.inicio_temprano, 14.334)
        self.assertEqual(self.tarea6.final_temprano, 21.501)

        self.assertEqual(self.tarea8.inicio_temprano, 30.501)
        self.assertEqual(self.tarea8.final_temprano, 39.501)

        self.assertEqual(self.tarea10.inicio_temprano, 39.501)
        self.assertEqual(self.tarea10.final_temprano, 48.501)

        self.assertEqual(self.tarea13.inicio_temprano, 55.668)
        self.assertEqual(self.tarea13.final_temprano, 85.668)

        self.assertEqual(self.tarea15.inicio_temprano, 86.668)
        self.assertEqual(self.tarea15.final_temprano, 95.668)

        self.assertEqual(self.tarea17.inicio_temprano, 85.668)
        self.assertEqual(self.tarea17.final_temprano, 92.835)

        self.assertEqual(self.tarea21.inicio_temprano, 95.668)
        self.assertEqual(self.tarea21.final_temprano, 97.668)

        self.assertEqual(self.tarea12.inicio_temprano, 55.668)
        self.assertEqual(self.tarea12.final_temprano, 86.668)

        self.assertEqual(self.tarea14.inicio_temprano, 55.668)
        self.assertEqual(self.tarea14.final_temprano, 62.835)

        self.assertEqual(self.tarea5.inicio_temprano, 7.167)
        self.assertEqual(self.tarea5.final_temprano, 14.334)

        self.assertEqual(self.tarea22.inicio_temprano, 97.668)
        self.assertEqual(self.tarea22.final_temprano, 99.668)

    def test_tiempos_tardios(self):
        self.grafo.calcular_cpm()

        self.assertEqual(self.tarea1.inicio_tardio, 1.167)
        self.assertEqual(self.tarea1.holgura, 1.167)
        self.assertEqual(self.tarea1.final_tardio, 8.334)

        self.assertEqual(self.tarea3.inicio_tardio, 14.334)
        self.assertEqual(self.tarea3.holgura, 1.167)
        self.assertEqual(self.tarea3.final_tardio, 21.501)

        self.assertEqual(self.tarea4.inicio_tardio, 0.0)
        self.assertEqual(self.tarea4.holgura, 0.0)
        self.assertEqual(self.tarea4.final_tardio, 7.167)

        self.assertEqual(self.tarea7.inicio_tardio, 21.501)
        self.assertEqual(self.tarea7.holgura, 0.0)
        self.assertEqual(self.tarea7.final_tardio, 30.501)

        self.assertEqual(self.tarea9.inicio_tardio, 41.334)
        self.assertEqual(self.tarea9.holgura, 1.833)
        self.assertEqual(self.tarea9.final_tardio, 48.501)

        self.assertEqual(self.tarea11.inicio_tardio, 48.501)
        self.assertEqual(self.tarea11.holgura, 0.0)
        self.assertEqual(self.tarea11.final_tardio, 55.668)

        self.assertEqual(self.tarea13.inicio_tardio, 58.501)
        self.assertEqual(self.tarea13.holgura, 2.833)
        self.assertEqual(self.tarea13.final_tardio, 88.501)

        self.assertEqual(self.tarea16.inicio_tardio, 86.668)
        self.assertEqual(self.tarea16.holgura, 0.0)
        self.assertEqual(self.tarea16.final_tardio, 95.668)

        self.assertEqual(self.tarea22.inicio_tardio, 97.668)
        self.assertEqual(self.tarea22.holgura, 0)
        self.assertEqual(self.tarea22.final_tardio, 99.668)

        self.assertEqual(self.tarea21.inicio_tardio, 95.668)
        self.assertEqual(self.tarea21.holgura, 0)
        self.assertEqual(self.tarea21.final_tardio, 97.668)

        self.assertEqual(self.tarea2.inicio_tardio, 8.334)
        self.assertEqual(self.tarea2.holgura, 1.167)
        self.assertEqual(self.tarea2.final_tardio, 14.334)

        self.assertEqual(self.tarea5.inicio_tardio, 7.167)
        self.assertEqual(self.tarea5.holgura, 0.0)
        self.assertEqual(self.tarea5.final_tardio, 14.334)

        self.assertEqual(self.tarea15.inicio_tardio, 86.668)
        self.assertEqual(self.tarea15.holgura, 0.0)
        self.assertEqual(self.tarea15.final_tardio, 95.668)

        self.assertEqual(self.tarea10.inicio_tardio, 39.501)
        self.assertEqual(self.tarea10.holgura, 0.0)
        self.assertEqual(self.tarea10.final_tardio, 48.501)

        self.assertEqual(self.tarea14.inicio_tardio, 79.501)
        self.assertEqual(self.tarea14.holgura, 23.833)
        self.assertEqual(self.tarea14.final_tardio, 86.668)

        self.assertEqual(self.tarea8.inicio_tardio, 30.501)
        self.assertEqual(self.tarea8.holgura, 0.0)
        self.assertEqual(self.tarea8.final_tardio, 39.501)
