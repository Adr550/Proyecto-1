precedencia = {
    '|': 2,
    '.': 3,
}

unarios = {'?', '*', '+'}


def puntos(expresion):
    resultado = []
    operadores = {'|', '.', '?', '*', '+'}

    expresion = expresion.replace(' ', '')

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

    for elemento in posfija:

        # Símbolo del alfabeto
        if elemento not in {'|', '.', '*', '+', '?'}:
            inicio = nuevo_estado()
            fin = nuevo_estado()

            agregar_transicion(inicio, elemento, fin)
            pila.append((inicio, fin))

        # Concatenación
        elif elemento == '.':
            derecho = pila.pop()
            izquierdo = pila.pop()

            agregar_transicion(izquierdo[1], 'ε', derecho[0])
            pila.append((izquierdo[0], derecho[1]))

        # Unión
        elif elemento == '|':
            derecho = pila.pop()
            izquierdo = pila.pop()

            inicio = nuevo_estado()
            fin = nuevo_estado()

            agregar_transicion(inicio, 'ε', izquierdo[0])
            agregar_transicion(inicio, 'ε', derecho[0])

            agregar_transicion(izquierdo[1], 'ε', fin)
            agregar_transicion(derecho[1], 'ε', fin)

            pila.append((inicio, fin))

        # Cerradura de Kleene
        elif elemento == '*':
            fragmento = pila.pop()

            inicio = nuevo_estado()
            fin = nuevo_estado()

            agregar_transicion(inicio, 'ε', fragmento[0])
            agregar_transicion(inicio, 'ε', fin)

            agregar_transicion(fragmento[1], 'ε', fragmento[0])
            agregar_transicion(fragmento[1], 'ε', fin)

            pila.append((inicio, fin))

        elif elemento == '+':
            fragmento = pila.pop()

            inicio = nuevo_estado()
            fin = nuevo_estado()

            agregar_transicion(inicio, 'ε', fragmento[0])
            agregar_transicion(fragmento[1], 'ε', fragmento[0])
            agregar_transicion(fragmento[1], 'ε', fin)

            pila.append((inicio, fin))

        # Cero o una aparición
        elif elemento == '?':
            fragmento = pila.pop()

            inicio = nuevo_estado()
            fin = nuevo_estado()

            agregar_transicion(inicio, 'ε', fragmento[0])
            agregar_transicion(inicio, 'ε', fin)
            agregar_transicion(fragmento[1], 'ε', fin)

            pila.append((inicio, fin))

    if len(pila) != 1:
        raise ValueError("La expresión posfija no es válida")


    inicio, fin = pila.pop()

    return {
        'inicial': inicio,
        'final': fin,
        'transiciones': transiciones
    }

c = analizador("(b|b)*abb(a|b)*")

print("Original:", c)
print("Como cadena:", ''.join(c))