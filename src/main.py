from pathlib import Path

from regex_parser import puntos, convertir_a_posfija
from afn import thompson
from afd import subconjuntos
from minimizacion import minimizar_afd
from simulacion import simular_afn, simular_afd
from graficas import graficar_afn, graficar_afd
from tablas import crear_reporte_tablas


def procesar_expresion(expresion, cadena, numero=1):
    """
    Ejecuta todo el proceso para una expresión y una cadena.
    """
    # '#' es una forma fácil de ingresar epsilon, tanto en la
    # expresión regular como en la cadena que se desea verificar.
    if cadena.strip() == '#':
        cadena = ''

    expresion_con_puntos = puntos(expresion)

    posfija = convertir_a_posfija(expresion)

    afn = thompson(posfija)

    afd = subconjuntos(afn)

    reporte_tablas = crear_reporte_tablas(
        afn,
        afd
    )

    afd_minimo = minimizar_afd(afd)

    resultado_afn = simular_afn(
        afn,
        cadena
    )

    resultado_afd = simular_afd(
        afd,
        cadena
    )

    resultado_minimo = simular_afd(
        afd_minimo,
        cadena
    )

    # Cada expresión tiene su propia carpeta de resultados.
    carpeta = (
        Path('resultados')
        / f'expresion_{numero}'
    )

    carpeta.mkdir(
        parents=True,
        exist_ok=True
    )

    ruta_tablas = carpeta / 'tablas.txt'

    cadena_mostrada = cadena if cadena else 'ε (cadena vacía)'
    respuesta = "SÍ pertenece" if resultado_afn else "NO pertenece"
    decision = 'aceptan' if resultado_afn else 'rechazan'
    verificacion = (
        '\n\nVERIFICACIÓN DE PERTENENCIA\n'
        f'r = {expresion}\n'
        f'w = {cadena_mostrada}\n'
        f'AFN: {"acepta" if resultado_afn else "rechaza"}\n'
        f'AFD: {"acepta" if resultado_afd else "rechaza"}\n'
        f'AFD mínimo: {"acepta" if resultado_minimo else "rechaza"}\n'
        f'Respuesta: w {respuesta} a L(r). El AFN y el AFD '
        f'{decision} la cadena.\n'
    )

    ruta_tablas.write_text(
        reporte_tablas + verificacion,
        encoding='utf-8'
    )

    graficar_afn(
        afn,
        carpeta / 'afn.png'
    )

    graficar_afd(
        afd,
        carpeta / 'afd.png'
    )

    graficar_afd(
        afd_minimo,
        carpeta / 'afd_minimo.png',
        titulo='AFD minimizado',
        prefijo='M'
    )

    print(f"\n--- Expresión {numero} ---")

    print(
        "Original:",
        expresion
    )

    print(
        "Con concatenaciones:",
        expresion_con_puntos
    )

    print(
        "Posfija:",
        ''.join(posfija)
    )

    if cadena:
        print("Cadena:", cadena)
    else:
        print("Cadena: ε (cadena vacía)")

    print(
        "Estados del AFN:",
        len(afn['transiciones'])
    )

    print(
        "Estados del AFD:",
        len(afd['transiciones'])
    )

    print(
        "Estados del AFD mínimo:",
        len(afd_minimo['transiciones'])
    )

    print()
    print(reporte_tablas)

    print(
        "AFN:",
        "sí" if resultado_afn else "no"
    )

    print(
        "AFD:",
        "sí" if resultado_afd else "no"
    )

    print(
        "AFD mínimo:",
        "sí" if resultado_minimo else "no"
    )

    print(
        f"Respuesta: w {respuesta} a L(r). "
        f"El AFN y el AFD {decision} "
        "la cadena."
    )

    print(
        "Imágenes guardadas en:",
        carpeta
    )

    print(
        "Tablas guardadas en:",
        ruta_tablas
    )

    # Los tres autómatas deben aceptar y rechazar
    # exactamente las mismas cadenas.
    if not (
        resultado_afn
        == resultado_afd
        == resultado_minimo
    ):
        raise RuntimeError(
            "Los tres autómatas produjeron "
            "resultados diferentes"
        )


def procesar_archivo(ruta):
    """
    Procesa las expresiones contenidas en un archivo de texto.

    Formatos aceptados:

        expresión;cadena

    o solamente:

        expresión

    Si una línea solamente tiene una expresión, el programa
    solicita la cadena desde el teclado.
    """
    with open(
        ruta,
        'r',
        encoding='utf-8'
    ) as archivo:

        cantidad_expresiones = 0

        for numero_linea, linea in enumerate(
            archivo,
            start=1
        ):
            linea = linea.strip()

            # Se usa "//" para comentarios porque "#" representa ε.
            if not linea or linea.startswith('//'):
                continue

            if ';' in linea:
                expresion, cadena = linea.split(
                    ';',
                    1
                )

                expresion = expresion.strip()
                cadena = cadena.strip()

            else:
                expresion = linea

                cadena = input(
                    "Cadena para la expresión de la "
                    f"línea {numero_linea} "
                    f"({expresion}): "
                )

            cantidad_expresiones += 1

            try:
                procesar_expresion(
                    expresion,
                    cadena,
                    cantidad_expresiones
                )

            except (ValueError, RuntimeError) as error:
                print(
                    f"\nError en la línea "
                    f"{numero_linea}: {error}"
                )

        if cantidad_expresiones == 0:
            print(
                "El archivo no contiene expresiones "
                "para procesar."
            )


def main():
    print(
        "Proyecto 1 - Expresiones regulares y autómatas"
    )

    print(
        "1. Ingresar una expresión manualmente"
    )

    print(
        "2. Procesar un archivo de texto"
    )

    opcion = input(
        "Seleccione una opción: "
    ).strip()

    try:
        if opcion == '1':
            expresion = input(
                "Ingrese la expresión regular: "
            )

            cadena = input(
                "Ingrese la cadena que desea evaluar: "
            )

            procesar_expresion(
                expresion,
                cadena
            )

        elif opcion == '2':
            ruta = input(
                "Ingrese la ruta del archivo: "
            ).strip()

            procesar_archivo(ruta)

        else:
            print(
                "La opción seleccionada no es válida."
            )

    except (
        ValueError,
        RuntimeError,
        OSError
    ) as error:
        print(
            "\nError:",
            error
        )


if __name__ == '__main__':
    main()
