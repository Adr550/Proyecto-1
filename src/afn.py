EPSILON = 'ε'

from regex_parser import restaurar_literal

OPERADORES = {'|', '.', '*', '+', '?'}


def thompson(posfija):
    transiciones = {}
    pila = []
    contador = 0

    def nuevo_estado():
        nonlocal contador

        estado = contador
        contador += 1
        transiciones[estado] = []

        return estado

    def agregar_transicion(origen, simbolo, destino):
        transiciones[origen].append((simbolo, destino))

    def sacar_fragmento(operador):
        """
        Saca un fragmento de la pila y evita que el programa
        falle con un IndexError poco comprensible.
        """
        if not pila:
            raise ValueError(
                f"Falta un operando para el operador '{operador}'"
            )

        return pila.pop()

    for elemento in posfija:

        # Símbolo del alfabeto
        if elemento not in OPERADORES:
            inicio = nuevo_estado()
            fin = nuevo_estado()

            agregar_transicion(inicio, restaurar_literal(elemento), fin)

            pila.append((inicio, fin))

        # Concatenación
        elif elemento == '.':
            derecho = sacar_fragmento(elemento)
            izquierdo = sacar_fragmento(elemento)

            agregar_transicion(
                izquierdo[1],
                EPSILON,
                derecho[0]
            )

            pila.append((izquierdo[0], derecho[1]))

        # Unión
        elif elemento == '|':
            derecho = sacar_fragmento(elemento)
            izquierdo = sacar_fragmento(elemento)

            inicio = nuevo_estado()
            fin = nuevo_estado()

            agregar_transicion(
                inicio,
                EPSILON,
                izquierdo[0]
            )

            agregar_transicion(
                inicio,
                EPSILON,
                derecho[0]
            )

            agregar_transicion(
                izquierdo[1],
                EPSILON,
                fin
            )

            agregar_transicion(
                derecho[1],
                EPSILON,
                fin
            )

            pila.append((inicio, fin))

        # Cerradura de Kleene
        elif elemento == '*':
            fragmento = sacar_fragmento(elemento)

            inicio = nuevo_estado()
            fin = nuevo_estado()

            agregar_transicion(
                inicio,
                EPSILON,
                fragmento[0]
            )

            agregar_transicion(
                inicio,
                EPSILON,
                fin
            )

            agregar_transicion(
                fragmento[1],
                EPSILON,
                fragmento[0]
            )

            agregar_transicion(
                fragmento[1],
                EPSILON,
                fin
            )

            pila.append((inicio, fin))

        # Cerradura positiva
        elif elemento == '+':
            fragmento = sacar_fragmento(elemento)

            inicio = nuevo_estado()
            fin = nuevo_estado()

            agregar_transicion(
                inicio,
                EPSILON,
                fragmento[0]
            )

            agregar_transicion(
                fragmento[1],
                EPSILON,
                fragmento[0]
            )

            agregar_transicion(
                fragmento[1],
                EPSILON,
                fin
            )

            pila.append((inicio, fin))

        # Cero o una aparición
        elif elemento == '?':
            fragmento = sacar_fragmento(elemento)

            inicio = nuevo_estado()
            fin = nuevo_estado()

            agregar_transicion(
                inicio,
                EPSILON,
                fragmento[0]
            )

            agregar_transicion(
                inicio,
                EPSILON,
                fin
            )

            agregar_transicion(
                fragmento[1],
                EPSILON,
                fin
            )

            pila.append((inicio, fin))

    if len(pila) != 1:
        raise ValueError(
            "La expresión posfija no es válida"
        )

    inicio, fin = pila.pop()

    return {
        'inicial': inicio,
        'final': fin,
        'transiciones': transiciones
    }
