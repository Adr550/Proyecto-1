# Proyecto-1
# Proyecto 1 - Expresiones regulares y autómatas

Programa en Python que construye y simula autómatas finitos a partir de expresiones regulares.

El programa convierte una expresión regular de notación infix a postfix, construye un AFN con Thompson, genera un AFD mediante subconjuntos y minimiza el AFD. También determina si una cadena pertenece al lenguaje y genera una imagen de cada autómata.

## Funcionalidades

- Conversión de infix a postfix con Shunting Yard.
- Construcción de AFN con Thompson.
- Conversión de AFN a AFD mediante subconjuntos.
- Minimización del AFD.
- Simulación del AFN, AFD y AFD mínimo.
- Generación de imágenes PNG.
- Lectura de expresiones desde un archivo de texto.
- Validación de expresiones regulares.

## Operadores admitidos

| Operador | Significado |
|----------|-------------|
| `\|` | Unión |
| `.` | Concatenación explícita |
| `*` | Cero o más repeticiones |
| `+` | Una o más repeticiones |
| `?` | Cero o una aparición |
| `( )` | Agrupación |
| `ε` | Cadena vacía |

La concatenación también puede escribirse implícitamente.

Por ejemplo:

```text
abb