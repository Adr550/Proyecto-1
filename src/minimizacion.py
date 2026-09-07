from collections import deque


def estados_alcanzables(afd):
    """
    Encuentra los estados del AFD que pueden alcanzarse
    desde el estado inicial.
    """
    alcanzables = {afd['inicial']}
    pendientes = deque([afd['inicial']])

    while pendientes:
        estado = pendientes.popleft()

        transiciones = afd['transiciones'].get(estado, {})

        for destino in transiciones.values():
            if destino not in alcanzables:
                alcanzables.add(destino)
                pendientes.append(destino)

    return alcanzables


def minimizar_afd(afd):
    """
    Minimiza un AFD utilizando el método de particiones sucesivas.
    """
    alcanzables = estados_alcanzables(afd)

    finales = set(afd['finales']) & alcanzables
    no_finales = alcanzables - finales

    # Primera partición:
    # estados finales y estados no finales.
    particiones = []

    if finales:
        particiones.append(finales)

    if no_finales:
        particiones.append(no_finales)

    cambio = True

    while cambio:
        cambio = False

        # Indica a qué partición pertenece cada estado.
        indice_particion = {
            estado: indice
            for indice, grupo in enumerate(particiones)
            for estado in grupo
        }

        nuevas_particiones = []

        for grupo in particiones:
            grupos_por_firma = {}

            for estado in grupo:
                """
                La firma indica a qué partición llega el estado
                con cada símbolo del alfabeto.
                """
                firma = tuple(
                    indice_particion[
                        afd['transiciones'][estado][simbolo]
                    ]
                    for simbolo in afd['alfabeto']
                )

                if firma not in grupos_por_firma:
                    grupos_por_firma[firma] = set()

                grupos_por_firma[firma].add(estado)

            nuevas_particiones.extend(
                grupos_por_firma.values()
            )

            if len(grupos_por_firma) > 1:
                cambio = True

        particiones = nuevas_particiones

    # Colocar primero el grupo que contiene al estado inicial.
    grupo_inicial = next(
        grupo
        for grupo in particiones
        if afd['inicial'] in grupo
    )

    restantes = [
        grupo
        for grupo in particiones
        if grupo is not grupo_inicial
    ]

    restantes.sort(
        key=lambda grupo: min(grupo)
    )

    particiones = [grupo_inicial] + restantes

    # Relacionar cada estado antiguo con su nuevo estado.
    estado_a_grupo = {
        estado: indice
        for indice, grupo in enumerate(particiones)
        for estado in grupo
    }

    transiciones_minimas = {}

    for indice, grupo in enumerate(particiones):
        representante = min(grupo)
        transiciones_minimas[indice] = {}

        for simbolo in afd['alfabeto']:
            destino_original = (
                afd['transiciones'][representante][simbolo]
            )

            destino_minimo = estado_a_grupo[
                destino_original
            ]

            transiciones_minimas[indice][simbolo] = (
                destino_minimo
            )

    finales_minimos = {
        indice
        for indice, grupo in enumerate(particiones)
        if grupo & finales
    }

    return {
        'inicial': 0,
        'finales': finales_minimos,
        'transiciones': transiciones_minimas,
        'alfabeto': list(afd['alfabeto']),

        # Permite saber qué estados originales fueron unidos.
        'grupos': {
            indice: set(grupo)
            for indice, grupo in enumerate(particiones)
        }
    }