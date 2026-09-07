from collections import deque

from afn import EPSILON
from simulacion import cerradura_epsilon, mover


def obtener_alfabeto(afn):
    """
    Obtiene los símbolos utilizados por el AFN, sin incluir epsilon.
    """
    alfabeto = set()

    for transiciones_estado in afn['transiciones'].values():
        for simbolo, destino in transiciones_estado:
            if simbolo != EPSILON:
                alfabeto.add(simbolo)

    return sorted(alfabeto)


def subconjuntos(afn):
    """
    Convierte un AFN en un AFD utilizando el algoritmo
    de construcción por subconjuntos.
    """
    alfabeto = obtener_alfabeto(afn)

    conjunto_inicial = frozenset(
        cerradura_epsilon(
            {afn['inicial']},
            afn
        )
    )

    # Relaciona cada conjunto del AFN con un número de estado del AFD.
    identificadores = {
        conjunto_inicial: 0
    }

    pendientes = deque([conjunto_inicial])

    transiciones_afd = {}
    estados_finales = set()

    while pendientes:
        conjunto_actual = pendientes.popleft()
        estado_actual = identificadores[conjunto_actual]

        transiciones_afd[estado_actual] = {}

        # Un estado del AFD es final si contiene al estado final del AFN.
        if afn['final'] in conjunto_actual:
            estados_finales.add(estado_actual)

        for simbolo in alfabeto:
            destinos = mover(
                conjunto_actual,
                simbolo,
                afn
            )

            cierre = frozenset(
                cerradura_epsilon(
                    destinos,
                    afn
                )
            )

            # Si el conjunto todavía no tiene identificador,
            # se crea un estado nuevo para el AFD.
            if cierre not in identificadores:
                identificadores[cierre] = len(identificadores)
                pendientes.append(cierre)

            estado_destino = identificadores[cierre]

            transiciones_afd[estado_actual][simbolo] = estado_destino

    # Esto permite conocer qué estados del AFN representa
    # cada estado numérico del AFD.
    conjuntos = {
        identificador: set(conjunto)
        for conjunto, identificador in identificadores.items()
    }

    return {
        'inicial': 0,
        'finales': estados_finales,
        'transiciones': transiciones_afd,
        'alfabeto': alfabeto,
        'conjuntos': conjuntos
    }