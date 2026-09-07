import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch


def agrupar_transiciones(transiciones, es_afn):
    """
    Agrupa las transiciones que tienen el mismo origen y destino.

    Por ejemplo, las transiciones:

        0 --a--> 1
        0 --b--> 1

    se muestran en una sola flecha con la etiqueta: a, b
    """
    agrupadas = {}

    for origen, salidas in transiciones.items():

        if es_afn:
            elementos = salidas
        else:
            elementos = [
                (simbolo, destino)
                for simbolo, destino in salidas.items()
            ]

        for simbolo, destino in elementos:
            clave = (origen, destino)

            if clave not in agrupadas:
                agrupadas[clave] = []

            agrupadas[clave].append(simbolo)

    return agrupadas


def dibujar_automata(
    estados,
    inicial,
    finales,
    transiciones,
    ruta,
    titulo,
    prefijo,
    es_afn=False
):
    """
    Función general para dibujar un AFN o AFD.
    """
    estados = sorted(estados)
    cantidad = len(estados)

    figura, eje = plt.subplots(
        figsize=(10, 8)
    )

    eje.set_aspect('equal')
    eje.axis('off')

    # Los estados se colocan alrededor de una circunferencia.
    radio_grafo = max(
        2.3,
        cantidad * 0.32
    )

    posiciones = {}

    for indice, estado in enumerate(estados):
        angulo = (
            math.pi
            - (2 * math.pi * indice / cantidad)
        )

        posiciones[estado] = (
            radio_grafo * math.cos(angulo),
            radio_grafo * math.sin(angulo)
        )

    radio_estado = 0.34

    # Dibujar los estados.
    for estado, posicion in posiciones.items():
        x, y = posicion

        circulo = Circle(
            (x, y),
            radio_estado,
            fill=False,
            linewidth=2
        )

        eje.add_patch(circulo)

        # Los estados finales tienen doble círculo.
        if estado in finales:
            circulo_final = Circle(
                (x, y),
                radio_estado - 0.07,
                fill=False,
                linewidth=1.5
            )

            eje.add_patch(circulo_final)

        eje.text(
            x,
            y,
            f'{prefijo}{estado}',
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=10
        )

    # Flecha que señala el estado inicial.
    x_inicial, y_inicial = posiciones[inicial]

    inicio_flecha = (
        x_inicial - 1.2,
        y_inicial
    )

    fin_flecha = (
        x_inicial - radio_estado,
        y_inicial
    )

    eje.add_patch(
        FancyArrowPatch(
            inicio_flecha,
            fin_flecha,
            arrowstyle='-|>',
            mutation_scale=15,
            linewidth=1.7
        )
    )

    transiciones_agrupadas = agrupar_transiciones(
        transiciones,
        es_afn
    )

    for clave, simbolos in transiciones_agrupadas.items():
        origen, destino = clave

        x1, y1 = posiciones[origen]
        x2, y2 = posiciones[destino]

        etiqueta = ', '.join(
            sorted(set(simbolos))
        )

        # Dibujar una transición hacia el mismo estado.
        if origen == destino:
            flecha = FancyArrowPatch(
                (
                    x1 - 0.20,
                    y1 + radio_estado * 0.75
                ),
                (
                    x1 + 0.20,
                    y1 + radio_estado * 0.75
                ),
                connectionstyle='arc3,rad=-1.8',
                arrowstyle='-|>',
                mutation_scale=13,
                linewidth=1.3
            )

            eje.add_patch(flecha)

            eje.text(
                x1,
                y1 + 0.85,
                etiqueta,
                horizontalalignment='center',
                fontsize=9
            )

            continue

        diferencia_x = x2 - x1
        diferencia_y = y2 - y1

        distancia = math.hypot(
            diferencia_x,
            diferencia_y
        )

        direccion_x = diferencia_x / distancia
        direccion_y = diferencia_y / distancia

        inicio = (
            x1 + direccion_x * radio_estado,
            y1 + direccion_y * radio_estado
        )

        fin = (
            x2 - direccion_x * radio_estado,
            y2 - direccion_y * radio_estado
        )

        # Si hay flechas en ambas direcciones,
        # se curvan para distinguirlas.
        existe_inversa = (
            destino,
            origen
        ) in transiciones_agrupadas

        if existe_inversa and origen < destino:
            curvatura = 0.18
        elif existe_inversa:
            curvatura = -0.18
        else:
            curvatura = 0

        flecha = FancyArrowPatch(
            inicio,
            fin,
            connectionstyle=f'arc3,rad={curvatura}',
            arrowstyle='-|>',
            mutation_scale=13,
            linewidth=1.3
        )

        eje.add_patch(flecha)

        medio_x = (x1 + x2) / 2
        medio_y = (y1 + y2) / 2

        perpendicular_x = (
            -direccion_y
            * curvatura
            * distancia
            * 0.45
        )

        perpendicular_y = (
            direccion_x
            * curvatura
            * distancia
            * 0.45
        )

        eje.text(
            medio_x + perpendicular_x,
            medio_y + perpendicular_y,
            etiqueta,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=9,
            bbox={
                'facecolor': 'white',
                'edgecolor': 'none',
                'pad': 1
            }
        )

    margen = radio_grafo + 1.8

    eje.set_xlim(-margen, margen)
    eje.set_ylim(-margen, margen)

    eje.set_title(
        titulo,
        fontsize=16
    )

    ruta = Path(ruta)

    ruta.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    figura.savefig(
        ruta,
        dpi=180,
        bbox_inches='tight'
    )

    plt.close(figura)


def graficar_afn(afn, ruta):
    """
    Genera la imagen del AFN.
    """
    dibujar_automata(
        estados=afn['transiciones'].keys(),
        inicial=afn['inicial'],
        finales={afn['final']},
        transiciones=afn['transiciones'],
        ruta=ruta,
        titulo='AFN construido con Thompson',
        prefijo='q',
        es_afn=True
    )


def graficar_afd(
    afd,
    ruta,
    titulo='AFD por subconjuntos',
    prefijo='D'
):
    """
    Genera la imagen de un AFD.
    """
    dibujar_automata(
        estados=afd['transiciones'].keys(),
        inicial=afd['inicial'],
        finales=afd['finales'],
        transiciones=afd['transiciones'],
        ruta=ruta,
        titulo=titulo,
        prefijo=prefijo,
        es_afn=False
    )