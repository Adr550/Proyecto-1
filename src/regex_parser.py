precedencia = {
    '|': 2,
    '.': 3,
}

unarios = {'?', '*', '+'}
operadores = {'|', '.', '?', '*', '+'}

# Los caracteres privados permiten que un operador escapado atraviese el
# analizador como símbolo normal. Se restaura al construir el autómata.
literales_escapados = {
    caracter: chr(0xE000 + indice)
    for indice, caracter in enumerate(r'(){}|.*+?\\')
}
literales_originales = {
    codigo: caracter
    for caracter, codigo in literales_escapados.items()
}


def normalizar_epsilon(expresion):
    """Permite escribir epsilon como '#' o como el símbolo 'ε'."""
    return expresion.replace('#', 'ε')


def normalizar_expresion(expresion):
    """Normaliza las formas alternativas admitidas por el programa."""
    expresion = normalizar_epsilon(expresion).replace(' ', '')
    resultado = []
    posicion = 0

    while posicion < len(expresion):
        actual = expresion[posicion]

        if actual == '\\':
            if posicion + 1 >= len(expresion):
                raise ValueError("La expresión termina con una barra invertida")

            literal = expresion[posicion + 1]
            resultado.append(literales_escapados.get(literal, literal))
            posicion += 2
            continue

        resultado.append(actual)
        posicion += 1

    return ''.join(resultado)


def restaurar_literal(simbolo):
    """Devuelve el carácter representado por un literal escapado."""
    return literales_originales.get(simbolo, simbolo)


def validar_expresion(expresion):
    """
    Verifica que la expresión regular tenga una estructura válida.

    No agrega puntos ni convierte la expresión. Solamente detecta
    errores antes de ejecutar los demás algoritmos.
    """
    expresion = normalizar_expresion(expresion)

    if not expresion:
        raise ValueError(
            "La expresión regular no puede estar vacía"
        )

    parentesis = []
    espera_operando = True

    for posicion, actual in enumerate(expresion):

        if actual == '(':
            parentesis.append(posicion)
            espera_operando = True

        elif actual == ')':
            if not parentesis:
                raise ValueError(
                    "Paréntesis de cierre inesperado "
                    f"en la posición {posicion + 1}"
                )

            if espera_operando:
                raise ValueError(
                    "Falta una expresión antes de ')' "
                    f"en la posición {posicion + 1}"
                )

            parentesis.pop()
            espera_operando = False

        elif actual in unarios:
            if espera_operando:
                raise ValueError(
                    f"El operador '{actual}' no tiene operando "
                    f"en la posición {posicion + 1}"
                )

            espera_operando = False

        elif actual in {'|', '.'}:
            if espera_operando:
                raise ValueError(
                    f"El operador '{actual}' no tiene operando izquierdo "
                    f"en la posición {posicion + 1}"
                )

            espera_operando = True

        else:
            # Cualquier otro carácter se considera un símbolo
            # perteneciente al alfabeto.
            espera_operando = False

    if parentesis:
        posicion = parentesis[-1]

        raise ValueError(
            "Falta cerrar el paréntesis abierto "
            f"en la posición {posicion + 1}"
        )

    if espera_operando:
        raise ValueError(
            "La expresión termina con un operador sin operando derecho"
        )


def puntos(expresion):
    """
    Agrega explícitamente el operador de concatenación '.'.
    """
    resultado = []
    operadores = {'|', '.', '?', '*', '+'}

    expresion = normalizar_expresion(expresion)

    for actual in expresion:
        if resultado:
            anterior = resultado[-1]

            anterior_termina = (
                anterior not in operadores
                and anterior != '('
                or anterior == ')'
                or anterior in {'?', '*', '+'}
            )

            actual_inicia = (
                actual not in operadores
                and actual != ')'
                or actual == '('
            )

            if anterior_termina and actual_inicia:
                resultado.append('.')

        resultado.append(actual)

    return ''.join(resultado)


def analizador(expresion):
    """
    Convierte una expresión infix a postfix usando Shunting Yard.
    """
    posfix = []
    stack = []

    for current in expresion:
        if current == '(':
            stack.append(current)

        elif current == ')':
            while stack and stack[-1] != '(':
                posfix.append(stack.pop())

            if stack and stack[-1] == '(':
                stack.pop()

        elif current in unarios:
            posfix.append(current)

        elif current not in precedencia:
            posfix.append(current)

        else:
            while (
                stack
                and stack[-1] != '('
                and precedencia[stack[-1]] >= precedencia[current]
            ):
                posfix.append(stack.pop())

            stack.append(current)

    while stack:
        posfix.append(stack.pop())

    return posfix


def convertir_a_posfija(expresion):
    """
    Ejecuta el proceso completo:

    1. Valida la expresión.
    2. Agrega concatenaciones explícitas.
    3. Convierte de infix a postfix.
    """
    validar_expresion(expresion)

    expresion_con_puntos = puntos(expresion)

    return analizador(expresion_con_puntos)
