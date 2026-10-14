from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
# 1. Importamos BecaController junto a los demas controladores
from views import EstudianteController, BecaController, MateriaController, MatriculaController

# Se crea UN solo controlador de cada tipo.
# Inyeccion de dependencias:
# - Becas se pasa a Estudiantes para asignar y validar beneficios.
# - Estudiantes y Materias se pasan a Matriculas (flujo 1 a 1 intacto).
becas = BecaController()                      # <--- NUEVO CONTROLADOR
estudiantes = EstudianteController(becas)     # <--- RECIBE A BECAS
materias = MateriaController()
matriculas = MatriculaController(estudiantes, materias)


# =====================================================================
# AYUDAS DE PANTALLA
# =====================================================================

def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta):
    """Devuelve un entero o None si el usuario escribio otra cosa."""
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def mostrar_resultado(exito, mensaje):
    # Los controladores devuelven la TUPLA (exito, mensaje)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_lista(objetos, vacio="No hay registros todavia."):
    """Sirve para becas, estudiantes, materias y matriculas: cada modelo sabe mostrarse."""
    if not objetos:
        imprimir_info(vacio)
        return
    for objeto in objetos:
        print(f"  {objeto}")
    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto):
    # Recorre el DICCIONARIO del objeto: clave y valor a la vez
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")


# =====================================================================
# MENU DE BECAS (NUEVO)
# =====================================================================

def crear_beca():
    imprimir_titulo("CREAR BECA / BENEFICIO")
    datos = {
        "nombre": input("Nombre (ej. Excelencia, Deportiva): "),
        "porcentaje": input("Porcentaje de cobertura (1-100) [Enter = 100]: "),
        "tipo": input("Tipo (Total, Parcial, Socioeconomica) [Enter = Parcial]: "),
        "descripcion": input("Descripcion o requisitos: "),
    }
    mostrar_resultado(*becas.crear(datos))
    pausa()


def listar_becas():
    imprimir_titulo("BECAS Y BENEFICIOS")
    mostrar_lista(becas.leer(), "Todavia no hay becas registradas.")
    pausa()


def buscar_beca():
    imprimir_titulo("BUSCAR BECA")
    termino = input("Nombre, tipo o descripcion: ")
    encontradas = becas.buscar(termino)
    mostrar_lista(encontradas, f"Ninguna beca coincide con '{termino}'.")
    pausa()


def ver_beca():
    imprimir_titulo("VER BECA POR ID")
    beca = becas.obtener(pedir_entero("Id: "))
    if beca is None:
        imprimir_error("No encontrada")
    else:
        mostrar_detalle(beca)
        beneficiarios = estudiantes.por_beca(beca.id)
        print(f"\n  Estudiantes con este beneficio ({len(beneficiarios)}):")
        for est in beneficiarios:
            print(f"    - [{est.carnet or 'Sin carnet'}] {est.nombre_completo()}")
    pausa()


def actualizar_beca():
    imprimir_titulo("ACTUALIZAR BECA")
    id_beca = pedir_entero("Id: ")
    beca = becas.obtener(id_beca)
    if beca is None:
        imprimir_error("No encontrada")
        return pausa()

    imprimir_info(f"Editando: {beca.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "porcentaje", "tipo", "descripcion"):
        actual = getattr(beca, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(*becas.actualizar(id_beca, cambios))
    pausa()


def eliminar_beca():
    imprimir_titulo("ELIMINAR BECA")
    id_beca = pedir_entero("Id: ")
    beca = becas.obtener(id_beca)
    if beca is None:
        imprimir_error("No encontrada")
        return pausa()

    beneficiarios = estudiantes.por_beca(id_beca)
    if beneficiarios:
        imprimir_info(f"Aviso: Hay {len(beneficiarios)} estudiante(s) con esta beca asignada.")

    imprimir_info(f"Se eliminara: {beca.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*becas.eliminar(id_beca))
    else:
        imprimir_info("Operacion cancelada")
    pausa()


# =====================================================================
# MENU DE ESTUDIANTES (ADAPTADO)
# =====================================================================

def crear_estudiante():
    imprimir_titulo("CREAR ESTUDIANTE")
    
    # Mostramos becas disponibles para que el usuario conozca los IDs
    imprimir_info("Becas disponibles:")
    mostrar_lista(becas.leer(), "No hay becas registradas (se creara sin beca).")

    datos = {
        "nombre": input("\nNombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "carnet": input("Carnet: "),
        "carrera": input("Carrera: "),
        "beca_id": pedir_entero("Id de la beca (0 o vacio si no tiene): ") or 0,
    }
    mostrar_resultado(*estudiantes.crear(datos))
    pausa()


def listar_estudiantes():
    imprimir_titulo("ESTUDIANTES")
    mostrar_lista(estudiantes.leer(), "Todavia no hay estudiantes registrados.")
    pausa()


def buscar_estudiante():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido, email, carnet o carrera: ")
    encontrados = estudiantes.buscar(termino)
    mostrar_lista(encontrados, f"Ningun estudiante coincide con '{termino}'.")
    pausa()


def ver_estudiante():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    estudiante = estudiantes.obtener(pedir_entero("Id: "))
    if estudiante is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(estudiante)
        beca_obj = becas.obtener(estudiante.beca_id) if estudiante.beca_id else None
        info_beca = f"{beca_obj.nombre} ({beca_obj.porcentaje}%)" if beca_obj else "Sin beneficio"
        print(f"  Beca Asignada : {info_beca}")
    pausa()


def actualizar_estudiante():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_estudiante = pedir_entero("Id: ")
    estudiante = estudiantes.obtener(id_estudiante)
    if estudiante is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {estudiante.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "apellido", "email", "carnet", "carrera"):
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    # Opcion para cambiar la beca asociada
    cambio_beca_id = input(f"Beca ID [{estudiante.beca_id}]: ").strip()
    if cambio_beca_id:
        try:
            cambios["beca_id"] = int(cambio_beca_id)
        except ValueError:
            imprimir_error("El ID de beca debe ser un numero")
            return pausa()

    mostrar_resultado(*estudiantes.actualizar(id_estudiante, cambios))
    pausa()


def eliminar_estudiante():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_estudiante = pedir_entero("Id: ")
    estudiante = estudiantes.obtener(id_estudiante)
    if estudiante is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminara: {estudiante.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*estudiantes.eliminar(id_estudiante))
    else:
        imprimir_info("Operacion cancelada")
    pausa()


# =====================================================================
# MENU DE MATERIAS (INTACTO)
# =====================================================================

def crear_materia():
    imprimir_titulo("CREAR MATERIA")
    datos = {
        "nombre": input("Nombre: "),
        "codigo": input("Codigo: "),
        "creditos": input("Creditos: "),
        "cupos": input("Cupos iniciales [Enter = 30]: "),
    }
    mostrar_resultado(*materias.crear(datos))
    pausa()


def listar_materias():
    imprimir_titulo("MATERIAS")
    mostrar_lista(materias.leer(), "Todavia no hay materias creadas.")
    pausa()


def buscar_materia():
    imprimir_titulo("BUSCAR MATERIA")
    termino = input("Nombre o codigo: ")
    mostrar_lista(materias.buscar(termino), "Sin coincidencias.")
    pausa()


def ver_materia():
    imprimir_titulo("VER MATERIA POR ID")
    materia = materias.obtener(pedir_entero("Id: "))
    if materia is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(materia)
    pausa()


def actualizar_materia():
    imprimir_titulo("ACTUALIZAR MATERIA")
    id_materia = pedir_entero("Id: ")
    materia = materias.obtener(id_materia)
    if materia is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {materia.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "codigo", "creditos", "cupos"):
        actual = getattr(materia, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(*materias.actualizar(id_materia, cambios))
    pausa()


def eliminar_materia():
    imprimir_titulo("ELIMINAR MATERIA")
    id_materia = pedir_entero("Id: ")
    materia = materias.obtener(id_materia)
    if materia is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminara: {materia.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*materias.eliminar(id_materia))
    else:
        imprimir_info("Operacion cancelada")
    pausa()


# =====================================================================
# MENU DE MATRICULAS (TRANSACCIONAL 1 A 1 INTACTO)
# =====================================================================

def registrar_matricula():
    imprimir_titulo("REGISTRAR MATRICULA")
    imprimir_info("Estudiantes:")
    mostrar_lista(estudiantes.leer())
    imprimir_info("Materias:")
    mostrar_lista(materias.leer())

    datos = {
        "estudiante_id": pedir_entero("\nId del estudiante: "),
        "materia_id": pedir_entero("Id de la materia: "),
        "periodo": input("Periodo (ej. 2026-1): "),
    }
    
    if None in (datos["estudiante_id"], datos["materia_id"]):
        imprimir_error("Los IDs deben ser numeros enteros")
        return pausa()

    mostrar_resultado(*matriculas.crear(datos))
    pausa()


def listar_matriculas():
    imprimir_titulo("MATRICULAS ACTIVAS")
    mostrar_lista(matriculas.leer(), "Todavia no hay inscripciones.")
    pausa()


def asentar_calificacion():
    imprimir_titulo("ASENTAR CALIFICACION")
    id_matricula = pedir_entero("Id de la matricula: ")
    if not id_matricula:
        return pausa()
        
    nota = input("Ingrese la nota (0 a 20): ")
    mostrar_resultado(*matriculas.actualizar(id_matricula, {"nota": nota}))
    pausa()


def ver_reporte():
    imprimir_titulo("REPORTE ACADEMICO")
    texto = matriculas.reporte_academico(pedir_entero("Id del estudiante: "))
    if texto is None:
        imprimir_error("El estudiante no existe.")
    else:
        print(texto)
    pausa()


def anular_matricula():
    imprimir_titulo("ANULAR MATRICULA")
    id_matricula = pedir_entero("Id de la matricula: ")
    if id_matricula and confirmar("Se liberara el cupo. ¿Confirma?"):
        mostrar_resultado(*matriculas.eliminar(id_matricula))
    else:
        imprimir_info("Operacion cancelada")
    pausa()


def resumen():
    imprimir_titulo("RESUMEN GENERAL")
    print(f"  Becas activas : {len(becas.leer())}")
    print(f"  Estudiantes   : {len(estudiantes.leer())}")
    print(f"  Carreras      : {', '.join(estudiantes.carreras_registradas()) or '-'}")
    print(f"  Materias      : {len(materias.leer())}")
    
    llenas = [m for m in materias.leer() if not m.hay_cupo()]
    print(f"  Sin cupos     : {', '.join(m.codigo for m in llenas) or 'ninguna'}")
    print(f"  Matriculas    : {len(matriculas.leer())}")
    pausa()


# =====================================================================
# MENUS: DICCIONARIOS tecla -> (texto, funcion)
# =====================================================================

MENU_BECAS = {
    "1": ("Crear beca", crear_beca),
    "2": ("Ver todas", listar_becas),
    "3": ("Buscar", buscar_beca),
    "4": ("Ver por id", ver_beca),
    "5": ("Actualizar", actualizar_beca),
    "6": ("Eliminar", eliminar_beca),
    "0": ("Volver", None),
}

MENU_ESTUDIANTES = {
    "1": ("Crear estudiante", crear_estudiante),
    "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante),
    "4": ("Ver por id", ver_estudiante),
    "5": ("Actualizar", actualizar_estudiante),
    "6": ("Eliminar", eliminar_estudiante),
    "0": ("Volver", None),
}

MENU_MATERIAS = {
    "1": ("Crear materia", crear_materia),
    "2": ("Ver todas", listar_materias),
    "3": ("Buscar", buscar_materia),
    "4": ("Ver por id", ver_materia),
    "5": ("Actualizar", actualizar_materia),
    "6": ("Eliminar", eliminar_materia),
    "0": ("Volver", None),
}

MENU_MATRICULAS = {
    "1": ("Inscribir estudiante", registrar_matricula),
    "2": ("Ver todas", listar_matriculas),
    "3": ("Asentar calificacion", asentar_calificacion),
    "4": ("Ver reporte academico", ver_reporte),
    "5": ("Anular matricula", anular_matricula),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo, opciones):
    """Un solo bucle para los submenus."""
    while True:
        imprimir_titulo(titulo)
        for tecla, (texto, _funcion) in opciones.items():
            print(f"  {tecla}. {texto}")
        print()

        tecla = input("Opcion: ").strip()
        if tecla not in opciones:
            imprimir_error("Opcion no valida")
            pausa()
            continue

        _texto, funcion = opciones[tecla]
        if funcion is None:
            break
        funcion()


def main():
    while True:
        imprimir_titulo("SISTEMA ACADEMICO")
        print("  1. Estudiantes")
        print("  2. Becas / Beneficios")  # <--- NUEVA OPCION EN EL MENU
        print("  3. Materias")
        print("  4. Matriculas")
        print("  5. Resumen")
        print("  0. Salir\n")

        tecla = input("Opcion: ").strip()
        if tecla == "1":
            ejecutar_menu("GESTION DE ESTUDIANTES", MENU_ESTUDIANTES)
        elif tecla == "2":
            ejecutar_menu("GESTION DE BECAS", MENU_BECAS)
        elif tecla == "3":
            ejecutar_menu("GESTION DE MATERIAS", MENU_MATERIAS)
        elif tecla == "4":
            ejecutar_menu("GESTION DE MATRICULAS", MENU_MATRICULAS)
        elif tecla == "5":
            resumen()
        elif tecla == "0":
            imprimir_info("¡Hasta luego! 👋")
            break
        else:
            imprimir_error("Opcion no valida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")