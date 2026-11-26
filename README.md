# ANALIZADOR DE CADENAS CON AFD
Proyecto final de Lenguajes Formales

# QUÉ HACE
El usuario escribe un alfabeto, agrega condiciones (empieza con, contiene,
termina en, cantidad de un símbolo, múltiplo o paridad, y la negación de
cualquiera) y prueba cadenas. El programa arma un AFD por cada condición,
los corre al mismo tiempo sobre la cadena y la acepta solo si todos
terminan en un estado de aceptación.

# ARCHIVOS
afd.py        la parte de autómatas (plantillas, negación y correr en paralelo)
interfaz.py   la ventana hecha con tkinter
pruebas.py    casos de prueba que se corren en la terminal

# CÓMO CORRERLO
1. Abrir una terminal en esta carpeta.
2. Para la ventana:     python3 interfaz.py
3. Para las pruebas:    python3 pruebas.py

No necesita instalar nada, tkinter ya viene con Python.
En Mac, si sale "No module named tkinter" (pasa con el Python de Homebrew):
    brew install python-tk

# CÓMO SE USA
1. Escribir el alfabeto, por ejemplo 0,1
2. Elegir el tipo de condición, escribir x o el símbolo (y n si lo pide),
   marcar "Negar" si se quiere la condición contraria y darle Agregar.
3. Escribir la cadena y darle Probar (o Enter).
4. "Ver tabla" muestra la tabla de transiciones de la condición seleccionada.
5. "Cargar ejemplo" pone el ejemplo del reporte (empieza con 1, contiene 101,
   termina en 0) con la cadena 11010.
