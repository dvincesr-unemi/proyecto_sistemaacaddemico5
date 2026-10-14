from datetime import date
from typing import Dict, Any


# =====================================================================
# CLASE BASE: lo que los modelos comparten
# =====================================================================
class ModeloBase:
    """Padre de todos los modelos. Guarda el id y define el comportamiento comun."""

    def __init__(self, id_registro: int) -> None:
        """
        Inicializa la entidad base con su identificador unico.

        Args:
            id_registro (int): Identificador numerico unico para el registro.

        Returns:
            None
        """
        self.id = int(id_registro)

    # ---- UNICO METODO DE CLASE DEL PROYECTO ----
    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "ModeloBase":
        """
        Diccionario -> objeto. Escrito UNA vez y usado por todos los modelos.
        cls es la clase que llamo: Beca, Estudiante, Materia o Matricula.

        Args:
            datos (Dict[str, Any]): Diccionario con los datos leidos del JSON.

        Returns:
            ModeloBase: Instancia de la clase que hizo la llamada.
        """
        datos_copia = dict(datos)                  # copia, para no tocar el original
        id_registro = datos_copia.pop("id")        # saco el id
        return cls(id_registro, **datos_copia)     # el resto son los campos del modelo

    # ---- METODOS DE INSTANCIA ----
    def a_diccionario(self) -> Dict[str, Any]:
        """
        Objeto -> diccionario. Cada hijo agrega sus campos.

        Args:
            Ninguno

        Returns:
            Dict[str, Any]: Diccionario base conteniendo solo el id.
        """
        return {"id": self.id}

    def etiqueta(self) -> str:
        """
        POLIMORFISMO: cada hijo la reescribe a su manera para listados.

        Args:
            Ninguno

        Returns:
            str: Texto generico con el numero de registro.
        """
        return f"registro {self.id}"

    def __str__(self) -> str:
        """
        Lo que se ve al hacer print(objeto). Llama a etiqueta(),
        asi que cada modelo se imprime distinto sin cambiar esta linea.

        Args:
            Ninguno

        Returns:
            str: Representacion final formateada para la consola.
        """
        return f"[{self.id}] {self.etiqueta()}"


# =====================================================================
# BECA: Catalogo de beneficios o incentivos estudiantiles
# =====================================================================
class Beca(ModeloBase):
    """Beca o beneficio economico/academico asignable a un estudiante."""

    def __init__(
        self, id_registro: int, nombre: str, porcentaje: float = 100.0, 
        tipo: str = "Parcial", descripcion: str = ""
    ) -> None:
        """
        Inicializa una Beca o estimulo de estudios.

        Args:
            id_registro (int): Identificador numerico unico.
            nombre (str): Nombre de la beca (ej: 'Excelencia Academica', 'Deportiva').
            porcentaje (float, opcional): Cobertura porcentual (0 a 100). Por defecto 100.0.
            tipo (str, opcional): Categoria del beneficio (Total, Parcial, Socioeconomica). Por defecto 'Parcial'.
            descripcion (str, opcional): Detalle o requisitos del beneficio. Por defecto "".

        Returns:
            None
        """
        super().__init__(id_registro)
        self.nombre = nombre
        self.porcentaje = float(porcentaje)
        self.tipo = tipo
        self.descripcion = descripcion

    # Metodo estatico para validar que el porcentaje de beca sea coherente
    @staticmethod
    def es_porcentaje_valido(valor: Any) -> bool:
        """
        Valida que el valor represente un porcentaje admisible entre 1 y 100.

        Args:
            valor (Any): Valor a evaluar.

        Returns:
            bool: True si esta entre 1 y 100 inclusive.
        """
        try:
            num = float(valor)
            return 0 < num <= 100
        except (TypeError, ValueError):
            return False

    def a_diccionario(self) -> Dict[str, Any]:
        """
        Serializa los campos de Beca a un diccionario compatible con JSON.

        Args:
            Ninguno

        Returns:
            Dict[str, Any]: Diccionario con id, nombre, porcentaje, tipo y descripcion.
        """
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["porcentaje"] = self.porcentaje
        datos["tipo"] = self.tipo
        datos["descripcion"] = self.descripcion
        return datos

    def etiqueta(self) -> str:
        """
        Representacion concisa de la beca para menus y comprobantes.

        Args:
            Ninguno

        Returns:
            str: Nombre, porcentaje y tipo de beca.
        """
        return f"{self.nombre} ({self.porcentaje:.0f}% cobertura) · Tipo: {self.tipo}"


# =====================================================================
# HERENCIA: Persona es la base de Estudiante
# =====================================================================
class Persona(ModeloBase):
    """Todo lo que tiene una persona del sistema."""

    def __init__(self, id_registro: int, nombre: str, apellido: str, email: str) -> None:
        """
        Inicializa una Persona con sus datos civiles basicos.

        Args:
            id_registro (int): Identificador unico numerico.
            nombre (str): Nombre de la persona.
            apellido (str): Apellido de la persona.
            email (str): Correo electronico de contacto.

        Returns:
            None
        """
        super().__init__(id_registro)      # el padre guarda el id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def nombre_completo(self) -> str:
        """
        Concatena de forma limpia el nombre y el apellido.

        Args:
            Ninguno

        Returns:
            str: Nombre y apellido unidos por un espacio.
        """
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self) -> Dict[str, Any]:
        """
        Agrega los atributos de Persona al diccionario del padre.

        Args:
            Ninguno

        Returns:
            Dict[str, Any]: Diccionario con id, nombre, apellido y email.
        """
        datos = super().a_diccionario()    # {"id": ...} que arma el padre
        datos["nombre"] = self.nombre
        datos["apellido"] = self.apellido
        datos["email"] = self.email
        return datos

    def etiqueta(self) -> str:
        """
        Sobrescribe la representacion base para devolver el nombre completo.

        Args:
            Ninguno

        Returns:
            str: Nombre completo.
        """
        return self.nombre_completo()


class Estudiante(Persona):
    """Estudiante ES UNA Persona, con carnet, carrera y vinculo opcional a una Beca."""

    def __init__(
        self, id_registro: int, nombre: str, apellido: str, email: str, 
        carnet: str = "", carrera: str = "", beca_id: int = 0
    ) -> None:
        """
        Inicializa un Estudiante integrando sus datos academicos y beneficio de beca.

        Args:
            id_registro (int): Identificador unico numerico.
            nombre (str): Nombre del estudiante.
            apellido (str): Apellido del estudiante.
            email (str): Correo electronico de contacto.
            carnet (str, opcional): Codigo de identificacion. Por defecto "".
            carrera (str, opcional): Programa academico. Por defecto "".
            beca_id (int, opcional): ID de la Beca asignada. Por defecto 0 (sin beca).

        Returns:
            None
        """
        super().__init__(id_registro, nombre, apellido, email)
        self.carnet = carnet
        self.carrera = carrera
        self.beca_id = int(beca_id)

    def tiene_beca(self) -> bool:
        """Indica si el alumno cuenta con algun beneficio activo."""
        return self.beca_id > 0

    def a_diccionario(self) -> Dict[str, Any]:
        """
        Extiende el diccionario de Persona agregando carnet, carrera y beca_id.

        Args:
            Ninguno

        Returns:
            Dict[str, Any]: Diccionario completo del Estudiante.
        """
        datos = super().a_diccionario()    # reutiliza lo de Persona
        datos["carnet"] = self.carnet
        datos["carrera"] = self.carrera
        datos["beca_id"] = self.beca_id
        return datos

    def etiqueta(self) -> str:
        """
        Sobrescribe y EXTIENDE la etiqueta del padre (Persona).

        Args:
            Ninguno

        Returns:
            str: Representacion con nombre, carnet, carrera y estado de beca.
        """
        beca_info = f" · [Beca #{self.beca_id}]" if self.tiene_beca() else ""
        return f"{super().etiqueta()} · {self.carnet or 'sin carnet'} · {self.carrera}{beca_info}"


# =====================================================================
# UNICA CLASE CON ATRIBUTOS Y METODOS ESTATICOS
# =====================================================================
class Materia(ModeloBase):
    """Materia ES UN ModeloBase. Aqui viven los ejemplos de lo estatico para el sistema."""

    # ATRIBUTOS ESTATICOS (de clase): existen una sola vez, no por objeto
    CUPOS_MAXIMOS = 30           # regla del negocio, igual para todas las materias
    NOTA_APROBACION = 14         # calificacion minima para aprobar
    total_creadas = 0            # contador compartido

    def __init__(
        self, id_registro: int, nombre: str, codigo: str, 
        creditos: int = 0, cupos: int = 30
    ) -> None:
        """
        Inicializa una asignatura academica.

        Args:
            id_registro (int): Identificador unico numerico.
            nombre (str): Nombre de la asignatura.
            codigo (str): Codigo institucional de la asignatura.
            creditos (int, opcional): Valor en creditos academicos. Por defecto 0.
            cupos (int, opcional): Plazas disponibles. Por defecto 30.

        Returns:
            None
        """
        super().__init__(id_registro)
        self.nombre = nombre
        self.codigo = codigo
        self.creditos = int(creditos)
        self.cupos = int(cupos)
        Materia.total_creadas += 1         # se modifica en la CLASE, no en self

    # METODOS ESTATICOS: reglas que no necesitan ninguna materia concreta
    @staticmethod
    def es_nota_valida(valor: Any) -> bool:
        """
        Valida que un ingreso numerico este dentro del rango permitido (0 a 20).

        Args:
            valor (Any): Valor a evaluar, usualmente string o numerico.

        Returns:
            bool: True si es valido, False si hay error de tipo o rango.
        """
        try:
            nota = float(valor)
            return 0 <= nota <= 20
        except (TypeError, ValueError):
            return False

    # METODOS DE INSTANCIA: necesitan los datos de ESTA materia
    def hay_cupo(self) -> bool:
        """
        Verifica si la materia aun cuenta con plazas disponibles.

        Args:
            Ninguno

        Returns:
            bool: True si hay cupos restantes.
        """
        return self.cupos > 0

    def ocupar_cupo(self) -> None:
        """
        Resta 1 a la disponibilidad si es que todavia hay cupos.

        Args:
            Ninguno

        Returns:
            None
        """
        if self.hay_cupo():
            self.cupos -= 1

    def liberar_cupo(self) -> None:
        """
        Suma 1 a la disponibilidad, sin exceder el maximo configurado en la clase.

        Args:
            Ninguno

        Returns:
            None
        """
        if self.cupos < Materia.CUPOS_MAXIMOS:
            self.cupos += 1

    def a_diccionario(self) -> Dict[str, Any]:
        """
        Objeto -> diccionario agregando los datos de la asignatura.

        Args:
            Ninguno

        Returns:
            Dict[str, Any]: Datos para el JSON.
        """
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["codigo"] = self.codigo
        datos["creditos"] = self.creditos
        datos["cupos"] = self.cupos
        return datos

    def etiqueta(self) -> str:
        """
        Genera el formato de lectura para la asignatura y alerta si esta llena.

        Args:
            Ninguno

        Returns:
            str: Texto con codigo, nombre y cupos restantes.
        """
        alerta = " ⚠ LLENA" if not self.hay_cupo() else ""
        return f"[{self.codigo}] {self.nombre} ({self.creditos} Cr) · cupos {self.cupos}/{Materia.CUPOS_MAXIMOS}{alerta}"


# =====================================================================
# MATRICULA: Relacion transaccional 1 a 1 intacta
# =====================================================================
class Matricula(ModeloBase):
    """Matricula simple: une a un estudiante con una materia en un periodo especifico."""

    def __init__(
        self, id_registro: int, estudiante_id: int, materia_id: int, 
        periodo: str, nota: float = 0.0, fecha: str = ""
    ) -> None:
        """
        Inicializa la relacion transaccional entre estudiante y materia.

        Args:
            id_registro (int): Identificador de la matricula.
            estudiante_id (int): ID de la entidad Estudiante.
            materia_id (int): ID de la entidad Materia.
            periodo (str): Ciclo lectivo o semestre.
            nota (float, opcional): Calificacion. Por defecto 0.0.
            fecha (str, opcional): Fecha de registro. Por defecto se usa la de hoy.

        Returns:
            None
        """
        super().__init__(id_registro)
        self.estudiante_id = int(estudiante_id)
        self.materia_id = int(materia_id)
        self.periodo = periodo
        self.nota = float(nota)
        self.fecha = fecha or date.today().isoformat()

    def esta_aprobada(self) -> bool:
        """
        Consulta la regla estatica de Materia para saber si la nota es aprobatoria.
        Se calcula cada vez para no quedar desactualizado si la nota cambia.

        Args:
            Ninguno

        Returns:
            bool: True si es mayor o igual a la NOTA_APROBACION.
        """
        return self.nota >= Materia.NOTA_APROBACION

    def estado(self) -> str:
        """
        Convierte la validacion de aprobacion en un estado legible.

        Args:
            Ninguno

        Returns:
            str: 'Aprobada' o 'Reprobada'.
        """
        return "Aprobada" if self.esta_aprobada() else "Reprobada"

    def a_diccionario(self) -> Dict[str, Any]:
        """
        Devuelve el diccionario que se persistira en la transaccion.

        Args:
            Ninguno

        Returns:
            Dict[str, Any]: Diccionario con referencias y calificacion.
        """
        datos = super().a_diccionario()
        datos["estudiante_id"] = self.estudiante_id
        datos["materia_id"] = self.materia_id
        datos["periodo"] = self.periodo
        datos["nota"] = self.nota
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self) -> str:
        """
        Formato de lectura que resume la situacion academica de la inscripcion.

        Args:
            Ninguno

        Returns:
            str: Historial formateado.
        """
        return (f"{self.fecha} · estudiante {self.estudiante_id} · "
                f"materia {self.materia_id} ({self.periodo}) "
                f"-> Nota: {self.nota} [{self.estado()}]")