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

    # Se calculan niveles desde el estado inicial. Esto coloca el
    # inicio a la izquierda y el final a la derecha. En una unión,
    # las dos alternativas quedan como dos ramas paralelas, igual
    # que en la construcción de Thompson.
    niveles = {inicial: 0}
    pendientes = [inicial]

    while pendientes:
        origen = pendientes.pop(0)

        if es_afn:
            salidas = transiciones.get(origen, [])
            destinos = [destino for simbolo, destino in salidas]
        else:
            salidas = transiciones.get(origen, {})
            destinos = list(salidas.values())

        for destino in destinos:
            if destino not in niveles:
                niveles[destino] = niveles[origen] + 1
                pendientes.append(destino)

    # Normalmente todos son alcanzables. Esta parte evita errores
    # si se recibe manualmente un autómata con estados aislados.
    ultimo_nivel = max(niveles.values())

    for estado in estados:
        if estado not in niveles:
            ultimo_nivel += 1
            niveles[estado] = ultimo_nivel

    estados_por_nivel = {}

    for estado in estados:
        nivel = niveles[estado]

        if nivel not in estados_por_nivel:
            estados_por_nivel[nivel] = []

        estados_por_nivel[nivel].append(estado)

    maximo_vertical = max(
        len(grupo)
        for grupo in estados_por_nivel.values()
    )

    figura, eje = plt.subplots(
        figsize=(
            max(9, (ultimo_nivel + 1) * 1.7),
            max(4.5, maximo_vertical * 2.0)
        )
    )

    eje.set_aspect('equal')
    eje.axis('off')

    posiciones = {}

    for nivel in sorted(estados_por_nivel):
        grupo = sorted(estados_por_nivel[nivel])

        for indice, estado in enumerate(grupo):
            y = (
                (len(grupo) - 1) / 2
                - indice
            ) * 1.8

            posiciones[estado] = (
                nivel * 1.8,
                y
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
        x_inicial - 1.0,
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

    # Recuerda las posiciones ya usadas por etiquetas para evitar que
    # varias transiciones escriban sus símbolos unas sobre otras.
    etiquetas_por_zona = {}

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
                y1 + 0.88,
                etiqueta,
                horizontalalignment='center',
                fontsize=9,
                zorder=5,
                bbox={
                    'facecolor': 'white',
                    'edgecolor': 'none',
                    'alpha': 0.9,
                    'pad': 1.5
                }
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
        diferencia_niveles = abs(
            niveles[destino] - niveles[origen]
        )

        if existe_inversa:
            # Se usa el mismo signo en ambas direcciones porque al
            # invertir origen y destino también se invierte la curva.
            # Así las dos flechas quedan en lados distintos.
            curvatura = 0.22
        elif diferencia_niveles:
            # Las aristas que saltan más de un nivel se curvan para no
            # atravesar estados intermedios ni sus nombres.
            curvatura = 0.13 if diferencia_niveles > 1 else 0
        else:
            # Separa transiciones entre estados del mismo nivel.
            curvatura = 0.18 if y1 <= y2 else -0.18

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

        zona = (round(medio_x, 1), round(medio_y, 1))
        repeticion = etiquetas_por_zona.get(zona, 0)
        etiquetas_por_zona[zona] = repeticion + 1

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

        separacion_extra = (repeticion // 2 + repeticion % 2) * 0.18
        if repeticion % 2 == 0:
            separacion_extra *= -1

        eje.text(
            medio_x + perpendicular_x,
            medio_y + perpendicular_y + separacion_extra,
            etiqueta,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=9,
            zorder=5,
            bbox={
                'facecolor': 'white',
                'edgecolor': 'none',
                'alpha': 0.9,
                'pad': 1.5
            }
        )

    valores_x = [posicion[0] for posicion in posiciones.values()]
    valores_y = [posicion[1] for posicion in posiciones.values()]

    eje.set_xlim(
        min(valores_x) - 1.35,
        max(valores_x) + 1.0
    )

    eje.set_ylim(
        min(valores_y) - 1.15,
        max(valores_y) + 1.15
    )

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
