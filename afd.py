# afd.py
# aqui esta toda la parte de autómatas del proyecto.
# cada condicion que elige el usuario se convierte en un afd (autómata finito determinista).
# un afd lo guardamos como un diccionario con:
#   nombre      -> texto para mostrar, por ejemplo "contiene 101"
#   estados     -> lista de estados, son numeros 0, 1, 2, ...
#   inicio      -> el estado inicial, siempre es 0
#   delta       -> la tabla de transiciones, (estado, simbolo) -> estado siguiente
#   aceptacion  -> conjunto de estados donde la cadena se acepta
#   trampa      -> el estado trampa si tiene uno, si no es None


def crear_afd(nombre, estados, delta, aceptacion, trampa=None):
    # junta todo en un diccionario para no andar pasando muchas variables
    return {
        "nombre": nombre,
        "estados": list(estados),
        "inicio": 0,
        "delta": delta,
        "aceptacion": set(aceptacion),
        "trampa": trampa,
    }


# funcion de apoyo para "contiene x" y "termina en x"

def siguiente_estado(x, i, c):
    # estoy en el estado i, o sea ya coinciden los primeros i simbolos de x.
    # leo el simbolo c y armo lo que llevo: los primeros i de x mas c.
    llevo = x[:i] + c
    # busco el pedazo mas largo del final de "llevo" que sea igual al inicio de x.
    # empiezo por el mas largo posible y voy bajando.
    k = min(len(llevo), len(x))
    while k > 0:
        if llevo.endswith(x[:k]):
            return k
        k -= 1
    # si no coincide nada regreso al estado 0
    return 0


# plantillas, una funcion por cada tipo de condicion

def empieza_con(sigma, x):
    # estados 0..m y un estado trampa m+1
    m = len(x)
    trampa = m + 1
    delta = {}
    for i in range(m):
        for c in sigma:
            if c == x[i]:
                delta[(i, c)] = i + 1      # coincide, avanzo
            else:
                delta[(i, c)] = trampa     # ya no empieza con x
    for c in sigma:
        delta[(m, c)] = m                  # ya empezo con x, me quedo aqui
        delta[(trampa, c)] = trampa        # de la trampa no se sale
    return crear_afd("empieza con " + x, range(m + 2), delta, {m}, trampa)


def contiene(sigma, x):
    # el estado i significa "los ultimos i simbolos que lei son los primeros i de x"
    m = len(x)
    delta = {}
    for i in range(m):
        for c in sigma:
            delta[(i, c)] = siguiente_estado(x, i, c)
    for c in sigma:
        delta[(m, c)] = m                  # ya encontre x, me quedo aqui
    return crear_afd("contiene " + x, range(m + 1), delta, {m})


def termina_en(sigma, x):
    # igual que contiene, pero el estado m no se queda fijo,
    # porque la cadena tiene que terminar justo en x
    m = len(x)
    delta = {}
    for i in range(m + 1):
        for c in sigma:
            delta[(i, c)] = siguiente_estado(x, i, c)
    return crear_afd("termina en " + x, range(m + 1), delta, {m})


def cantidad(sigma, s, n, modo):
    # el estado i significa "he leido i veces el simbolo s"
    # el estado n+1 significa "lo lei mas de n veces"
    delta = {}
    for i in range(n + 2):
        for c in sigma:
            if c == s:
                delta[(i, c)] = min(i + 1, n + 1)
            else:
                delta[(i, c)] = i          # otro simbolo no cambia la cuenta
    # lo unico que cambia entre los tres modos es que estados aceptan
    if modo == "exactamente":
        aceptacion = {n}
    elif modo == "al menos":
        aceptacion = {n, n + 1}
    else:  # "a lo sumo"
        aceptacion = set(range(n + 1))
    nombre = modo + " " + str(n) + " veces " + s
    return crear_afd(nombre, range(n + 2), delta, aceptacion)


def multiplo(sigma, s, k, residuo=0, nombre=None):
    # el estado i significa "el numero de s que llevo deja residuo i al dividir entre k"
    delta = {}
    for i in range(k):
        for c in sigma:
            if c == s:
                delta[(i, c)] = (i + 1) % k
            else:
                delta[(i, c)] = i
    if nombre is None:
        nombre = "cantidad de " + s + " múltiplo de " + str(k)
    return crear_afd(nombre, range(k), delta, {residuo})


def negar(afd):
    # para negar una condicion intercambio estados de aceptacion y de no aceptacion.
    # funciona porque todos los afd estan completos (tienen transicion para todo).
    nuevo = dict(afd)
    nuevo["aceptacion"] = set(afd["estados"]) - afd["aceptacion"]
    nuevo["nombre"] = "NO " + afd["nombre"]
    return nuevo


# lista de tipos de condicion para la interfaz
# "pide" dice que datos necesita: "x" (una cadena) o "s" y "n" (simbolo y numero)

TIPOS = [
    "Empieza con",
    "Contiene",
    "Termina en",
    "Exactamente n veces el símbolo",
    "Al menos n veces el símbolo",
    "A lo sumo n veces el símbolo",
    "Cantidad del símbolo múltiplo de n",
    "Cantidad par del símbolo",
    "Cantidad impar del símbolo",
]


def construir(sigma, tipo, texto, numero, negada):
    # recibe lo que escribio el usuario y regresa el afd ya armado.
    # si algo esta mal lanza un ValueError con un mensaje para mostrar.
    if tipo in ("Empieza con", "Contiene", "Termina en"):
        if texto == "":
            raise ValueError("Escribe la cadena x para la condición «" + tipo + "».")
        for c in texto:
            if c not in sigma:
                raise ValueError("El símbolo «" + c + "» de «" + texto + "» no está en el alfabeto.")
        if tipo == "Empieza con":
            afd = empieza_con(sigma, texto)
        elif tipo == "Contiene":
            afd = contiene(sigma, texto)
        else:
            afd = termina_en(sigma, texto)
    else:
        # las demas condiciones piden un solo simbolo
        if len(texto) != 1 or texto not in sigma:
            raise ValueError("Para «" + tipo + "» escribe un solo símbolo que esté en el alfabeto.")
        if tipo == "Cantidad par del símbolo":
            afd = multiplo(sigma, texto, 2, 0, "cantidad par de " + texto)
        elif tipo == "Cantidad impar del símbolo":
            afd = multiplo(sigma, texto, 2, 1, "cantidad impar de " + texto)
        else:
            # estas si necesitan el numero
            if not numero.isdigit():
                raise ValueError("Para «" + tipo + "» escribe un número entero en n.")
            n = int(numero)
            if tipo == "Exactamente n veces el símbolo":
                afd = cantidad(sigma, texto, n, "exactamente")
            elif tipo == "Al menos n veces el símbolo":
                afd = cantidad(sigma, texto, n, "al menos")
            elif tipo == "A lo sumo n veces el símbolo":
                afd = cantidad(sigma, texto, n, "a lo sumo")
            else:
                if n < 1:
                    raise ValueError("Para «múltiplo de n», n tiene que ser 1 o más.")
                afd = multiplo(sigma, texto, n)
    if negada:
        afd = negar(afd)
    return afd


# correr los afd en paralelo

def correr(afds, cadena):
    # todos los afd leen el mismo simbolo al mismo tiempo, cada uno avanza por su lado.
    # regresa:
    #   acepta    -> True si todos terminaron en aceptacion
    #   recorridos -> para cada afd, la lista de estados por los que paso
    actuales = [afd["inicio"] for afd in afds]
    recorridos = [[afd["inicio"]] for afd in afds]
    for c in cadena:
        for j, afd in enumerate(afds):
            actuales[j] = afd["delta"][(actuales[j], c)]
            recorridos[j].append(actuales[j])
    cumple = [actuales[j] in afds[j]["aceptacion"] for j in range(len(afds))]
    acepta = all(cumple)
    return acepta, recorridos, cumple


# cosas para mostrar

def nombre_estado(afd, q):
    # pone q0, q1, ... y marca la trampa
    if q == afd["trampa"]:
        return "trampa"
    return "q" + str(q)


def tabla_texto(afd, sigma):
    # arma la tabla de transiciones como texto
    # -> marca el estado inicial y * los de aceptacion
    ancho = 10
    lineas = []
    lineas.append(afd["nombre"])
    lineas.append("")
    encabezado = "estado".ljust(ancho + 4) + "".join(("lee " + c).ljust(ancho) for c in sigma)
    lineas.append(encabezado)
    lineas.append("-" * len(encabezado))
    for q in afd["estados"]:
        marca = ""
        if q == afd["inicio"]:
            marca += "->"
        if q in afd["aceptacion"]:
            marca += "*"
        fila = (marca.ljust(4) + nombre_estado(afd, q)).ljust(ancho + 4)
        for c in sigma:
            fila += nombre_estado(afd, afd["delta"][(q, c)]).ljust(ancho)
        lineas.append(fila)
    lineas.append("")
    lineas.append("-> estado inicial     * estado de aceptación")
    return "\n".join(lineas)
