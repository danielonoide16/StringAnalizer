# pruebas.py
# casos de prueba del analizador, se corren en la terminal sin abrir la ventana.
# sirven para la seccion de pruebas del reporte.
#
# para correrlo:  python3 pruebas.py

import afd as automatas

SIGMA = ["0", "1"]

# cada caso es: (condiciones, cadena, resultado esperado)
# cada condicion es: (tipo, x o simbolo, n, negada)
CASOS = [
    # el ejemplo del reporte
    ([("Empieza con", "1", "", False), ("Contiene", "101", "", False), ("Termina en", "0", "", False)], "11010", True),
    ([("Empieza con", "1", "", False), ("Contiene", "101", "", False), ("Termina en", "0", "", False)], "1101", False),
    ([("Empieza con", "1", "", False), ("Contiene", "101", "", False), ("Termina en", "0", "", False)], "01010", False),
    # empieza con
    ([("Empieza con", "01", "", False)], "0110", True),
    ([("Empieza con", "01", "", False)], "1001", False),
    ([("Empieza con", "01", "", False)], "", False),
    # contiene (el caso de 00 que se queda en q1)
    ([("Contiene", "01", "", False)], "0001", True),
    ([("Contiene", "01", "", False)], "1110", False),
    # termina en
    ([("Termina en", "01", "", False)], "1101", True),
    ([("Termina en", "01", "", False)], "0110", False),
    # cantidad
    ([("Exactamente n veces el símbolo", "1", "2", False)], "0101", True),
    ([("Exactamente n veces el símbolo", "1", "2", False)], "0111", False),
    ([("Al menos n veces el símbolo", "1", "2", False)], "1110", True),
    ([("A lo sumo n veces el símbolo", "1", "2", False)], "1110", False),
    # multiplo y paridad
    ([("Cantidad del símbolo múltiplo de n", "1", "3", False)], "101010", True),
    ([("Cantidad par del símbolo", "1", "", False)], "1001", True),
    ([("Cantidad impar del símbolo", "1", "", False)], "1001", False),
    ([("Cantidad par del símbolo", "1", "", False)], "", True),
    # negacion
    ([("Contiene", "01", "", True)], "1100", True),
    ([("Contiene", "01", "", True)], "1010", False),
]


def main():
    bien = 0
    print("cadena".ljust(10), "condiciones".ljust(55), "esperado".ljust(11), "obtenido".ljust(11), "ok")
    print("-" * 95)
    for condiciones, cadena, esperado in CASOS:
        afds = [automatas.construir(SIGMA, *cond) for cond in condiciones]
        obtenido, recorridos, cumple = automatas.correr(afds, cadena)
        nombres = ", ".join(a["nombre"] for a in afds)
        ok = obtenido == esperado
        if ok:
            bien += 1
        print((cadena or "ε").ljust(10), nombres.ljust(55),
              ("ACEPTADA" if esperado else "RECHAZADA").ljust(11),
              ("ACEPTADA" if obtenido else "RECHAZADA").ljust(11),
              "sí" if ok else "NO")
    print()
    print(bien, "de", len(CASOS), "casos correctos")

    # tambien imprimo la tabla de "contiene 01" para compararla con la figura 4 del reporte
    print()
    print(automatas.tabla_texto(automatas.contiene(SIGMA, "01"), SIGMA))


if __name__ == "__main__":
    main()
