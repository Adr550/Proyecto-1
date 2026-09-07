from regex_parser import convertir_a_posfija
from afn import thompson
from afd import subconjuntos
from minimizacion import minimizar_afd
from simulacion import simular_afn, simular_afd
from tablas import crear_reporte_tablas


def probar(expresion, casos):
    posfija = convertir_a_posfija(expresion)
    afn = thompson(posfija)
    afd = subconjuntos(afn)
    afd_minimo = minimizar_afd(afd)

    reporte = crear_reporte_tablas(afn, afd)

    assert 'Estado AFN' in reporte
    assert 'Estado AFD' in reporte
    assert 'ε' in reporte

    for cadena, esperado in casos:
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

        assert resultado_afn == esperado, (
            f"El AFN falló con la expresión '{expresion}' "
            f"y la cadena '{cadena}'"
        )

        assert resultado_afd == esperado, (
            f"El AFD falló con la expresión '{expresion}' "
            f"y la cadena '{cadena}'"
        )

        assert resultado_minimo == esperado, (
            f"El AFD mínimo falló con la expresión '{expresion}' "
            f"y la cadena '{cadena}'"
        )

        assert (
            resultado_afn
            == resultado_afd
            == resultado_minimo
        ), (
            "Los autómatas dieron resultados diferentes "
            f"para la cadena '{cadena}'"
        )


def probar_error(expresion):
    """
    Comprueba que una expresión incorrecta produzca ValueError.
    """
    try:
        convertir_a_posfija(expresion)

    except ValueError:
        return

    raise AssertionError(
        f"La expresión inválida '{expresion}' fue aceptada"
    )


probar(
    '(b|b)*abb(a|b)*',
    [
        ('babbaaaa', True),
        ('abb', True),
        ('ab', False),
        ('', False),
    ]
)


probar(
    'a*',
    [
        ('', True),
        ('a', True),
        ('aaaa', True),
        ('b', False),
    ]
)


probar(
    'ab+c?',
    [
        ('ab', True),
        ('abb', True),
        ('abc', True),
        ('abbc', True),
        ('a', False),
    ]
)


probar(
    'ε|ab',
    [
        ('', True),
        ('ab', True),
        ('a', False),
    ]
)


probar(
    '#|ab',
    [
        ('', True),
        ('ab', True),
        ('#', True),
        ('a', False),
    ]
)


expresiones_invalidas = [
    '',
    '(a|b',
    'a|b)',
    '|ab',
    'ab|',
    '*a',
    '()',
]


for expresion_invalida in expresiones_invalidas:
    probar_error(expresion_invalida)


print("Todas las pruebas pasaron correctamente")
