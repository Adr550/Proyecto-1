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
- Tablas de transición del AFN-ε y del AFD por subconjuntos.
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
| `ε` o `#` | Cadena vacía (epsilon) |

La concatenación también puede escribirse implícitamente.

Al solicitar la cadena `w`, puede ingresarse `#` para evaluar la
cadena vacía. En archivos, los comentarios deben comenzar con `//`.

Por ejemplo:

```text
abb
```

## Tablas generadas

Para cada expresión se crea un archivo `tablas.txt` dentro de su
carpeta de resultados. Primero aparece la tabla del AFN con una
columna para cada símbolo y otra para `ε`. Después aparece la tabla
del AFD con las columnas `Estado AFD`, `Estado AFN` y las transiciones.

Cada fila del AFD representa un subconjunto de estados del AFN,
obtenido al aplicar `cerradura-ε(mover(conjunto, símbolo))`.
