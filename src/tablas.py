from afn import EPSILON


def conjunto_como_texto(estados, prefijo='q'):
    """
    Convierte un conjunto de estados a un texto fácil de leer.
    """
    if not estados:
        return '∅'

    nombres = []

    for estado in sorted(estados):
        nombres.append(f'{prefijo}{estado}')

    return '{' + ', '.join(nombres) + '}'


def crear_tabla(encabezados, filas):
    """
    Crea una tabla de texto sin utilizar librerías adicionales.
    """
    anchos = []

    for columna in range(len(encabezados)):
        ancho = len(encabezados[columna])

        for fila in filas:
            if len(fila[columna]) > ancho:
                ancho = len(fila[columna])

        anchos.append(ancho)

    separador = '+'

    for ancho in anchos:
        separador += '-' * (ancho + 2) + '+'

    lineas = [separador]
    lineas.append(crear_fila(encabezados, anchos))
    lineas.append(separador)

    for fila in filas:
        lineas.append(crear_fila(fila, anchos))

    lineas.append(separador)

    return '\n'.join(lineas)


def crear_fila(fila, anchos):
    texto = '|'

    for columna in range(len(fila)):
        texto += ' ' + fila[columna].ljust(anchos[columna]) + ' |'

    return texto


def tabla_transiciones_afn(afn, alfabeto):
    """
    Muestra una columna por símbolo y una columna para epsilon.
    """
    encabezados = ['Estado AFN'] + list(alfabeto) + [EPSILON]
    filas = []

    for estado in sorted(afn['transiciones']):
        nombre = f'q{estado}'

        if estado == afn['inicial']:
            nombre = '->' + nombre

        if estado == afn['final']:
            nombre = '*' + nombre

        destinos_por_simbolo = {}

        for simbolo in alfabeto:
            destinos_por_simbolo[simbolo] = set()

        destinos_por_simbolo[EPSILON] = set()

        for simbolo, destino in afn['transiciones'][estado]:
            destinos_por_simbolo[simbolo].add(destino)

        fila = [nombre]

        for simbolo in list(alfabeto) + [EPSILON]:
            fila.append(
                conjunto_como_texto(destinos_por_simbolo[simbolo])
            )

        filas.append(fila)

    return crear_tabla(encabezados, filas)


def tabla_transiciones_afd(afd):
    """
    Relaciona cada estado del AFD con su subconjunto del AFN y
    después muestra sus transiciones para cada símbolo.
    """
    encabezados = ['Estado AFD', 'Estado AFN'] + list(afd['alfabeto'])
    filas = []

    for estado in sorted(afd['transiciones']):
        nombre = f'D{estado}'

        if estado == afd['inicial']:
            nombre = '->' + nombre

        if estado in afd['finales']:
            nombre = '*' + nombre

        fila = [
            nombre,
            conjunto_como_texto(afd['conjuntos'][estado])
        ]

        for simbolo in afd['alfabeto']:
            destino = afd['transiciones'][estado][simbolo]
            fila.append(f'D{destino}')

        filas.append(fila)

    return crear_tabla(encabezados, filas)


def crear_reporte_tablas(afn, afd):
    tabla_afn = tabla_transiciones_afn(
        afn,
        afd['alfabeto']
    )

    tabla_afd = tabla_transiciones_afd(afd)

    return (
        'TABLA DE TRANSICIONES DEL AFN-ε\n'
        '-> estado inicial, * estado de aceptación\n\n'
        + tabla_afn
        + '\n\n'
        + 'TABLA DE CONSTRUCCIÓN DEL AFD POR SUBCONJUNTOS\n'
        + 'Cada Estado AFD representa el conjunto de la columna Estado AFN.\n'
        + '-> estado inicial, * estado de aceptación\n\n'
        + tabla_afd
    )
