precedencia = {
    '|': 2,
    '.': 3,
    '?': 4,
    '*': 4,
    '+': 4,
}

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
        elif current not in precedencia:
            posfix.append(current)
        else:
            while stack and stack[-1] != '(' and precedencia[stack[-1]] >= precedencia[current]:
                posfix.append(stack.pop())
            stack.append(current)

    while stack:
        posfix.append(stack.pop())

    return posfix


c = analizador("(b|b)*abb(a|b)*")
print(c)