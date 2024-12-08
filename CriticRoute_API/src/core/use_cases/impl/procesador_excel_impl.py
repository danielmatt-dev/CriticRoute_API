from datetime import date
from io import BytesIO
from typing import List, Dict, Any, Optional

import pandas as pd

from CriticRoute_API.src.core.exceptions.invalid_excel_format_ex import InvalidExcelFormatEx
from CriticRoute_API.src.core.use_cases.procesador_excel import ProcesadorExcel


class ProcesadorExcelImpl(ProcesadorExcel):

    def __init__(self):
        super().__init__()
        self._file_bytes = None
        self.df = None
        self.ids_tareas = set()

    def get_file_bytes(self) -> Optional[bytes]:
        return self._file_bytes

    def set_file_bytes(self, file_bytes: bytes):
        self._file_bytes = file_bytes
        self.df = self.__limpiar_y_renombrar_columnas()

    def __limpiar_y_renombrar_columnas(self) -> pd.DataFrame:
        """
        Limpia y renombra las columnas del archivo Excel, basándose en las filas específicas
        para obtener los encabezados.

        Returns:
            pd.DataFrame: El DataFrame con las columnas renombradas y las filas relevantes extraídas.

        Raises:
            ValueError: Si no se encuentra una de las columnas esperadas.
        """
        excel_file = BytesIO(self._file_bytes)

        # Leer la fila 7 como referencia
        df_header_7 = pd.read_excel(excel_file, header=None, engine='openpyxl')

        columnas = list(df_header_7.iloc[7, :])  # Tomar las columnas de la fila 7 como lista

        try:
            # Encontrar los rangos de columnas
            inicio_responsables = columnas.index("Responsables")
            fin_responsables = columnas.index("Actividades predecesoras")
            inicio_predecesoras = fin_responsables
            fin_predecesoras = columnas.index("Duración")
        except ValueError as ex:
            raise ValueError(f"No se encontró una columna esperada: {ex}")

        # Leer el DataFrame desde la fila 8
        df_header_8 = pd.read_excel(excel_file, header=8, engine='openpyxl')

        # Renombrar columnas de Responsables
        for i, col in enumerate(df_header_8.columns[inicio_responsables:fin_responsables], start=1):
            df_header_8.rename(columns={col: f"Responsable {i}"}, inplace=True)

        # Renombrar columnas de Actividades predecesoras
        for i, col in enumerate(df_header_8.columns[inicio_predecesoras:fin_predecesoras], start=1):
            df_header_8.rename(columns={col: f"Predecesor {i}"}, inplace=True)

        return df_header_8

    def __validar_id_actividad(self, id_tarea: int):
        """
        Valida que el ID de la tarea sea único dentro del conjunto de tareas.

        Args:
            id_tarea (int): El ID de la tarea a validar.

        Raises:
            InvalidExcelFormatEx: Si el ID de la tarea ya ha sido utilizado.
        """
        if id_tarea and id_tarea in self.ids_tareas:
            raise InvalidExcelFormatEx(f'El ID {id_tarea} ya ha sido utilizado, los IDs deben ser únicos')

        if id_tarea:
            self.ids_tareas.add(id_tarea)

    def __validar_predecesoras(self, acts: List[Dict]):
        """
        Valida que las predecesoras de cada actividad existan en el conjunto de tareas.

        Args:
            acts (List[Dict]): La lista de actividades con sus respectivas predecesoras.

        Raises:
            InvalidExcelFormatEx: Si alguna predecesora no existe en el conjunto de tareas.
        """
        for act in acts:
            predecesoras = act['Predecesoras']
            for predecesora in predecesoras:
                if predecesora not in self.ids_tareas:
                    raise InvalidExcelFormatEx(f'La tarea ID {predecesora} no existe')

    def procesar_datos_actividades(self) -> List[Dict]:

        nombre = 'Nombre'
        descripcion = 'Descripción'

        actividades = []

        # Itera sobre cada fila del DataFrame y construye un diccionario con los datos de la actividad
        for _, row in self.df.iterrows():

            # Validar el ID de la tarea
            id_tarea = int(row["ID"]) if not pd.isna(row.get("ID", None)) else None
            self.__validar_id_actividad(id_tarea)

            # Obtener y validar el nombre de la actividad
            nombre_actividad = row[nombre].strip() if isinstance(row[nombre], str) and not pd.isna(row.get(nombre, "")) \
                else ""

            if not nombre_actividad:
                raise InvalidExcelFormatEx(f'El nombre de la tarea ID {id_tarea} no puede estar en blanco')

            actividad = {
                "ID": id_tarea,
                nombre: row[nombre].strip() if not pd.isna(row.get(nombre, "")) else "",
                descripcion: row[descripcion].strip() if not pd.isna(row.get(descripcion, "")) else "",
                "Responsables": self.__extraer_responsables(row),
                "Predecesoras": self.__extraer_predecesoras(row),
                "Tiempos": self.__extraer_tiempos(row, id_tarea),
            }
            actividades.append(actividad)

        # Validar que todas las predecesoras existen en el conjunto de tareas
        self.__validar_predecesoras(actividades)
        return actividades

    def __extraer_responsables(self, row: pd.Series) -> List[str]:

        """
        Extrae los responsables de una actividad de una fila del DataFrame.

        Args:
            row (pd.Series): Una fila del DataFrame que contiene los datos de la actividad.

        Returns:
            List[str]: Una lista de responsables asociados a la actividad.
        """

        responsables = []
        for col in [c for c in self.df.columns if "Responsable" in c]:
            if not pd.isna(row.get(col, "")):
                responsables.append(row[col].strip())
        return responsables

    def __extraer_predecesoras(self, row: pd.Series) -> List[int]:

        """
        Extrae las actividades predecesoras de una fila del DataFrame.

        Args:
            row (pd.Series): Una fila del DataFrame que contiene los datos de la actividad.

        Returns:
            List[int]: Una lista de IDs de las actividades predecesoras.
        """

        predecesoras = []
        for col in [c for c in self.df.columns if "Predecesor" in c]:
            try:
                if not pd.isna(row.get(col, "")):
                    predecesoras.append(int(row[col]))
            except ValueError:
                continue
        return predecesoras

    @staticmethod
    def __extraer_tiempos(row: pd.Series, id_tarea: int) -> Dict:

        """
        Extrae los tiempos (optimista, probable, pesimista) de una fila del DataFrame.

        Args:
            row (pd.Series): Una fila del DataFrame que contiene los datos de la actividad.

        Returns:
            Dict: Un diccionario con los tiempos extraídos (optimista, más probable y pesimista).
        """

        optimista = 'Optimista'
        probable = 'Más probable'
        pesimista = 'Pesimista'

        def safe_float(value, name):
            """
            Intenta convertir un valor a un número flotante. Si no es posible, lanza una excepción personalizada.
            """
            try:
                return float(value) if not pd.isna(value) else None
            except (ValueError, TypeError):
                raise ValueError(f'La tarea ID {id_tarea}, su tiempo {name} debe ser un número flotante válido.')

        return {
            optimista: safe_float(row.get(optimista, None), optimista),
            probable: safe_float(row.get(probable, None), probable),
            pesimista: safe_float(row.get(pesimista, None), pesimista),
        }

    def extraer_datos_proyecto(self) -> Dict[str, Any]:
        """Extrae los datos de configuración desde un archivo Excel."""

        # Convertir los bytes del archivo a un DataFrame
        excel_file = BytesIO(self._file_bytes)
        df = pd.read_excel(excel_file, header=None, engine='openpyxl')

        # Inicializar las variables para los datos
        datos = {
            'fecha_inicio': None,
            'unidad_tiempo': None,
            'horas_trabajo_dia': 0,
            'numero_decimales': 0
        }

        # Iterar sobre las filas para extraer los valores usando las funciones auxiliares
        for _, row in df.iterrows():
            # Buscar y extraer los valores
            datos['fecha_inicio'] = self.__extraer_valor(row, 'Fecha de inicio:', datos['fecha_inicio'])
            datos['unidad_tiempo'] = self.__extraer_valor(row, 'Unidad de tiempo:', datos['unidad_tiempo'])
            datos['horas_trabajo_dia'] = self.__extraer_valor_horas(row, 'Horas de trabajo al día:',
                                                                    datos['horas_trabajo_dia'])
            datos['numero_decimales'] = self.__extraer_valor_numero(row, 'Número de decimales:',
                                                                    datos['numero_decimales'])

        fecha_inicio = datos['fecha_inicio']

        # Convertir la fecha de inicio al formato deseado 'yyyy-MM-dd' (si es posible)
        if isinstance(fecha_inicio, str):
            try:
                fecha_inicio = pd.to_datetime(fecha_inicio, format='%d/%m/%Y', errors='coerce')
                fecha_inicio = fecha_inicio.strftime('%Y-%m-%d') if pd.notna(fecha_inicio) else None
            except ValueError:
                fecha_inicio = None

        datos['fecha_inicio'] = fecha_inicio

        if not isinstance(datos['fecha_inicio'], date):
            raise ValueError("La fecha de inicio debe ser de tipo 'date'.")
        if not isinstance(datos['unidad_tiempo'], str):
            raise ValueError("La unidad de tiempo debe ser una cadena de texto.")
        if not isinstance(datos['horas_trabajo_dia'], int):
            raise ValueError("Las horas de trabajo por día deben ser enteros.")
        if not isinstance(datos['numero_decimales'], int):
            raise ValueError("El número de decimales debe ser entero")

        return datos

    @staticmethod
    def __extraer_valor(row: pd.Series, texto: str, valor_actual: Any) -> Any:
        """
        Busca y extrae el valor correspondiente si el texto está en la celda, sino retorna el valor actual.

        Args:
            row (pd.Series): Fila del DataFrame.
            texto (str): Texto que debe ser buscado en la fila.
            valor_actual (Any): Valor a retornar si no se encuentra el texto.

        Returns:
            Any: El valor extraído o el valor actual si no se encuentra el texto.
        """
        if texto in str(row[2]):
            return row[3]  # Extrae el valor de la celda siguiente
        return valor_actual

    @staticmethod
    def __extraer_valor_horas(row: pd.Series, texto: str, valor_actual: int) -> int:

        """
        Extrae las horas de trabajo al día desde una fila si el texto está presente.

        Args:
            row (pd.Series): Fila del DataFrame.
            texto (str): Texto que debe ser buscado en la fila.
            valor_actual (int): Valor a retornar si no se encuentra el texto.

        Returns:
            int: El valor de horas extraído o el valor actual si no se encuentra.
        """

        if texto in str(row[2]) and row[3] and str(row[3]).isdigit():
            return int(row[3])
        return valor_actual

    @staticmethod
    def __extraer_valor_numero(row: pd.Series, texto: str, valor_actual: int) -> int:

        """
        Extrae el número de decimales desde una fila si el texto está presente.

        Args:
            row (pd.Series): Fila del DataFrame.
            texto (str): Texto que debe ser buscado en la fila.
            valor_actual (int): Valor a retornar si no se encuentra el texto.

        Returns:
            int: El número de decimales extraído o el valor actual si no se encuentra.
        """

        if texto in str(row[5]):
            try:
                return int(row[6]) if pd.notna(row[6]) and str(row[6]).isdigit() else 0
            except ValueError:
                return 0
        return valor_actual
