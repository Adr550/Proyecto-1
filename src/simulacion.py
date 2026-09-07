from afn import EPSILON


def normalizar_cadena(cadena):
    """Interpreta '#' como la cadena vacía en las simulaciones."""
    return '' if cadena.strip() == '#' else cadena


def cerradura_epsilon(estados, afn):
    """
    Encuentra todos los estados alcanzables utilizando solamente
    transiciones epsilon.
    """
    cierre = set(estados)
    pila = list(estados)

    while pila:
        estado = pila.pop()

        transiciones = afn['transiciones'].get(estado, [])

        for simbolo, destino in transiciones:
            if simbolo == EPSILON and destino not in cierre:
                cierre.add(destino)
                pila.append(destino)

    return cierre


def mover(estados, simbolo, afn):
    """
    Encuentra los estados alcanzables desde un conjunto de estados
    consumiendo un símbolo.
    """
    destinos = set()

    for estado in estados:
        transiciones = afn['transiciones'].get(estado, [])

        for etiqueta, destino in transiciones:
            if etiqueta == simbolo:
                destinos.add(destino)

    return destinos


def simular_afn(afn, cadena):
    """
    Determina si una cadena es aceptada por el AFN.
    """
    cadena = normalizar_cadena(cadena)

    estados_actuales = cerradura_epsilon(
        {afn['inicial']},
        afn
    )

    for simbolo in cadena:
        alcanzados = mover(
            estados_actuales,
            simbolo,
            afn
        )

        estados_actuales = cerradura_epsilon(
            alcanzados,
            afn
        )

    return afn['final'] in estados_actuales


def simular_afd(afd, cadena):
    """
    Determina si una cadena es aceptada por el AFD.
    """
    cadena = normalizar_cadena(cadena)
    estado_actual = afd['inicial']

    for simbolo in cadena:

        # Si aparece un símbolo que no pertenece al alfabeto,
        # la cadena se rechaza automáticamente.
        if simbolo not in afd['alfabeto']:
            return False

        estado_actual = afd['transiciones'][estado_actual][simbolo]

    return estado_actual in afd['finales']
