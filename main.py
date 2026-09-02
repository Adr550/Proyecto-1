precedencia = {
    '(': 1,
    '|': 2,
    '.': 3,
    '?': 4,
    '*': 4,
    '+': 4,
}


def analizador(cadena):
    """Esta función convierte de infix a posfix"""
    t = list(cadena)
    posfix = []
    stack = []

    for current in t:
        if current not in precedencia:
            posfix.append(current)

        elif current in precedencia:


            if len(stack) > 0:
                if precedencia[stack[-1]] < precedencia[current]:
                    stack.append(current)

                elif precedencia[stack[-1]] > precedencia[current]:
                    while (
                        len(stack) > 0
                        and precedencia[stack[-1]] > precedencia[current]
                    ):
                        posfix.append(stack.pop())

                    stack.append(current)

                else:
                    posfix.append(stack.pop())
                    stack.append(current)

            else:
                stack.append(current)

    while len(stack) > 0:
        posfix.append(stack.pop())

    return posfix


c = analizador("a|b")
print(c)