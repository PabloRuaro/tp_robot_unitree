# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  .....................................
#  Comision:           .....................................
# =====================================================================

from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO

# Tabla: cuantos datos lleva cada comando valido.
FORMATOS = {
    "avanzar": 3,
    "girar": 3,
    "detenerse": 1,
    "saludar": 1,
}


def _es_numero(valor):
    """True si 'valor' es un numero (int o float), False si no."""
    # bool es subclase de int: True vale 1 y False vale 0.
    # Si no lo sacamos, ("avanzar", True, 2.0) pasaria como valido.
    if isinstance(valor, bool):
        return False
    return isinstance(valor, (int, float))


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    """Decide si un comando se puede ejecutar. Devuelve True o False.

    Un comando es una tupla. El primer elemento dice que hacer:

        ("avanzar", velocidad, tiempo)    velocidad en m/s, tiempo en s
        ("girar", velocidad, tiempo)      velocidad en rad/s, tiempo en s
        ("detenerse",)
        ("saludar",)

    Cosas que conviene revisar:
      - que la tupla no este vacia
      - que el nombre del comando sea uno de los cuatro validos
      - que tenga la cantidad de datos que corresponde
        (avanzar y girar llevan dos; detenerse y saludar, ninguno)
      - que velocidad y tiempo sean numeros de verdad, no textos
      - que el tiempo no sea negativo
    """
    # TU CODIGO ACA
        # Chequeo 1: tiene que ser una tupla no vacia.
    if not isinstance(comando, tuple) or len(comando) == 0:
        return False

    # El primer elemento siempre es el nombre.
    nombre = comando[0]

    # Chequeo 2: el nombre tiene que ser uno de los 4 validos.
    if nombre not in FORMATOS:
        return False

    # Chequeo 3: la cantidad de elementos tiene que coincidir.
    if len(comando) != FORMATOS[nombre]:
        return False

    # Chequeos 4 y 5: solo aplican a avanzar y girar.
    if nombre in ("avanzar", "girar"):
        velocidad = comando[1]
        tiempo = comando[2]

        # Chequeo 4: los dos tienen que ser numeros de verdad.
        if not _es_numero(velocidad) or not _es_numero(tiempo):
            return False

        # Chequeo 5: el tiempo no puede ser negativo.
        if tiempo < 0:
            return False

    return True


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:

        robot.avanzar(velocidad=..., tiempo=...)
        robot.girar(velocidad=..., tiempo=...)
        robot.detenerse()
        robot.saludar()

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """
    # TU CODIGO ACA
    nombre = comando[0]

    try:
        if nombre == "avanzar":
            robot.avanzar(velocidad=comando[1], tiempo=comando[2])
        elif nombre == "girar":
            robot.girar(velocidad=comando[1], tiempo=comando[2])
        elif nombre == "detenerse":
            robot.detenerse()
        elif nombre == "saludar":
            robot.saludar()

        return f"OK: {nombre} ejecutado"

    except ErrorDeSeguridad as exc:
        return f"RECHAZADO por seguridad: {exc}"


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos, uno por uno.

    Por cada comando:
      - si NO es valido, lo rechaza y sigue con el siguiente
      - si es valido, lo ejecuta
      - en los dos casos, guarda en 'historial' que fue lo que paso

    Un comando invalido NO tiene que cortar la mision.
    """
    # TU CODIGO ACA
    for numero, comando in enumerate(mision, start=1):

        # Caso A: comando invalido. Lo anotamos y seguimos.
        if not comando_es_valido(comando):
            historial.append({
                "numero": numero,
                "comando": comando,
                "resultado": "invalido",
                "detalle": "el comando no tiene el formato correcto",
            })
            continue

        # Caso B: comando valido. Lo intentamos ejecutar.
        detalle = ejecutar_comando(robot, comando)

        if detalle.startswith("OK"):
            historial.append({
                "numero": numero,
                "comando": comando,
                "resultado": "ejecutado",
                "detalle": detalle,
            })
        else:
            historial.append({
                "numero": numero,
                "comando": comando,
                "resultado": "rechazado",
                "detalle": detalle,
            })


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision.

    Tiene que decir, como minimo:
      - cuantos comandos se ejecutaron bien
      - cuantos se rechazaron
      - cual fue el motivo de cada rechazo
    """
    # TU CODIGO ACA
    ejecutados = [e for e in historial if e["resultado"] == "ejecutado"]
    invalidos = [e for e in historial if e["resultado"] == "invalido"]
    rechazados = [e for e in historial if e["resultado"] == "rechazado"]

    print()
    print("=" * 62)
    print("  REPORTE DE LA MISION")
    print("=" * 62)
    print(f"  Total de comandos         : {len(historial)}")
    print(f"  Ejecutados correctamente  : {len(ejecutados)}")
    print(f"  Rechazados                : {len(invalidos) + len(rechazados)}")
    print(f"      - con formato invalido    : {len(invalidos)}")
    print(f"      - rechazados por seguridad: {len(rechazados)}")

    if invalidos or rechazados:
        print()
        print("  Motivo de cada rechazo:")
        print("  " + "-" * 58)
        for e in historial:
            if e["resultado"] == "ejecutado":
                continue
            print(f"  #{e['numero']:>2}  {e['comando']!r}")
            print(f"        {e['detalle']}")
    print("=" * 62)
    print()


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot()
    robot.conectar()

    historial = []

    try:
        # Empeza probando con MISION_BASICA.
        # Cuando funcione, proba con MISION_CON_ERRORES: esa tiene
        # comandos invalidos a proposito.
        ejecutar_mision(robot, MISION_BASICA, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
